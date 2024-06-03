# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

import datetime as dt
import hashlib
import json
import lzma
import pathlib as pl

import msgspec

from .database import CveDatabase
from .schema import CveItem


def _year_from_cve(cve: CveItem) -> int:
    return int(cve.id.split("-")[1])


class Feed(msgspec.Struct):
    name: str
    timestamp: dt.datetime
    cves: list[CveItem]

    class Metadata(msgspec.Struct):
        last_modified: dt.datetime
        size: int
        xz_size: int
        sha256: str

        def write(self, dest: pl.Path):
            dest.write_text(
                f"lastModifiedDate:{_format_datetime(self.last_modified)}\n"
                f"size:{self.size}\n"
                f"xzSize:{self.xz_size}\n"
                f"sha256:{self.sha256}\n"
            )

    @staticmethod
    def write(
        dest_dir: str | pl.Path,
        name: str,
        db: CveDatabase,
        xz_preset: int | None = None,
    ):
        """Writes the feed of the given name into the directory dest_dir.
        A feed consists of two files:
        - CVE-${name}.json.xz
        - CVE-${name}.meta

        Raises a ValueError if the feed name is invalid.
        """
        dest_dir = pl.Path(dest_dir)

        feed = Feed.from_database(db, name=name)
        data_dest = pl.Path(f"{dest_dir}/CVE-{name}.json.xz")
        meta_dest = pl.Path(f"{dest_dir}/CVE-{name}.meta")

        feed = Feed.from_database(db, name=name)
        metadata = feed.xz_write(
            data_dest,
            xz_preset=xz_preset,
        )
        metadata.write(meta_dest)

    @classmethod
    def from_database(cls, db: CveDatabase, name: str):
        if name == "all":
            return cls._all_from_database(db)
        elif name == "recent":
            return cls._recent_from_database(db)
        elif name == "modified":
            return cls._modified_from_database(db)
        else:
            try:
                year = int(name)
            except ValueError:
                raise ValueError(f"'{name}' is not a valid feed name.")
            return cls._year_from_database(db, year)

    @classmethod
    def _year_from_database(cls, db: CveDatabase, year: int):
        # Note that the published year must not equal the year in the identifier.
        # Related: https://cve.mitre.org/cve/identifiers/syntaxchange.html

        return cls(
            name=str(year),
            cves=[cve for cve in db.cves.values() if _year_from_cve(cve) == year],
            timestamp=db.timestamp,
        )

    @classmethod
    def _all_from_database(cls, db: CveDatabase):
        return cls(
            name="all",
            timestamp=db.timestamp,
            cves=list(db.cves.values()),
        )

    @classmethod
    def _recent_from_database(cls, db: CveDatabase):
        oldest_recent_datetime = db.timestamp - dt.timedelta(days=8)
        cves = [
            cve for cve in db.cves.values() if cve.published > oldest_recent_datetime
        ]

        return cls(
            name="recent",
            timestamp=db.timestamp,
            cves=cves,
        )

    @classmethod
    def _modified_from_database(cls, db: CveDatabase):
        oldest_modified_datetime = db.timestamp - dt.timedelta(days=8)
        cves = [
            cve
            for cve in db.cves.values()
            if cve.last_modified > oldest_modified_datetime
        ]

        return cls(
            name="modified",
            timestamp=db.timestamp,
            cves=cves,
        )

    def xz_write(self, dest: pl.Path, xz_preset: int | None = None) -> Metadata:
        data = {
            # The date formats differ for the NVD dates and the feed timestamp.
            # Thus, we use a string here.
            "timestamp": self.timestamp.isoformat(sep="T", timespec="microseconds")
            + "+00:00",
            "cve_count": len(self.cves),
            "feed_name": f"CVE-{self.name}",
            "source": "fkie-cad/nvd-json-data-feeds",
            "cve_items": self.cves,
        }
        data = msgspec.to_builtins(data, builtin_types=[dt.datetime])
        data["cve_items"].sort(key=lambda cve: cve["id"])
        data_str = json.dumps(
            data,
            default=_json_serialize,
            indent=2,
        )

        with lzma.open(dest, "xt", preset=xz_preset) as f:
            f.write(data_str)

        last_modified = _get_last_modified_date(self.cves)
        sha256 = hashlib.sha256()
        sha256.update(data_str.encode())

        return Feed.Metadata(
            last_modified=last_modified,
            size=len(data_str),
            xz_size=dest.stat().st_size,
            sha256=sha256.hexdigest(),
        )


def _format_datetime(datetime: dt.datetime):
    assert datetime.utcoffset() is None

    return datetime.isoformat(sep="T", timespec="milliseconds")


def _json_serialize(obj):
    if isinstance(obj, dt.datetime):
        return _format_datetime(obj)

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _get_last_modified_date(cve_items: list[CveItem]):
    max_last_modified = dt.datetime.fromisoformat("0001-01-01")
    for cve in cve_items:
        if cve.last_modified > max_last_modified:
            max_last_modified = cve.last_modified

    return max_last_modified

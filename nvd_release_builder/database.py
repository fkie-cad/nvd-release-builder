# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

import datetime as dt
import os
import pathlib as pl

import msgspec

from . import repo
from .schema import CveId, CveItem


class CveDatabase(msgspec.Struct):
    """A collection of CVEs at a given timestamp."""

    cves: dict[str, CveItem]
    timestamp: dt.datetime

    @classmethod
    def from_timestamp(cls, timestamp: str | dt.date):
        if isinstance(timestamp, str):
            timestamp = dt.date.fromisoformat(timestamp)

        repo_timestamp = repo.checkout_timestamp()
        if repo_timestamp.date() != timestamp:
            raise ValueError(
                f"The repository currently checked out the tag at {repo_timestamp}"
                f" but the from_timestamp got {timestamp}."
                " Use repo.checkout to checkout the correct data before creating"
                f" a {CveDatabase.__qualname__}."
            )
        cves = load_cves()

        return cls(
            cves=cves,
            timestamp=repo_timestamp,
        )

    def __getitem__(self, key):
        return self.cves[key]


def load_cve(id: str | CveId) -> CveItem | None:
    """Return the CveItem for the given CVE identifier if it exists"""
    id = CveId(id)

    _, year_str, number_str = id.split("-")
    data_path = (
        repo.checkout_dir
        / f"CVE-{year_str}"
        / f"CVE-{year_str}-{number_str[:-2]}xx"
        / f"{id}.json"
    )

    data_bytes = data_path.read_bytes()
    return msgspec.json.decode(data_bytes, type=CveItem)


def load_cves() -> dict[str, CveItem]:
    cves: list[CveItem] = []
    for dirent in os.scandir(repo.checkout_dir):
        if not dirent.is_dir:
            continue
        if not dirent.name.startswith("CVE-"):
            continue

        cves.extend(
            _get_cve_items(dirent.path),
        )

    return {cve.id: cve for cve in cves}


def _get_cve_items(cve_dir: str | pl.Path) -> list[CveItem]:
    cve_dir = pl.Path(cve_dir)
    cve_items = []
    for cve_file in cve_dir.glob(f"{cve_dir.name}-*/*.json"):
        data_bytes = cve_file.read_bytes()
        cve_item = msgspec.json.decode(data_bytes, type=CveItem)
        cve_items.append(cve_item)

    return cve_items

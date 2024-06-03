# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

import datetime as dt
import os
import pathlib as pl

import pygit2
from pygit2.enums import CheckoutStrategy, ReferenceFilter, RepositoryOpenFlag

_xdg_cache_home = pl.Path(
    os.getenv("XDG_CACHE_HOME", pl.Path.home() / ".cache"),
)
checkout_dir = _xdg_cache_home / "fkie_cve_make_release" / "nvd-json-data-feeds"
checkout_dir.mkdir(exist_ok=True, parents=True)
git_dir = _xdg_cache_home / "fkie_cve_make_release" / "nvd-json-data-feeds.git"


def _get_repo_or_raise():
    if not git_dir.exists():
        raise ValueError(
            f"There is no git repository at {git_dir}. Please run"
            " 'git clone --bare https://github.com/fkie-cad/nvd-json-data-feeds.git"
            f" {git_dir}'"
        )

    return pygit2.Repository(
        str(git_dir),
        flags=RepositoryOpenFlag.BARE,
    )


_repo = _get_repo_or_raise()


def fetch():
    """Fetch the latest changes from the repository"""
    assert len(_repo.remotes) == 1
    name = next(_repo.remotes.names())
    remote = _repo.remotes[name]

    remote.fetch()


def checkout_timestamp() -> dt.datetime:
    """Returns the timestamp of the currently checked-out tag."""
    head_commit = _repo.head.peel(pygit2.Commit)
    tags: list[pygit2.Reference] = _repo.references.iterator(ReferenceFilter.TAGS)
    for tag in tags:
        tag_commit = tag.peel(pygit2.Commit)
        if tag_commit == head_commit:
            break
    else:
        raise ValueError(
            f"The current HEAD ({head_commit}) does not have an associated tag"
        )

    return _datetime_from_tag_name(tag.name)


def checkout(timestamp: dt.date):
    """Checkout the tag at the given timestamp.
    Use repo.checkout_dir to access the written date."""
    tags: list[pygit2.Reference] = _repo.references.iterator(ReferenceFilter.TAGS)
    for tag in tags:
        tag_datetime = _datetime_from_tag_name(tag.name)
        if tag_datetime.date() == timestamp:
            break
    else:
        raise ValueError(
            f"There is no tag for the timestamp {timestamp}."
            " Did you fetch the latest tags?"
        )

    _repo.checkout(
        tag,
        directory=checkout_dir,
        strategy=CheckoutStrategy.FORCE,
    )


def _datetime_from_tag_name(name: str) -> dt.datetime:
    assert name.startswith("refs/tags/v")
    dottet_datetime = name[len("refs/tags/v") :][: len("1970.01.01-000000")]
    return dt.datetime.fromisoformat(dottet_datetime.replace(".", "-"))

# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

import datetime as dt
import pathlib as pl

import click


@click.command(
    name="nvd-release-builder",
)
@click.option(
    "--date",
    type=click.DateTime(
        formats=[
            "%Y-%m-%d",
        ]
    ),
    help=(
        "Specifies the state of the database."
        " Interpreted as a date in UTC timezone."
        " If not given implies '--fetch'."
    ),
)
@click.argument(
    "FEEDS_PATH",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=False,
        path_type=pl.Path,
    ),
)
@click.option(
    "--fetch",
    is_flag=True,
    default=False,
    help="Fetch the latest changes before proceeding.",
)
@click.option(
    "--xz-preset",
    default=9,
    help="The xz compression preset level to use.",
)
@click.option(
    "--feed-name",
    default=None,
    help="The name of the feed to create. If not given, create all feeds.",
)
def cli(
    date: dt.datetime | None,
    feeds_path: pl.Path,
    fetch: bool,
    xz_preset,
    feed_name: str | None,
):
    """Creates release packages of the CVE data feeds released by FKIE-CAD [1].
    The packages are put into FEEDS_PATH.

    [1]: https://github.com/fkie-cad/nvd-json-data-feeds"""
    # Import here to avoid erroring out before click can print the help page
    try:
        from nvd_release_builder import repo
    except ValueError as e:
        raise click.ClickException(str(e))

    from nvd_release_builder import CveDatabase, Feed

    fetch |= date is None
    if feeds_path.exists() and len(list(feeds_path.iterdir())) > 0:
        raise click.ClickException(
            f"{feeds_path} exists and is not empty. Please specify a non-existing or empty directory."
        )

    if feed_name is not None and not _feed_name_is_valid(feed_name):
        raise click.ClickException(
            f"{feed_name} is not a valid --feed-name."
            " Please chose either a year after 1999, or from 'all', 'recent', or 'modified'."
        )

    feeds_path.mkdir(exist_ok=True)

    if date is None:
        # XXX Timezones and times when it is not released yet
        timestamp = dt.date.today()
    else:
        timestamp = date.date()

    if fetch:
        click.echo("Fetching repository")
        repo.fetch()

    click.echo(f"Checking out repository for timestamp {timestamp}")
    repo.checkout(timestamp)
    db = CveDatabase.from_timestamp(timestamp)

    if feed_name is None:
        _write_all_feeds(feeds_path, db, xz_preset)
    else:
        click.echo(f"Creating {feed_name} archive")
        Feed.write(
            dest_dir=feeds_path,
            db=db,
            name=feed_name,
            xz_preset=xz_preset,
        )


def _write_all_feeds(
    path: pl.Path,
    db: "nvd_release_builder.CveDatabase",  # noqa: F821
    xz_preset: int,
):
    from nvd_release_builder import Feed

    for year in range(1999, db.timestamp.year + 1):
        click.echo(f"Creating {year} archive")
        Feed.write(
            dest_dir=path,
            db=db,
            name=str(year),
            xz_preset=xz_preset,
        )

    click.echo("Creating all archive")
    Feed.write(
        dest_dir=path,
        db=db,
        name="all",
        xz_preset=xz_preset,
    )
    click.echo("Creating recent archive")
    Feed.write(
        dest_dir=path,
        db=db,
        name="recent",
        xz_preset=xz_preset,
    )
    click.echo("Creating modified archive")
    Feed.write(
        dest_dir=path,
        db=db,
        name="modified",
        xz_preset=xz_preset,
    )


def _feed_name_is_valid(name: str) -> bool:
    if name in ["all", "recent", "modified"]:
        return True

    try:
        year = int(name)
        return year >= 1999  # noqa: PLR2004
    except ValueError:
        return False


cli()

<!--
SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# fkie-cve-make-release
A script and python package to create a release of
[nvd-json-data-feeds][nvd-json-data-feeds].

After installing using [poetry][poetry] the script can be used as follows:
```
Usage: fkie-cve-make-release [OPTIONS] FEEDS_PATH

  Creates release packages of the CVE data feeds released by FKIE-CAD [1]. The
  packages are put into FEEDS_PATH.

  [1]: https://github.com/fkie-cad/nvd-json-data-feeds

Options:
  --date [%Y-%m-%d]    Specifies the state of the database. Interpreted as a
                       date in UTC timezone. If not given implies '--fetch'.
  --fetch              Fetch the latest changes before proceeding.
  --xz-preset INTEGER  The xz compression preset level to use.
  --feed-name TEXT     The name of the feed to create. If not given, create
                       all feeds.
  --help               Show this message and exit.
```

The python package exposes a single class `Feed`.
See it's methods for the package's usage.

[nvd-json-data-feeds]: https://github.com/fkie-cad/nvd-json-data-feeds
[poetry]: https://python-poetry.org/

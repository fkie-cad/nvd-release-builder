# fkie-cve-make-release
A script and python package to create a release of
[nvd-json-data-feeds][nvd-json-data-feeds].

After installing using [poetry][poetry] the script can be used as follows:
```
Usage: fkie-cve-make-release [OPTIONS] PATH

  Create a release package of the CVE datafeeds released by FKIE-CAD.

Options:
  --date [%Y-%m-%d]    Specifies the state of the database. If not given
                       implies '--fetch'
  --fetch              Fetch the latest changes from https://github.com/fkie-
                       cad/nvd-json-data-feeds
  --xz-preset INTEGER  The xz compression preset level to use.
  --feed-name TEXT     The name of the feed to create. If not given, create
                       all feeds.
  --help               Show this message and exit.

```

The python package exposes a single class `Feed`.
See it's methods for the package's usage.

[nvd-json-data-feeds]: https://github.com/fkie-cad/nvd-json-data-feeds
[poetry]: https://python-poetry.org/

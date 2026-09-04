<p align="center">
  <a href="https://www.zenodo.org">
    <img src="https://github.com/zenodo/zenodo-docs-user/raw/master/assets/static/img/logos/zenodo-black-200.png">
  </a>
</p>

# Getting Started

Zenodo user documentation uses [Lektor](https://www.getlektor.com), a powerful
static content management system.

Dependencies are managed with [uv](https://docs.astral.sh/uv/). They are
declared in `pyproject.toml` and pinned in `uv.lock`.

## Install

1. Install `uv` (see [other installation methods](https://docs.astral.sh/uv/getting-started/installation/)):

    ```console
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. From the root of the repository, create the virtual environment and install
   the pinned dependencies:

    ```console
    $ uv sync
    ```

`uv` reads `.python-version` and downloads the right Python for you, so there
is nothing else to set up.

## Run the site locally

```console
$ uv run lektor server
```

Then open [http://localhost:5000/](http://localhost:5000/) in your browser.

Prefix any command with `uv run` to execute it inside the project environment.
Alternatively, activate the environment once with `source .venv/bin/activate`
and drop the prefix.

## Run the tests

```console
$ uv run ./runtests.sh
```

## Documentation search with Pagefind

The search index needs a few extra packages, grouped under `search` in
`pyproject.toml`. Install them and build the index:

```console
$ uv sync --group search
$ uv run lektor build
$ uv run python pagefind_index.py "$(uv run lektor project-info --output-path)"
$ uv run python -m http.server --directory "$(uv run lektor project-info --output-path)"
```

Note that plain `uv sync` and `uv run` remove the `search` packages again. Pass
`--group search` to keep them installed.

## Lektor desktop application

As an alternative to the command line, download and install the desktop
application from [Lektor's website](https://www.getlektor.com/downloads/).
Launch it, then browse to `zenodo-docs-user.lektorproject` in the root folder of
the repository and open the file.

# tasky

A tiny to-do list for the command line: the example package for
**Python Pro, Module 14**.

```
tasky_project/
├── pyproject.toml        # metadata, dependencies, the `tasky` command
├── README.md
├── src/
│   └── tasky/            # the importable package
│       ├── __init__.py   # marks the folder as a package, exposes the public API
│       ├── __main__.py   # makes `python -m tasky` work
│       ├── cli.py        # argparse: turns command-line text into function calls
│       └── store.py      # the logic: load/save tasks as JSON
└── tests/
    └── test_store.py     # pytest tests (Module 16)
```

## Install it (in a virtual environment)

```bash
cd 14_packaging/tasky_project
```

```bash
python -m venv .venv
```

Activate it (Windows PowerShell: `.venv\Scripts\Activate.ps1`, macOS/Linux: `source .venv/bin/activate`), then:

```bash
pip install -e .
```

`-e` ("editable") links the install to your source folder, so code changes
apply immediately without reinstalling.

## Use it

```bash
tasky add "Record Module 14"
```

```bash
tasky list
```

```bash
tasky done 1
```

```bash
python -m tasky list
```

Tasks are stored in `tasks.json` in the current folder (set `TASKY_FILE` to change it).

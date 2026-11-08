"""Slides · Module 14 · Project structure & packaging"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 14 · Project structure &amp; packaging"
SLIDES = [
 cover("14", "Project structure &amp; packaging", "From one script to a real project: imports, virtual environments, a CLI, and pip install.",
       [("Modules, packages, import", "01_modules_and_imports.py"), ("Command-line tools", "02_cli_with_argparse.py"),
        ("pyproject, PyPI, uv, pre-commit", "03_publishing_and_tooling.md"), ("The tasky package", "tasky_project/"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Project structure", "One file doesn't scale",
     "Your script grew to <b>1,500 lines</b>. Two teammates edit it at once, nobody can test one part alone, and "
     "\"it works on my machine\" because everyone has different library versions.",
     "Split code into <b>modules and packages</b>, pin dependencies in <b>pyproject.toml</b>, and isolate them in a <b>virtual environment</b>."),

 picture(M, "Imports", "What import really does",
     "&#128218; Like a <b>library</b>: Python looks for the book on a list of shelves (<b>sys.path</b>), reads it <b>once</b>, "
     "and keeps it in a cache (<b>sys.modules</b>). The next import just hands you the cached copy.",
     [("import tasky.store", "you write this"), ("sys.modules?", "already loaded: reuse it"),
      ("search sys.path", "script folder, venv site-packages, stdlib"), ("run the file once", "then cache the module")],
     "That's why a module-level object behaves like a <b>singleton</b>."),

 trace(M, "Project structure", "A layout that every team recognises", ["Path", "What it's for"],
       [["<span class=\"m\">pyproject.toml</span>", "name, version, dependencies, tool settings (ruff, mypy, pytest)"],
        ["<span class=\"m\">src/tasky/__init__.py</span>", "makes <b>tasky</b> a package; the public API"],
        ["<span class=\"m\">src/tasky/__main__.py</span>", "lets you run <b>python -m tasky</b>"],
        ["<span class=\"m\">src/tasky/cli.py · store.py</span>", "one module per responsibility"],
        ["<span class=\"m\">tests/</span>", "pytest tests, mirroring the package"],
        ["<span class=\"m\">.venv/</span> (git-ignored)", "this project's own Python + libraries"]],
       "The <b>src/</b> layout stops tests from accidentally importing local files instead of the installed package."),

 code_out(M, "Imports", "if __name__ == \"__main__\"", '''
# tools.py
def slugify(title):
    return "-".join(title.lower().split())

if __name__ == "__main__":     # only when run directly
    print(slugify("Hello Python Pro"))

print("__name__ is", repr(__name__))''',
     steps=["Run directly: <b>__name__ == \"__main__\"</b>, so the demo runs.", "Imported: <b>__name__ == \"tools\"</b>, so it doesn't.",
            "Put scripts' entry code behind this guard."]),

 mistake(M, "Imports", "Circular imports",
     '''
# models.py
from services import send_welcome
class User: ...

# services.py
from models import User      # ImportError:
def send_welcome(u: User): ...  # partially initialised''',
     "Each module needs the other <b>while it's still loading</b>. Python finds a half-built module and fails.",
     '''
# services.py
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:            # only for type hints
    from models import User

def send_welcome(u: User): ...''',
     "Better still: move shared code into a third module, so dependencies point <b>one way</b>."),

 code_out(M, "Command-line tools", "argparse: a real CLI in 15 lines", '''
import argparse

parser = argparse.ArgumentParser(prog="tasky", description="Tiny todo app")
sub = parser.add_subparsers(dest="cmd", required=True)

add = sub.add_parser("add", help="add a task")
add.add_argument("title")
add.add_argument("--priority", type=int, choices=[1, 2, 3], default=2)

sub.add_parser("list", help="show tasks")

args = parser.parse_args(["add", "Write slides", "--priority", "1"])
print(args)
print(args.cmd, args.title, args.priority)''',
     steps=["<b>Subcommands</b> like git: <b>tasky add</b>, <b>tasky list</b>.", "<b>type=int</b> and <b>choices</b> validate input for you.",
            "<b>--help</b> is generated automatically."]),

 trace(M, "Environments and tools", "The modern Python toolbox", ["Need", "Tool", "Command"],
       [["Isolate dependencies", "venv / uv", "<span class=\"m\">python -m venv .venv</span> · <span class=\"m\">uv venv</span>"],
        ["Install the project", "pip / uv", "<span class=\"m\">pip install -e .</span> · <span class=\"m\">uv sync</span>"],
        ["Pin exact versions", "lock file", "<span class=\"m\">uv lock</span> · <span class=\"m\">pip freeze &gt; requirements.txt</span>"],
        ["Build and publish", "build + twine", "<span class=\"m\">python -m build</span> · <span class=\"m\">twine upload dist/*</span>"],
        ["Checks on every commit", "pre-commit", "<span class=\"m\">pre-commit install</span> (ruff, mypy)"]],
       "One rule: <b>never pip install into the system Python</b>. One venv per project."),

 code_out(M, "pyproject.toml", "One file describes the project", '''
print(open("pyproject.toml").read())''',
     setup='''open("pyproject.toml", "w").write("""[project]
name = "tasky"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = ["rich>=13"]

[project.scripts]
tasky = "tasky.cli:main"      # creates a 'tasky' command

[project.optional-dependencies]
dev = ["pytest", "mypy", "ruff"]
""")''',
     steps=["<b>[project.scripts]</b>: pip creates a real <b>tasky</b> command.",
            "Dev tools: <b>pip install -e \".[dev]\"</b>."]),

 job(M, "Packaging", "On day one at a new job", [
     ("Set up the project", '''
git clone ... && cd api
uv sync            # or: python -m venv .venv
                   #     pip install -e ".[dev]"'''),
     ("Run the app as a module", '''
python -m app      # uses app/__main__.py'''),
     ("Internal shared library", '''
pip install git+https://github.com/acme/
    acme-auth.git@v2.3.0'''),
     ("Admin commands", '''
python manage.py migrate   # Django CLI
typer / click for your own tools'''),
 ]),

 interview(M, "What does if __name__ == \"__main__\" do?",
     ["Every module has <b>__name__</b>. When you <b>run</b> a file it's <b>\"__main__\"</b>; when it's <b>imported</b> it's the module name.",
      "So the code under the guard runs only when the file is executed directly.",
      "Use it for demos, CLIs and scripts, so importing the module has no side effects."],
     None,
     "\"How does Python find a module when you import it?\" (sys.modules cache first, then the folders in sys.path: the script's folder, PYTHONPATH, site-packages, the stdlib)."),

 interview(M, "How do you manage dependencies in a Python project?",
     ["One <b>virtual environment</b> per project; never the system Python.",
      "Declare direct dependencies with ranges in <b>pyproject.toml</b>.",
      "<b>Lock</b> exact versions (uv.lock, poetry.lock or pip-tools) so CI and production match.",
      "Separate <b>dev</b> dependencies (pytest, mypy, ruff).",
      "Update regularly and scan for vulnerabilities (pip-audit, Dependabot)."],
     None,
     "\"What is the difference between a module and a package?\" (a module is one .py file; a package is a folder of modules, usually with __init__.py)."),

 recap(M, "Module 14 in 6 lines",
     ["Module = a .py file; package = a folder with <b>__init__.py</b>.",
      "Imports are cached in <b>sys.modules</b> and searched on <b>sys.path</b>.",
      "Guard script code with <b>if __name__ == \"__main__\"</b>.",
      "Avoid circular imports: dependencies point one way.",
      "<b>argparse</b> subcommands for CLIs; <b>[project.scripts]</b> makes a command.",
      "One <b>venv</b> per project, <b>pyproject.toml</b>, a lock file."],
     "Do <b>exercises/ex14_wordtool_cli.py</b>, then install <b>tasky</b> with <b>pip install -e .</b>"),
]

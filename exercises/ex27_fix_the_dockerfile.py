"""Exercise 27 · Fix a bad Dockerfile

exercises/ex27_Dockerfile.bad WORKS, but it's slow to rebuild, huge, insecure and
hard to operate. Copy it to exercises/ex27_Dockerfile and fix it until this
reviewer is happy. Each check is a real-world best practice from Module 27.

    python exercises/ex27_fix_the_dockerfile.py                  # reviews exercises/ex27_Dockerfile
    python exercises/ex27_fix_the_dockerfile.py path/to/Dockerfile

No Docker needed to do this exercise (but if you have it: docker build it!).
Stuck? Compare with solutions/ex27_Dockerfile
"""
import re
import sys
from pathlib import Path

CHECKS = [
    ("uses a slim, pinned Python base image (e.g. python:3.12-slim)",
     lambda d: re.search(r"^FROM\s+python:3\.\d+-slim", d, re.M) is not None),
    ("does not use the 'latest' tag",
     lambda d: ":latest" not in d and not re.search(r"^FROM\s+python\s*$", d, re.M)),
    ("copies requirements.txt and installs BEFORE copying the code (layer caching)",
     lambda d: ("requirements.txt" in d or "pyproject.toml" in d) and "pip install" in d
     and ("COPY app" not in d or d.find("pip install") < d.find("COPY app"))),
    ("pip install uses --no-cache-dir (smaller image)",
     lambda d: "--no-cache-dir" in d),
    ("runs as a non-root user (USER ...)",
     lambda d: re.search(r"^USER\s+(?!root\b)\S+", d, re.M) is not None),
    ("has no secrets baked in (no PASSWORD/SECRET/KEY values in ENV/ARG)",
     lambda d: not re.search(r"^(ENV|ARG)\s+.*(PASSWORD|SECRET|API_KEY)\s*[= ]\s*\S+", d, re.M | re.I)),
    ("has a HEALTHCHECK",
     lambda d: "HEALTHCHECK" in d),
    ("starts the server with the exec form CMD [\"...\"] and binds 0.0.0.0",
     lambda d: re.search(r'^CMD\s+\[', d, re.M) is not None and "0.0.0.0" in d),
    ("does not run in --reload / debug mode",
     lambda d: "--reload" not in d and "DEBUG=1" not in d.replace(" ", "")),
]


def review(text: str) -> list[str]:
    text = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    return [name for name, ok in CHECKS if not ok(text)]


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ex27_Dockerfile")
    if not path.exists():
        sys.exit(f"{path} not found: copy exercises/ex27_Dockerfile.bad to it first")
    problems = review(path.read_text(encoding="utf-8"))
    print(f"Reviewed {path.name}: {len(CHECKS) - len(problems)}/{len(CHECKS)} checks passed")
    for p in problems:
        print("  x", p)
    assert not problems, "fix the Dockerfile"
    print("All checks passed!")

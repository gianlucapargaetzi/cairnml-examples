"""Make a local git repository from the training code of example 2: the code you will keep private.

It copies train.py and requirements.txt of example 2 into a new folder, adds a short README and a .gitignore, and makes
the first commit. It does not touch GitHub and needs no GitHub tools: only git. Publishing the folder as a private
repository is the next step of the example README, with the GitHub command line or in the browser.

    python examples/03-private-code-and-credentials/make_private_repo.py ../cairnml-private-demo
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "02-cifar10-classification"
FILES = ["train.py", "requirements.txt"]

README = """# CairnML private demo

The CIFAR-10 training of the CairnML examples, in a private repository. A CairnML agent reads it with a GitHub App.

    pip install -r requirements.txt
    python train.py --epochs 3                 # train on this machine
    python train.py --epochs 3 --queue <queue> # queue the run for an agent, by the exact queue name in the web app
"""

GITIGNORE = """__pycache__/
*.pt
cifar10/
.venv/
"""


def git(folder: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(folder), *arguments], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", type=Path, help="the new folder; it must not exist yet, or be empty")
    args = parser.parse_args()
    folder: Path = args.folder.expanduser().resolve()

    if shutil.which("git") is None:
        print("git is not installed. Install it from https://git-scm.com and run this again.", file=sys.stderr)
        return 1
    if folder.exists() and any(folder.iterdir()):
        print(f"{folder} is not empty. Choose a new folder.", file=sys.stderr)
        return 1
    if folder == SOURCE.parent.parent or SOURCE.parent.parent in folder.parents:
        print("Choose a folder outside the examples repository: it becomes a repository of its own.", file=sys.stderr)
        return 1

    folder.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copy2(SOURCE / name, folder / name)
    (folder / "README.md").write_text(README)
    (folder / ".gitignore").write_text(GITIGNORE)

    git(folder, "init", "-q")
    git(folder, "add", ".")
    try:
        git(folder, "commit", "-q", "-m", "CIFAR-10 training from the CairnML examples")
    except subprocess.CalledProcessError:
        print("The commit failed. If git asks who you are, run:\n"
              '  git config --global user.name "Your Name"\n'
              '  git config --global user.email "you@example.com"\n'
              f"and run `git -C {folder} commit -m \"CIFAR-10 training from the CairnML examples\"`.", file=sys.stderr)
        return 1
    git(folder, "branch", "-M", "main")

    print(f"ready: {folder}")
    print("a git repository with one commit. Next: publish it as a private repository (step 2 of the README).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# git-hooks

Git hooks for formatting python, java, and golang files.

### Usage

`git clone https://github.com/mlctrez/git-hooks`

`cd git-hooks; python install.py`

The installation creates `~/.git_template/hooks/pre-commit` and sets the
git global init.templatedir to `~/.git_template`.  New and cloned git repositories
will pick up the pre-commit hook.

On a git commit, the precommit.py script executes each hook in the hooks directory.
Modify, remove, or add new python scripts in this directory and they
will be picked up the next time the pre-commit hook runs.



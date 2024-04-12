"""Make the commit message start with the current branch name."""

import argparse
import re
import subprocess
import sys
from typing import List, Optional

ALLOWED_BRANCH_PREFIXES = [
    "feature/",
    "bugfix/",
    "hotfix/",
    "feat/",
    "docs/",
    "bug/",
    "fix/",
    "refactor/",
    "style/",
    "test/",
]


def branch_name_is_valid(branch_name: str, branch_is_user_prefixed: bool = False) -> bool:
    """Check if branch name is valid.

    Parameters
    ----------
    branch_name : str
        The name of the branch.
    branch_is_user_prefixed : bool, optional
        If the branch name is prefixed with a username, by default False.

    Returns
    -------
    bool
        True if the branch name is valid, False otherwise.
    """
    prefix_regex = "|".join(ALLOWED_BRANCH_PREFIXES)
    if branch_is_user_prefixed:
        pattern = rf"^[a-z]+/{prefix_regex}/[A-Z]+-\d+"
    else:
        pattern = rf"^{prefix_regex}/[A-Z]+-\d+"

    if re.match(pattern, branch_name):
        return True
    else:
        return False


def get_branch_type(branch_name: str, branch_is_user_prefixed: bool = False) -> str:
    """Get the type of the branch.

    Parameters
    ----------
    branch_name : str
        The name of the branch.
    branch_is_user_prefixed : bool, optional
        If the branch name is prefixed with a username, by default False.

    Returns
    -------
    str
        The type of the branch.
    """
    if branch_is_user_prefixed:
        return branch_name.split("/")[1]
    else:
        return branch_name.split("/")[0]


def get_branch_context(branch_name: str, branch_is_user_prefixed: bool = False) -> str:
    """Get the context of the branch.

    Parameters
    ----------
    branch_name : str
        The name of the branch.
    branch_is_user_prefixed : bool, optional
        If the branch name is prefixed with a username, by default False.

    Returns
    -------
    str
        The context of the branch.
    """
    if branch_is_user_prefixed:
        return "".join(branch_name.split("/")[2:])
    else:
        return "".join(branch_name.split("/")[1:])


def main(argv: Optional[List] = None):
    """Add the current branch name to the commit message.

    The commit message will be prefixed with a conventional commit message friendly version
    of the current branch name.

    Parameters
    ----------
    argv : Optional[List]
        The command line arguments, by default None.

    Raises
    ------
    ValueError
        If the branch name is invalid.
    """
    parser = argparse.ArgumentParser(
        prog="commit-prefix-pre-commit",
        description="Auto Add feature Branch Name to commit message and validate branch names",
    )
    parser.add_argument(
        "--branch-is-user-prefixed",
        type=bool,
        help="If the branch name is prefixed with a username i.e. jgoesser/fix/ABC-123",
        default=False,
    )
    commit_msg_filepath = sys.argv[1]
    args = parser.parse_args(argv)
    branch_name = subprocess.check_output(
        ["git", "symbolic-ref", "--short", "HEAD"],
        text=True,
    ).strip()

    if not branch_name_is_valid(branch_name, branch_is_user_prefixed=args.branch_is_user_prefixed):
        raise ValueError(f"Branch name '{branch_name}' is invalid.")

    with open(commit_msg_filepath, "r") as file:
        commit_msg = file.read()

    with open(commit_msg_filepath, "w") as file:
        branch_type = get_branch_type(
            branch_name, branch_is_user_prefixed=args.branch_is_user_prefixed
        )
        branch_context = get_branch_context(
            branch_name, branch_is_user_prefixed=args.branch_is_user_prefixed
        )
        prefix = f"{branch_type}({branch_context})"
        if commit_msg.startswith(prefix):
            return
        else:
            file.write(f"{prefix}: {commit_msg}")


if __name__ == "__main__":
    main()

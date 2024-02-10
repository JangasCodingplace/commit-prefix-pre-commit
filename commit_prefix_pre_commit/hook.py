"""Make the commit message start with the current branch name."""

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


def branch_name_is_valid(branch_name: str) -> bool:
    """Check if branch name is valid.

    Parameters
    ----------
    branch_name : str
        The name of the branch.

    Returns
    -------
    bool
        True if the branch name is valid, False otherwise.
    """
    prefix_regex = "|".join(ALLOWED_BRANCH_PREFIXES)

    if re.match(rf"^{prefix_regex}/[A-Z]+-\d+", branch_name):
        return True
    else:
        return False


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
    print(sys.argv)
    print(sys.argv[1])
    commit_msg_filepath = sys.argv[1]
    branch_name = subprocess.check_output(
        ["git", "symbolic-ref", "--short", "HEAD"],
        text=True,
    ).strip()

    if not branch_name_is_valid(branch_name):
        raise ValueError(f"Branch name '{branch_name}' is invalid.")

    with open(commit_msg_filepath, "r") as file:
        commit_msg = file.read()

    with open(commit_msg_filepath, "w") as file:
        branch_type = branch_name.split("/")[0]
        branch_context = "".join(branch_name.split("/")[1:])
        prefix = f"{branch_type}({branch_context})"
        if commit_msg.startswith(prefix):
            return
        else:
            file.write(f"{prefix}: {commit_msg}")


if __name__ == "__main__":
    main()

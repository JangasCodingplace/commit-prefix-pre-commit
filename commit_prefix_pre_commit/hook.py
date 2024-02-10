"""Make the commit message start with the current branch name."""

import subprocess
import sys


def main(commit_msg_filepath: str):
    """Add the current branch name to the commit message.

    Parameters
    ----------
    commit_msg_filepath : str
        The file that contains the commit message.
    """
    branch_name = subprocess.check_output(
        ["git", "symbolic-ref", "--short", "HEAD"],
        text=True,
    ).strip()

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
    main(sys.argv[1])

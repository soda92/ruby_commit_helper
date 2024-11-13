import re
from colorama import Fore, Style
import subprocess


def get_changed_files():
    output = subprocess.getoutput("git status")
    files = re.findall(r"modified: *(.*)", output)
    print(files)
    return files


def check(file):
    r = subprocess.getoutput(f"rubocop {file}")
    r = r.replace("offense", "configured linter message")
    r = r.replace("Offense", "configured linter message")
    r = r.replace(
        """Inspecting 1 file
C
""",
        "",
    )
    lines = r.split("\n")
    lines = lines[3:-3]
    s = "\n".join(lines)
    s = s.replace(
        "C: Layout/EndOfLine: Carriage return character detected.", "Not a problem"
    )

    s2 = s.split("\n")
    s3 = []

    for line in s2:
        if line.endswith("Not a problem"):
            continue
        if line.startswith("# frozen_string_literal: true ..."):
            continue
        s3.append(line)

    s = "\n".join(s3).strip()
    if s == "":
        print(Fore.GREEN + "No problem found")
    else:
        print(s)
    print(Style.RESET_ALL)


def check_style():
    for file in get_changed_files():
        check(file)


def main():
    check_style()


if __name__ == "__main__":
    main()

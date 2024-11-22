import re
from rich import print
import subprocess


def get_changed_files():
    output = subprocess.getoutput("git status")
    files = re.findall(r"modified: *(.*)", output)
    files.extend(re.findall(r"new file: *(.*)", output))
    files_str = " ".join(files)
    print(f"files: [#af0087]{files_str}[/]")
    return files


def warning_print(s):
    print(s)


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
    status = 0

    for line in s2:
        if line.endswith("Not a problem"):
            continue
        if line.startswith("# frozen_string_literal: true ..."):
            continue
        if line.strip().startswith("^^^^^^"):
            continue
        s3.append(line)

    s = "\n".join(s3).strip()
    if s == "":
        pass
        # print(Fore.GREEN + "No problem found")
    else:
        warning_print(s)
        status = 1

    return status


def check_style():
    status = 0
    for file in get_changed_files():
        status += check(file)

    exit(status)


def main():
    check_style()


if __name__ == "__main__":
    main()

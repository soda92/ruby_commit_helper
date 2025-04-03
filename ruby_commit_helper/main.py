import re
import rich
import subprocess


def get_changed_files() -> list[str]:
    output = subprocess.getoutput("git status")
    files = re.findall(r"modified: *(.*)", output)
    files.extend(re.findall(r"new file: *(.*)", output))
    files_str = " ".join(files)
    rich.print(f"files: [#af0087]{files_str}[/]")
    return files


def warning_print(s):
    for line in s.split("\n"):
        try:
            rich.print(line)
        except Exception as e:
            print(line)


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
        if file.endswith(".rb"):
            status += check(file)

    exit(status)

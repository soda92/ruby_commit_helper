import re
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
    print(s)


def check_style():
    for file in get_changed_files():
        check(file)


def main():
    check_style()


if __name__ == "__main__":
    main()

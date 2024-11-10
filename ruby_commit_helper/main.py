import re
import subprocess


def get_changed_files():
    output = subprocess.getoutput("git status")
    files = re.findall(r"modified: *(.*)", output)
    print(files)
    return files


def check(file):
    print(subprocess.getoutput(f"rubocop {file}"))


def check_style():
    for file in get_changed_files():
        check(file)


def main():
    check_style()


if __name__ == "__main__":
    main()

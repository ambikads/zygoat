import os

from .shell import run
from .files import use_dir, repository_root
from zygoat.constants import Projects

pip = os.path.join("venv", "bin", "pip")
dev_file_name = "requirements.dev.txt"
prod_file_name = "requirements.txt"


def freeze():
    return run([pip, "freeze"], capture_output=True).stdout.decode().split("\n")


def packages_to_map(arr):
    result = {}

    for package_line in arr:
        if "=" not in package_line:
            continue
        package = package_line.split("=")[0]
        result[package] = package_line

    return result


def dump_dependencies(package_map, dev=False):
    file_name = dev_file_name if dev else prod_file_name

    with repository_root():
        with use_dir(Projects.BACKEND):
            with open(file_name, "w") as f:
                if dev:
                    f.write(f"-r {prod_file_name}\n")

                for name, version in package_map.items():
                    if name == "" or "=" not in version:
                        continue

                    f.write(f"{version}\n")


def install_dependency(name, dev=False):
    initialize_files()
    file_name = dev_file_name if dev else prod_file_name
    with repository_root():
        with use_dir(Projects.BACKEND):
            run([pip, "install", "--upgrade", name])
            freeze_map = packages_to_map(freeze())

            with open(file_name) as f:
                file_map = packages_to_map(f.read().split("\n"))

            file_map[name] = freeze_map[name]

            dump_dependencies(file_map, dev=dev)


def initialize_files():
    with repository_root():
        with use_dir(Projects.BACKEND):
            if not os.path.exists(prod_file_name):
                open(prod_file_name, "w").close()

            if not os.path.exists(dev_file_name):
                open(dev_file_name, "w").close()

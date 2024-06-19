import argparse
import glob
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

FUNCTION_NAME = 'ws3_telemetry_handler_1'
REQUIREMENTS_FILE = 'requirements_prod.txt'
AWS_PIP_PLATFORM = 'manylinux2014_x86_64'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layer", help="Generate a lambda layer", default=False, action='store_true')
    parser.add_argument("-a", "--app", help="Package the lambda app", default=True, action='store_true')
    parser.add_argument("-t", "--test", help="Run tests", default=False, action='store_true')
    args = parser.parse_args()

    if args.test:
        run_all_tests()

    if args.layer:
        build_lambda_layer()

    if args.app:
        build_app_package()


def copy_python_files(src_path: Path, dest_path: Path, dirname: Optional[str] = None):
    if dirname is None:
        files_list = glob.glob(os.path.join(src_path, '*.py'))
        os.makedirs(dest_path, exist_ok=True)
    else:
        files_list = glob.glob(os.path.join(src_path, dirname, '*.py'))
        os.makedirs(dest_path / dirname, exist_ok=True)

    for f in files_list:
        if dirname is None:
            shutil.copy(f, dest_path)
        else:
            shutil.copy(f, dest_path / dirname)


def build_lambda_layer():
    release_name = datetime.now().strftime(f"%Y%m%d-layer")  # TODO: add git commit
    release_path = Path(__file__) / os.pardir / 'dist' / release_name
    package_install_path = release_path / 'layer' / 'python'
    os.makedirs(package_install_path, exist_ok=True)
    requirements_file = Path(__file__) / os.pardir / os.pardir / REQUIREMENTS_FILE

    print("Copying python libraries...")
    install_requirements(package_install_path, requirements_file)

    print("Zipping everything together")
    archive = shutil.make_archive(release_path / os.pardir / release_name, 'zip',
                                  root_dir=release_path, dry_run=False)
    print(f"Layer ready for upload at {archive}")


def build_app_package():
    release_name = datetime.now().strftime(f"%Y%m%d-{FUNCTION_NAME}")  # TODO: add git commit
    release_path = Path(__file__) / os.pardir / 'dist' / release_name / 'package'
    os.makedirs(release_path, exist_ok=True)
    repo_dir = Path(__file__) / os.pardir / os.pardir

    print("Copying project files...")
    copy_python_files(repo_dir, release_path)

    print("Zipping everything together")
    archieve = shutil.make_archive(release_path / os.pardir / release_name, 'zip',
                                   root_dir=release_path, dry_run=False)

    print(f"App ready for upload at {archieve}")


def install_requirements(target_path: Path, requirements_path: Path, platform: Optional[str] = AWS_PIP_PLATFORM):
    target_path = target_path.resolve()
    requirements_path = requirements_path.resolve()

    try:
        command = (f"{sys.executable} -m pip install --platform {platform} --target={target_path} "
                   f"--implementation cp --python-version 3.12 --only-binary=:all: "
                   f"--upgrade -r {requirements_path}")
        res = subprocess.run(command, check=True)
        if res.returncode != 0:
            raise Exception(f"pip installation Failed. see \n{res.stderr}")
    except Exception as e:
        print(e)


def run_all_tests():
    tests_dir = Path(__file__) / os.pardir / os.pardir / "tests"
    retcode = pytest.main(["-x", tests_dir.resolve()])
    print(f"All tests returned {retcode.name}")


if __name__ == '__main__':
    main()

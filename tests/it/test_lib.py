# The MIT License (MIT).
#
# Copyright (c) 2023-2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

# flake8: noqa: S603, S607. Not a production code

import os
import subprocess
from collections.abc import Generator
from pathlib import Path
from shutil import copytree

import pytest
from _pytest.legacypath import TempdirFactory


@pytest.fixture(scope='module')
def current_dir() -> Path:
    """Current directory for installing actual eljson."""
    return Path().absolute()


@pytest.fixture(scope='module')
def _test_repo(tmpdir_factory: TempdirFactory, current_dir: Path) -> Generator[None, None, None]:
    """Real git repository."""
    tmp_path = tmpdir_factory.mktemp('eljson_test_dir')
    os.chdir(tmp_path)
    os.makedirs('tests')
    copytree(current_dir / 'tests', 'tests', dirs_exist_ok=True)
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)
    subprocess.run(['venv/bin/pip', 'install', 'pip', '-U'], check=True)
    subprocess.run(['venv/bin/pip', 'install', 'pytest', str(current_dir)], check=True)
    yield
    os.chdir(current_dir)


@pytest.mark.usefixtures('_test_repo')
@pytest.mark.parametrize('version', [
    ('attrs==22.2.0',),
    ('attrs', '-U'),
    ('jsonschema==0.3',),
    ('jsonschema', '-U'),
    ('jsonpath-ng==1.4.1',),
    ('jsonpath-ng', '-U'),
    ('ujson==1.19',),
    ('ujson', '-U'),
])
def test_dependency_versions(version: tuple[str]) -> None:
    """Test lib with different dependency versions."""
    subprocess.run(['venv/bin/pip', 'install', *version], check=True)
    got = subprocess.run(
        ['pytest', 'tests/unit'],
        stdout=subprocess.PIPE,
        check=False,
    )

    assert got.returncode == 0

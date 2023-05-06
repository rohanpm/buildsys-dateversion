import os
import pathlib
import subprocess
import sys

import pytest

THIS_DIR = os.path.dirname(__file__)
PROJECTS_DIR = os.path.join(THIS_DIR, "sample_projects")


def all_sample_projects():
    out = []

    for entry in os.scandir(PROJECTS_DIR):
        if entry.is_dir:
            out.append(entry.name)

    assert out, "Test setup error: cannot find sample_projects"

    return out


@pytest.fixture(params=all_sample_projects())
def sample_project(request: pytest.FixtureRequest) -> str:
    return os.path.join(PROJECTS_DIR, request.param)


def test_build(sample_project: str, tmp_path: pathlib.Path):
    # The project should build successfully
    subprocess.run(
        [
            sys.executable or "python",
            "-mbuild",
            ".",
            "--outdir",
            str(tmp_path),
        ],
        check=True,
        cwd=sample_project,
    )

    # Should have built a wheel and an sdist.
    assert len(list(tmp_path.glob("*.whl"))) == 1
    assert len(list(tmp_path.glob("*.tar.gz"))) == 1

    # TODO: more complete checks on the outputs...

from pathlib import Path

from skillpack_studio.main import main


def test_init_and_validate(tmp_path: Path) -> None:
    pack = tmp_path / "demo-skill"
    assert main(["init", str(pack)]) == 0
    assert (pack / "skillpack.json").exists()
    assert main(["validate", str(pack)]) == 0


def test_validate_missing_files(tmp_path: Path) -> None:
    assert main(["validate", str(tmp_path)]) == 1

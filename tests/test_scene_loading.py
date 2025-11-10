import pytest
from pathlib import Path


def test_scenes_yaml_exists() -> None:
    p = Path(__file__).resolve().parents[1] / "config" / "scenes.yaml"
    assert p.exists(), f"Expected scenes.yaml at {p}"


def test_load_samples_parse() -> None:
    # Basic YAML parse smoke test
    import yaml
    p = Path(__file__).resolve().parents[1] / "config" / "scenes.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert "scenes" in data

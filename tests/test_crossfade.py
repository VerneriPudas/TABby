import pytest


def test_crossfade_not_implemented():
    # The scaffold's crossfade raises NotImplementedError
    from src.core.audio_engine import AudioEngine, Track

    engine = AudioEngine()
    t1 = Track(path="a.wav")
    t2 = Track(path="b.wav")
    with pytest.raises(NotImplementedError):
        engine.crossfade(t1, t2, duration=1.0)

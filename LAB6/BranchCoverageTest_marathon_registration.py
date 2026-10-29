import pytest

from marathon_registration import (
    entry_fee,
    start_wave,
    finisher_status
)


# ==========================================
# 1. BRANCH COVERAGE FOR entry_fee()
# ==========================================

def test_unknown_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("invalid", 30, False, False)


def test_age_below_12():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_age_12_boundary():
    assert entry_fee("5k", 12, False, False) == 500


def test_underage_half_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)


def test_underage_full_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


def test_age_18_can_enter_half_marathon():
    assert entry_fee("half", 18, False, False) == 1200


def test_early_bird_true():
    assert entry_fee("10k", 30, True, False) == 600


def test_early_bird_false():
    assert entry_fee("10k", 30, False, False) == 800


def test_senior_discount_true():
    assert entry_fee("10k", 65, False, False) == 400


def test_senior_discount_false():
    assert entry_fee("10k", 64, False, False) == 800


def test_tshirt_true():
    assert entry_fee("5k", 30, False, True) == 800


def test_tshirt_false():
    assert entry_fee("5k", 30, False, False) == 500


# ==========================================
# 2. BRANCH COVERAGE FOR start_wave()
# ==========================================

def test_missing_finish_time():
    assert start_wave(None, "full") == "D"


def test_full_race_wave_a():
    assert start_wave(180, "full") == "A"


def test_full_race_wave_b():
    assert start_wave(200, "full") == "B"


def test_full_race_wave_c():
    assert start_wave(241, "full") == "C"


def test_non_full_race_wave_a():
    assert start_wave(90, "10k") == "A"


def test_non_full_race_wave_b():
    assert start_wave(100, "10k") == "B"


def test_non_full_race_wave_c():
    assert start_wave(121, "10k") == "C"


def test_full_race_exact_cutoff():
    assert start_wave(240, "full") == "B"


def test_non_full_race_exact_cutoff():
    assert start_wave(120, "10k") == "B"


# ==========================================
# 3. BRANCH COVERAGE FOR finisher_status()
# ==========================================

def test_missed_checkpoint_disqualification():
    assert finisher_status(100, "10k", 1) == "DSQ"


def test_no_missed_checkpoints():
    assert finisher_status(80, "10k", 0) == "finisher"


def test_full_marathon_within_limit():
    assert finisher_status(360, "full", 0) == "finisher"


def test_full_marathon_over_limit():
    assert finisher_status(361, "full", 0) == "DNF"


def test_half_marathon_within_limit():
    assert finisher_status(180, "half", 0) == "finisher"


def test_half_marathon_over_limit():
    assert finisher_status(181, "half", 0) == "DNF"


def test_other_race_within_limit():
    assert finisher_status(90, "10k", 0) == "finisher"


def test_other_race_over_limit():
    assert finisher_status(91, "10k", 0) == "DNF"


def test_disqualification_takes_priority():
    assert finisher_status(400, "full", 2) == "DSQ"


import pytest

from marathon_registration import (
    entry_fee,
    start_wave,
    finisher_status
)


# --------------------------------------------------
# Tests for entry_fee()
# --------------------------------------------------

def test_entry_fee_standard_10k():
    assert entry_fee("10k", 30, False, False) == 800


def test_entry_fee_unknown_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("invalid", 30, False, False)


def test_entry_fee_age_below_12():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_entry_fee_underage_half_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 16, False, False)


def test_entry_fee_underage_full_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


def test_entry_fee_age_12_allowed():
    assert entry_fee("5k", 12, False, False) == 500


def test_entry_fee_age_65_discount():
    assert entry_fee("10k", 65, False, False) == 400


def test_entry_fee_early_bird_discount():
    assert entry_fee("10k", 30, True, False) == 600


def test_entry_fee_tshirt_addition():
    assert entry_fee("5k", 30, False, True) == 800


def test_entry_fee_all_adjustments():
    # 1800 - 25% early-bird discount = 1350
    # Senior discount: 1350 // 2 = 675
    # T-shirt: 675 + 300 = 975
    assert entry_fee("full", 65, True, True) == 975


# --------------------------------------------------
# Tests for start_wave()
# --------------------------------------------------

def test_start_wave_missing_time():
    assert start_wave(None, "full") == "D"


def test_start_wave_full_fast_runner():
    assert start_wave(180, "full") == "A"


def test_start_wave_full_medium_runner():
    assert start_wave(200, "full") == "B"


def test_start_wave_full_slow_runner():
    assert start_wave(241, "full") == "C"


def test_start_wave_non_full_fast_runner():
    assert start_wave(90, "10k") == "A"


def test_start_wave_non_full_medium_runner():
    assert start_wave(100, "10k") == "B"


def test_start_wave_non_full_slow_runner():
    assert start_wave(121, "10k") == "C"


def test_start_wave_exact_full_cutoff():
    assert start_wave(240, "full") == "B"


# --------------------------------------------------
# Tests for finisher_status()
# --------------------------------------------------

def test_finisher_disqualified_for_missed_checkpoint():
    assert finisher_status(100, "10k", 1) == "DSQ"


def test_finisher_full_marathon_within_limit():
    assert finisher_status(360, "full", 0) == "finisher"


def test_finisher_full_marathon_over_limit():
    assert finisher_status(361, "full", 0) == "DNF"


def test_finisher_half_marathon_within_limit():
    assert finisher_status(180, "half", 0) == "finisher"


def test_finisher_half_marathon_over_limit():
    assert finisher_status(181, "half", 0) == "DNF"


def test_finisher_other_race_within_limit():
    assert finisher_status(90, "10k", 0) == "finisher"


def test_finisher_other_race_over_limit():
    assert finisher_status(91, "10k", 0) == "DNF"


def test_finisher_missed_checkpoint_takes_priority():
    assert finisher_status(500, "full", 1) == "DSQ"
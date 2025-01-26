from lib.ntpclock import NTPClock
from unittest.mock import patch
import pytest

@pytest.fixture()
def mock_ticks_ms():
  with patch("time.ticks_ms", create=True, return_value=101010) as mocked_func:
    yield mocked_func

def test_top_of_second(mock_ticks_ms):
  # Given
  clock = NTPClock(12345, 10, 0)
  local_ms = 100000
  wallclock_ms = 10

  # When
  new_ms = clock.top_of_second(local_ms, wallclock_ms)

  # Then
  assert new_ms == (local_ms - wallclock_ms)

def test_top_of_second_wrap(mock_ticks_ms):
  # Given
  clock = NTPClock(12345, 10, 0)
  local_ms = 10
  wallclock_ms = 100

  # When
  new_ms = clock.top_of_second(local_ms, wallclock_ms)

  # Then
  assert new_ms == 1073741734

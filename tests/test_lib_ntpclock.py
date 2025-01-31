from lib.ntpclock import NTPClock
from unittest.mock import patch
import pytest

@pytest.fixture()
def mock_ticks_ms():
  with patch("time.ticks_ms", create=True, return_value=101010) as mocked_func:
    yield mocked_func

@pytest.fixture()
def mock_ticks_add():
  with patch("time.ticks_add", create=True, return_value=101000) as mocked_func:
    yield mocked_func

def test_top_of_second(mock_ticks_add):
  # Given
  clock = NTPClock(101010, 12345, 10, 0)
  local_ms = 101010
  wallclock_ms = 10

  # When
  new_ms = clock.top_of_second(local_ms, wallclock_ms)

  # Then
  assert new_ms == (local_ms - wallclock_ms)

@pytest.mark.skip(reason="requires micropython platform implementation")
def test_top_of_second_wrap(mock_ticks_ms):
  # Given
  clock = NTPClock(101010, 12345, 10, 0)
  local_ms = 10
  wallclock_ms = 100

  # When
  new_ms = clock.top_of_second(local_ms, wallclock_ms)

  # Then
  assert new_ms == 1073741734

def test_timestamps_regression(mock_ticks_add):
  # Given
  timestamps = [ 
    # ntp seconds, ntp ms, tx ms, rx ms
    [1737375531, 557.620, 8243952, 8243952+23],
    [1737375595, 997.857, 8308392, 8308392+18],
    [1737375661, 0.623, 8373394, 8373394+20],
    [1737375725, 998.878, 8438393, 8438393+20],
    [1737375791, 14.136, 8503407, 8503407+25],
    [1737375856, 5.647, 8568398, 8568398+26],
    [1737375921, 0.665, 8633393, 8633393+21],
    [1737375985, 997.686, 8698390, 8698390+18],
    [1737376051, 35.928, 8763428, 8763428+21],
    [1737376115, 999.762, 8828391, 8828391+20],
  ]
  clock = NTPClock(101010, 12345, 10, 0)

  # When
  (beta, alpha) = clock.timestamps_regression(timestamps)

  # Then
  assert abs(beta - 5.874e-06) < 1e-9
  assert abs(alpha - 12.3) < 0.1
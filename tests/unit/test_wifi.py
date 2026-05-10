from subway_server.core.locator import WifiSample
from subway_server.core.wifi import MISSING_RSSI, normalize_wifi


def _s(bssid: str, rssi: int) -> WifiSample:
    return WifiSample(bssid=bssid, rssi=rssi)


def test_normalize_respects_bssid_order():
    samples = [_s("bb", -70), _s("aa", -50), _s("cc", -60)]
    order = ["aa", "bb", "cc"]
    assert normalize_wifi(samples, order) == [-50, -70, -60]


def test_normalize_fills_missing_with_minus_100():
    samples = [_s("aa", -50)]
    order = ["aa", "bb", "cc"]
    assert normalize_wifi(samples, order) == [-50, MISSING_RSSI, MISSING_RSSI]


def test_normalize_empty_input_returns_all_minus_100():
    assert normalize_wifi([], ["aa", "bb"]) == [MISSING_RSSI, MISSING_RSSI]


def test_normalize_extra_bssids_dropped():
    samples = [_s("aa", -50), _s("zz", -99)]
    order = ["aa", "bb"]
    assert normalize_wifi(samples, order) == [-50, MISSING_RSSI]


def test_normalize_output_length_equals_order_length():
    order = ["a", "b", "c", "d", "e"]
    result = normalize_wifi([_s("a", -1)], order)
    assert len(result) == len(order)


def test_missing_rssi_constant_is_minus_100():
    # Pinned by the docs §5.2.2 / §4.2.4.
    assert MISSING_RSSI == -100

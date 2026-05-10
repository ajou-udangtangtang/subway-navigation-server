from .locator import WifiSample


MISSING_RSSI = -100


def normalize_wifi(samples: list[WifiSample], bssid_order: list[str]) -> list[int]:
    """Project samples onto the canonical bssid_order vector.

    - Missing AP (in order but not in samples) → MISSING_RSSI (-100).
    - Extra AP (in samples but not in order) → dropped.
    - Output length always equals len(bssid_order).
    """
    by_bssid = {s.bssid: s.rssi for s in samples}
    return [by_bssid.get(bssid, MISSING_RSSI) for bssid in bssid_order]

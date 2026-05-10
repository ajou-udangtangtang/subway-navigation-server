"""Stub for Team B's fingerprint repository.

Contract:
    list_bssid_order() -> list[str]
        Returns BSSIDs in the canonical order used to build training vectors.
        Must be stable across calls (same DB state → same order).

    load_training_set() -> list[tuple[str, list[int]]]
        Returns (node_id, rssi_vector) pairs. The rssi_vector length must
        equal len(list_bssid_order()), with -100 for samples missing an AP.
"""


class FingerprintRepository:
    def list_bssid_order(self) -> list[str]:
        raise NotImplementedError(
            "Team B: implement against the fingerprint table. "
            "See CLAUDE.md 'Team B integration boundary'."
        )

    def load_training_set(self) -> list[tuple[str, list[int]]]:
        raise NotImplementedError(
            "Team B: implement against the fingerprint table. "
            "Order must match list_bssid_order(); fill missing with -100."
        )

import pytest

from config import TestConfig
from subway_server import create_app
from subway_server.core import locator


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app
    # Reset estimator after each test so cross-test state is impossible.
    locator.register_estimator(locator._stub_estimator)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def fake_estimator():
    """Inject a deterministic LocationEstimator for the duration of a test.

    Usage:
        def test_locate(client, fake_estimator):
            fake_estimator("B")
            res = client.post("/locate", json={"wifi": [...]})
            assert res.json == {"node": "B"}
    """
    def _set(node_id: str):
        locator.register_estimator(lambda samples: node_id)

    return _set

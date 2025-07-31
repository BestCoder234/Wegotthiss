import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_data(monkeypatch):
    # Monkey‑patch the DB session to return a known dataset
    from routers.screener import Session, Fundamental, PriceEOD
    class DummyRow:
        def __init__(self, symbol, pe, pb, close, eps, book_value):
            self.symbol = symbol
            self.pe = pe
            self.pb = pb
            self.close = close
            self.eps = eps
            self.book_value = book_value
        def _asdict(self):
            return self.__dict__

    class DummyResult:
        def __init__(self, data):
            self.data = data
        def all(self):
            return self.data

    def dummy_exec(stmt):
        return DummyResult([DummyRow("TCS", 20.0, 3.5, 2600.0, 130.0, 750.0)])

    monkeypatch.setattr(Session, "exec", lambda self, stmt: dummy_exec(stmt))

def test_screener_defaults():
    response = client.get("/screener")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data and data[0]["symbol"] == "TCS"

def test_screener_filters():
    response = client.get("/screener?pe=25&pb=5")
    assert response.status_code == 200
    data = response.json()
    # Our dummy row has pe=20, pb=3.5 so it should pass filter pe<=25,pb<=5
    assert data and data[0]["symbol"] == "TCS" 
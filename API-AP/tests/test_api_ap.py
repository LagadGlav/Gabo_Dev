import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from API_AP import *


@pytest.fixture
def client():
    """Client de test Flask"""
    with app.test_client() as client:
        yield client

# -----------------------
# Mocks utilitaires
# -----------------------

class FakeCursor:
    def __init__(self, data=None):
        self._data = data or []
        self._index = 0

    def execute(self, query, params=None):
        pass

    def fetchone(self):
        if isinstance(self._data, list):
            return self._data[0] if self._data else None
        return self._data

    def fetchall(self):
        return self._data

    def close(self):
        pass


class FakeConnection:
    def __init__(self, data=None):
        self._data = data

    def cursor(self, dictionary=False, prepared=False):
        return FakeCursor(self._data)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


# -----------------------
# Tests
# -----------------------

def test_save_player_success(monkeypatch, client):
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection())
    monkeypatch.setattr("app.send_to_database_j", lambda pid, pname: True)
    monkeypatch.setattr("app.patch_mapping_index", lambda pid, pname: True)
    monkeypatch.setattr("app.indexbyname", {})
    monkeypatch.setattr("app.id", 1)

    resp = client.post("/api-ap/save_player", json={"playername": "Alice"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["data"]["name"] == "Alice"


def test_save_player_missing_name(client):
    resp = client.post("/api-ap/save_player", json={})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_get_player_info_found(monkeypatch, client):
    fake_data = {"joueur_id": 1, "joueur_nom": "Alice"}
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection(fake_data))

    resp = client.get("/api-ap/get_player_info?playerId=1")
    assert resp.status_code == 200
    assert resp.get_json()["joueur_nom"] == "Alice"


def test_get_player_info_not_found(monkeypatch, client):
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection(None))

    resp = client.get("/api-ap/get_player_info?playerId=99")
    assert resp.status_code == 404


def test_get_all_players_success(monkeypatch, client):
    fake_players = [{"joueur_id": 1, "joueur_nom": "Alice", "elo": 1500}]
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection(fake_players))

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_get_all_players_not_found(monkeypatch, client):
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection(None))
    monkeypatch.setattr("app.get_all_players", lambda: None)

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 404


def test_last_ten_games_no_games(monkeypatch, client):
    # Première requête : aucune partie trouvée
    monkeypatch.setattr("app.get_connexion", lambda: FakeConnection([]))

    resp = client.get("/api-ap/player/1/last-games")
    assert resp.status_code == 200
    assert resp.get_json() == {}


def test_last_ten_games_with_data(monkeypatch, client):
    # Première requête : IDs de parties
    first_conn = FakeConnection([{"partie_id": 1}, {"partie_id": 2}])
    # Deuxième requête : données jointes
    joined_data = [
        {"partie_id": 1, "joueur_nom": "Alice"},
        {"partie_id": 2, "joueur_nom": "Alice"}
    ]
    calls = [first_conn, FakeConnection(joined_data)]

    def fake_get_connexion():
        return calls.pop(0)

    monkeypatch.setattr("app.get_connexion", fake_get_connexion)

    resp = client.get("/api-ap/player/1/last-games")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "1" in map(str, data.keys())


def test_ready_endpoint_success(monkeypatch, client):
    monkeypatch.setattr("app.connect_to_database_interro", lambda: True)
    monkeypatch.setattr("app.get_nb_players_in_db", lambda: {"MAX(joueur_id)": 1})
    monkeypatch.setattr("app.build_index_byname", lambda: {"Alice": 1})

    resp = client.get("/ready")
    assert resp.status_code == 200
    assert "ready" in resp.get_json()["message"].lower()

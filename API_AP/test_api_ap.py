import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from API_AP.api_ap import app
from API_AP import api_ap

@pytest.fixture
def client():
    """Client test Flask"""
    with app.test_client() as client:
        yield client

@pytest.fixture
def num_players():
    return 4

class FakeConnection:
    def __init__(self, return_value=None):
        self.return_value = return_value

    def cursor(self, **kwargs):
        return self

    def execute(self, *args, **kwargs):
        pass

    def fetchone(self):
        return self.return_value if isinstance(self.return_value, dict) else None

    def fetchall(self):
        return self.return_value if isinstance(self.return_value, list) else None

    def close(self):
        pass


# --- TESTS EXISTANTS ADAPTÉS ---

def test_save_player_success(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection())
    monkeypatch.setattr(api_ap, "send_to_database_j", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "patch_mapping_index", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "indexbyname", {})
    monkeypatch.setattr(api_ap, "id", 1)

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
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection(fake_data))

    resp = client.get("/api-ap/get_player_info?playerId=1")
    assert resp.status_code == 200
    assert resp.get_json()["joueur_nom"] == "Alice"


def test_get_player_info_not_found(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection(None))

    resp = client.get("/api-ap/get_player_info?playerId=99")
    assert resp.status_code == 404


def test_get_all_players_success(monkeypatch, client):
    fake_players = [{"joueur_id": 1, "joueur_nom": "Alice", "elo": 1500}]
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection(fake_players))

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_get_all_players_not_found(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection(None))
    monkeypatch.setattr(api_ap, "get_all_players", lambda: None)

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 404


def test_last_ten_games_no_games(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection([]))

    resp = client.get("/api-ap/player/1/last-games")
    assert resp.status_code == 200
    assert resp.get_json() == {}


def test_last_ten_games_with_data(monkeypatch, client):
    first_conn = FakeConnection([{"partie_id": 1}, {"partie_id": 2}])
    joined_data = [
        {"partie_id": 1, "joueur_nom": "Alice"},
        {"partie_id": 2, "joueur_nom": "Alice"}
    ]
    calls = [first_conn, FakeConnection(joined_data)]

    def fake_get_connexion():
        return calls.pop(0)

    monkeypatch.setattr(api_ap, "get_connexion", fake_get_connexion)

    resp = client.get("/api-ap/player/1/last-games")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "1" in map(str, data.keys())


def test_ready_endpoint_success(monkeypatch, client):
    monkeypatch.setattr(api_ap, "connect_to_database_interro", lambda: True)
    monkeypatch.setattr(api_ap, "get_nb_players_in_db", lambda: {"MAX(joueur_id)": 1})
    monkeypatch.setattr(api_ap, "build_index_byname", lambda: {"Alice": 1})

    resp = client.get("/ready")
    assert resp.status_code == 200
    assert "ready" in resp.get_json()["message"].lower()


# --- TESTS INJECTION SQL ---

@pytest.mark.parametrize("payload", [
    {"playername": "Robert'); DROP TABLE joueurs;--"},
    {"playername": "' OR '1'='1"},
    {"playername": "Alice; DELETE FROM joueurs WHERE 'a'='a"}
])
def test_sql_injection_save_player(monkeypatch, client, payload):
    """
    Vérifie que l'API ne casse pas ou n'exécute pas de SQL malveillant.
    """
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection())
    monkeypatch.setattr(api_ap, "send_to_database_j", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "patch_mapping_index", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "indexbyname", {})
    monkeypatch.setattr(api_ap, "id", 1)

    resp = client.post("/api-ap/save_player", json=payload)
    # On attend un code 201 si l'API échappe correctement les entrées
    # ou un 400 si elle les rejette
    assert resp.status_code in (201, 400)


@pytest.mark.parametrize("malicious_id", [
    "1 OR 1=1",
    "1; DROP TABLE joueurs;--",
    "'; UPDATE joueurs SET elo=9999 WHERE 'a'='a"
])
def test_sql_injection_get_player_info(monkeypatch, client, malicious_id):
    """
    Vérifie que l'API ne retourne pas toutes les données ou ne plante pas
    avec un ID malveillant.
    """
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeConnection(None))

    resp = client.get(f"/api-ap/get_player_info?playerId={malicious_id}")
    # On attend un 404 ou un 400, mais pas un dump massif de données
    assert resp.status_code in (400, 404)
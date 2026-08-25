import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from API_AP.api_ap import app
from API_AP import api_ap


@pytest.fixture
def client():
    """Client de test Flask"""
    with app.test_client() as client:
        yield client


class FakeMySQLCursor:
    """Simule un curseur MySQL avec support des options dictionary/prepared."""
    def __init__(self, data=None):
        self._data = data or []
    def execute(self, *args, **kwargs):
        pass
    def fetchone(self):
        return self._data[0] if self._data else None
    def fetchall(self):
        return self._data
    def close(self):
        pass

class FakeMySQLConnection:
    """Simule une connexion MySQL compatible avec mysql.connector.connect()."""
    def __init__(self, data=None):
        self._data = data
    def cursor(self, *args, **kwargs):
        return FakeMySQLCursor(self._data)
    def commit(self):
        pass
    def rollback(self):
        pass
    def close(self):
        pass

@pytest.fixture
def mysql_conn_with_table():
    """
    Simule une base MySQL avec la table Joueurs et une donnée initiale.
    """
    table = [{"joueur_id": 1, "joueur_nom": "Initial"}]
    conn = FakeMySQLConnection(table)
    conn._table_data = table
    return conn


def test_save_player_success(monkeypatch, client, mysql_conn_with_table):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: mysql_conn_with_table)
    monkeypatch.setattr(api_ap, "patch_mapping_index", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "indexbyname", {})
    monkeypatch.setattr(api_ap, "id", 2)

    resp = client.post("/api-ap/save_player", json={"playername": "Alice"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["data"]["name"] == "Alice"


def test_save_player_missing_name(client):
    resp = client.post("/api-ap/save_player", json={})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_get_player_info_found(monkeypatch, client):
    fake_data = [{"joueur_id": 1, "joueur_nom": "Alice"}]
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeMySQLConnection(fake_data))

    resp = client.get("/api-ap/get_player_info?playerId=1")
    assert resp.status_code == 200
    assert resp.get_json()["joueur_nom"] == "Alice"


def test_get_player_info_not_found(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeMySQLConnection([]))

    resp = client.get("/api-ap/get_player_info?playerId=99")
    assert resp.status_code == 404


def test_get_all_players_success(monkeypatch, client):
    fake_players = [{"joueur_id": 1, "joueur_nom": "Alice", "elo": 1500}]
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeMySQLConnection(fake_players))

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)
    assert resp.get_json()[0]["joueur_nom"] == "Alice"


def test_get_all_players_not_found(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeMySQLConnection([]))
    monkeypatch.setattr(api_ap, "get_all_players", lambda: None)

    resp = client.get("/api-ap/get_all_players")
    assert resp.status_code == 404


def test_last_ten_games_no_games(monkeypatch, client):
    monkeypatch.setattr(api_ap, "get_connexion", lambda: FakeMySQLConnection([]))

    resp = client.get("/api-ap/player/1/last-games")
    assert resp.status_code == 200
    assert resp.get_json() == {}


def test_last_ten_games_with_data(monkeypatch, client):
    first_conn = FakeMySQLConnection([{"partie_id": 1}, {"partie_id": 2}])
    second_conn = FakeMySQLConnection([
        {"partie_id": 1, "joueur_nom": "Alice"},
        {"partie_id": 2, "joueur_nom": "Alice"}
    ])
    calls = [first_conn, second_conn]
    monkeypatch.setattr(api_ap, "get_connexion", lambda: calls.pop(0))

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


@pytest.mark.parametrize("payload", [
    {"playername": "Robert'); DROP TABLE Joueurs;--"},
    {"playername": "' OR '1'='1"},
    {"playername": "Alice; DELETE FROM Joueurs WHERE 'a'='a"}
])
def test_sql_injection_save_player(monkeypatch, client, mysql_conn_with_table, payload):
    """
    Vérifie que l'API échappe ou rejette les entrées malveillantes
    et que la table/données restent intactes.
    """
    monkeypatch.setattr(api_ap, "get_connexion", lambda: mysql_conn_with_table)
    monkeypatch.setattr(api_ap, "patch_mapping_index", lambda pid, pname: True)
    monkeypatch.setattr(api_ap, "indexbyname", {})
    monkeypatch.setattr(api_ap, "id", 2)

    resp = client.post("/api-ap/save_player", json=payload)
    assert resp.status_code in (201, 400)

    assert any(r["joueur_nom"] == "Initial" for r in mysql_conn_with_table._table_data)


@pytest.mark.parametrize("malicious_id", [
    "1 OR 1=1",
    "1; DROP TABLE Joueurs;--",
    "'; UPDATE Joueurs SET elo=9999 WHERE 'a'='a"
])
def test_sql_injection_get_player_info(monkeypatch, client, mysql_conn_with_table, malicious_id):
    """
    Vérifie que l'API ne fuit pas de données et ne casse pas la table
    avec un ID malveillant.
    """
    monkeypatch.setattr(api_ap, "get_connexion", lambda: mysql_conn_with_table)

    resp = client.get(f"/api-ap/get_player_info?playerId={malicious_id}")
    assert resp.status_code in (400, 404)

    assert any(r["joueur_nom"] == "Initial" for r in mysql_conn_with_table._table_data)

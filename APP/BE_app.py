from webbrowser import Error

from flask import Flask, render_template, request, jsonify
from threading import Lock

lock = Lock()

import time
import mysql.connector
import mysql.connector.pooling

app = Flask(__name__, template_folder='Front_End/html', static_folder='Front_End')


def get_connection():
    connection = mysql.connector.connect(
        host="data_base",
        user="root",
        password="Gabo",
        database="Gabo_base"
    )
    return connection


class game:
    def __init__(self, id_game,nb_joueurs, id_joueur, score, rang):
        self.score = score
        self.id_game = id_game
        self.nb_joueurs = nb_joueurs
        self.id_joueur = id_joueur
        self.rang = rang
    def __str__(self):
        return f"Partie({[(self.id_game, self.nb_joueurs, self.id_joueur, self.score, self.rang)]})"

class queue:
    def __init__(self):
        self.queue = []

    def add_queue(self, partie):
        self.queue.append(partie)

    def empty_queue(self):
        app.logger.info(self.display())
        with lock:
            if self.queue:
                for i in range(len(self.queue)):
                        p = self.queue[0]
                        self.queue.pop(0)
                        try:
                            send_to_database(p)
                        except Error as e:
                            raise f"Erreur MySQL : {str(e)}"

            else:
                return None
        app.logger.info(self.display())
        return True


    def display(self):
        return [str(obj) for obj in self.queue]


def send_to_database(p):
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Partie (partie_id, nombre_joueur, joueur_id, joueur_score, rang)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (p.id_game, p.nb_joueurs, p.id_joueur, p.score, p.rang)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        connection.rollback()
        app.logger.error(f"Erreur MySQL : {str(e)}")
        raise f"Erreur MySQL : {str(e)}"
    finally:
        if connection:
            connection.close()

    return True

def send_to_database_j(id_joueur, nom):
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Joueurs (joueur_id, joueur_nom)
            VALUES (%s, %s)
        """
        data = (id_joueur, nom)
        cursor.execute(query, data)
        connection.commit()
        app.logger.info(f"Joueur inséré : ID={id_joueur}, Nom={nom}")
    except Error as e:
        connection.rollback()
        app.logger.error(f"Erreur MySQL : {str(e)}")
        raise f"Erreur MySQL : {str(e)}"
    finally:
        if connection:
            connection.close()

    return True


def connect_to_database_interro():
    """Function to establish in case of disconnectin  a connection to the MySQL database.
    Retries the connection up to 10 times with a 1-second delay between attempts."""

    connection = None
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host="data_base",
                user="root",
                password="Gabo",
                database="Gabo_base"
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as e:
            raise Exception(f"Attempt connexion Data_Base {e}/10")

        time.sleep(1)
    raise Exception("Impossible to connect to the database after several attempts")


@app.route('/')
def index():
    time.sleep(1)
    return render_template("Chtml.html")

def sort_table(table):
    # Tri par insertion
    n = len(table[1])
    try:
        for i in range(1, n):
            cle = table[1][i]
            cle_valeur = table[0][i]  # Sauvegarde de la première ligne associée
            j = i - 1
            while j >= 0 and table[1][j] > cle:
                table[1][j + 1] = table[1][j]  # Décale la deuxième ligne
                table[0][j + 1] = table[0][j]  # Décale la première ligne associée
                j -= 1
            table[1][j + 1] = cle
            table[0][j + 1] = cle_valeur
        return table
    except Error as e:
        raise f"Error sorting table : {e}"

def format_table(table):
    table = table[0]

    table = [list(map(int, item.replace(',', '').split())) for item in table]

    id = table[0][0]
    nb_joueurs = table[1][0]

    table = sort_table(table)

    for i in range(1, len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        rang = i
        p_received = game(id, nb_joueurs, id_joueur, score, rang)
        with lock:
            try:
                Q.add_queue(p_received)
            except Error as e:
                raise f"Error add to queue : {e}"
    app.logger.info(Q.display())
    em = Q.empty_queue()
    table = get_all_players()
    app.logger.info(table)
    return em

def get_all_players():
    """Récupère toutes les lignes de la table 'joueurs' depuis MySQL."""
    app.logger.info("Load joueurs done")
    connection = None
    try:
        # Obtenir une connexion depuis le pool
        connection = get_connection()
        cursor = connection.cursor()

        # Requête pour récupérer toutes les lignes
        query = "SELECT * FROM Joueurs"
        cursor.execute(query)
        rows = cursor.fetchall()  # Récupère toutes les lignes

        if rows == None:
            return []

        # Afficher les résultats
        for row in rows:
            app.logger.info(row)  # Vous pouvez traiter chaque ligne ici
        return rows
    except Error as e:
        app.logger.info(f"Erreur lors de la récupération des données : {e}")
        return []
    finally:
        if connection:
            connection.close()  # Libère la connexion

@app.route('/save_table', methods=['POST'])
def receive_table():
    if get_all_players() == []:
        send_to_database_j(14, "Marco")
        send_to_database_j(15, "Gerveur")
        send_to_database_j(198, "Andrée")

    data = request.json
    app.logger.info("Connecting...")

    app.logger.info("Réussie")

    get_all_players()

    data = request.json
    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    format_table(table)
    return jsonify({"message": "Table received"}), 200

if __name__ == "__main__":
    time.sleep(5)
    Q = queue()
    connexion = connect_to_database_interro()


    app.run(host='0.0.0.0', port=80, debug=True)





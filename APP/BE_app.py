from flask import Flask, render_template, request, jsonify
from threading import Lock

lock = Lock()

import time
import mysql.connector

app = Flask(__name__, template_folder='Front_End/html', static_folder='Front_End')

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="pool",
    pool_size=5,
    host="data_base",
    user="root",
    password="Gabo",
    database="Gabo_base"
)

def get_connection():
    return connection_pool.get_connection()


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

    def queue_management(self):
        with lock:
            if self.queue:
                p = self.queue[0]
                self.queue.pop(0)
                return p
            else:
                return None

    def display(self):
        return [str(obj) for obj in self.queue]



def send_to_database(p):
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Partie (id_partie, nombre_joueurs, joueur_id, joueur_score, rang)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (p.id_game, p.nbjoueur, p.id_joueurs, p.score, p.rang)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        connection.rollback()
        app.logger.error(f"Erreur MySQL : {str(e)}")
        return jsonify({"error": "Database error"}), 500
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

    app.logger.info("Connecting...")
    connect_to_database_interro()

    app.logger.info("Réussie")

    return render_template("Chtml.html")


@app.route('/save_table', methods=['POST'])
def receive_table():


    data = request.json
    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    app.logger.info(data)
    table = table[0]


    table = [list(map(int, item.replace(',', '').split())) for item in table]

    id = table[0][0]
    nb_joueurs = table[1][0]

    n = len(table[1])
    # Tri par insertion
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

    table_sorted = table
    app.logger.info(table_sorted)

    for i in range(1, len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        rang = i
        p_received = game(table[0][0], table[1][0], id_joueur, score, rang)
        with lock:
            Q.add_queue(p_received)

    return jsonify({"message": "Table received"}), 200


    

if __name__ == "__main__":
    Q = queue()
    app.run(host='0.0.0.0', port=80, debug=True)



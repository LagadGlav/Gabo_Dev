from flask import Flask, render_template, request, jsonify

import time
import mysql.connector
from mysql.connector import connect

app = Flask(__name__, template_folder='Front_End/html', static_folder='Front_End')

saved_tables = []

class game:
    def __init__(self, id_game, table):
        self.table = table
        self.id_game = id_game

class queue:
    def __init__(self):
        self.queue = [[]]

    def add_queue(self, partie):
        self.queue.append(partie)
        app.logger.debug(f"Queue: {[(g.id_game, g.table) if isinstance(g, game) else g for g in self.queue]}")


def connect_to_database():
    """Function to establish a connection to the MySQL database.
    Retries the connection up to 10 times with a 5-second delay between attempts."""

    connection = None
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host="data_base",  # Nom du service défini dans docker-compose
                user="root",
                password="Gabo",  # Mot de passe défini dans MYSQL_ROOT_PASSWORD
                database="Gabo_base"
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as e:  # Remplacez `Error` par le module correct
            app.logger.info(f"Connection_failed{attempt}")
            time.sleep(5)  # Attente de 5 secondes (comme dans le docstring)

    raise Exception("Impossible to connect to the database after several attempts")


@app.route('/')
def index():
    time.sleep(1)

    app.logger.info("Connecting...")
    connect_to_database()

    app.logger.info("Réussie")

    return render_template("Chtml.html")


@app.route('/save_table', methods=['POST'])
def receive_table():
    app.logger.info("received table")

    data = request.json
    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    n = len(table[0])//2
    table = [table[0][:n], table[0][n:]]
    app.logger.info(table)
    id = table[0][0][0]
    p_receive = game(id, table)
    Q.add_queue(p_receive)
    return jsonify({"message": "Table received"}), 200

    

if __name__ == "__main__":
    Q = queue()
    app.run(host='0.0.0.0', port=80, debug=True)



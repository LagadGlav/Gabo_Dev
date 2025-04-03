from webbrowser import Error
import logging
from Front_End.blueprints.main import main_bp

from flask import Flask, render_template, request, jsonify
from threading import Lock

import datetime
import os, sys

lock = Lock()

import time
import mysql.connector
import mysql.connector.pooling

app = Flask(__name__, template_folder='Front_End/templates', static_folder='Front_End/static')

app.register_blueprint(main_bp)

# Configure le logger pour qu'il affiche les messages INFO (et plus)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app.logger.setLevel(logging.INFO)
app.logger.propagate = True  # Permet de faire remonter les messages au logger parent (par ex. Gunicorn)


def get_connection():
    connection = mysql.connector.connect(
        host="data_base",
        user="root",
        password="Gabo",
        database="Gabo_base"
    )
    return connection

class Game:
    def __init__(self, id_game,nb_joueurs, id_joueur, score, rang, var_elo):
        self.score = score
        self.id_game = id_game
        self.nb_joueurs = nb_joueurs
        self.id_joueur = id_joueur
        self.rang = rang
        self.var_elo = var_elo
    def __str__(self):
        return f"Partie in queue({[(self.id_game, self.nb_joueurs, self.id_joueur, self.score, self.rang)]})"

class Queue:
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
            INSERT INTO Partie (partie_id, nombre_joueur, joueur_id, joueur_score, rang, car_elo)
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

@app.route('/get_player_info')
def get_player_info():
    player_id = request.args.get('playerId')
    app.logger.info(f"Recherche Joueur : {player_id}")
    connection = mysql.connector.connect(
        host="data_base",
        user="root",
        password="Gabo",
        database="Gabo_base"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.close()
    connection.close()

    if player:
        app.logger.info(player)
        return jsonify(player)
    else:
        return jsonify({'error': 'Joueur non trouvé'}), 404



@app.route('/save_player', methods=['POST'])
def save_player():
    data = request.json
    if not data or 'playerId' not in data or 'playername' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    playerId = data['playerId']
    playername = data['playername']
    app.logger.info(f"Nouveau Joueur : {playerId}")
    app.logger.info(f"Nouveau Joueur : {playername}")

    try:
        # Simulez l'enregistrement dans la base de données
        send_to_database_j(playerId, playername)
        return jsonify({
            'message': 'Votre profil a été enregistré',
            'variables': [playerId, playername]  # Renvoyer la liste des variables
        }), 200
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': 'Id déjà pris'}), 404




def get_all_players():
    """Récupère toutes les lignes de la table 'joueurs' depuis MySQL."""
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


def format_table(table):

    app.logger.info(table)
    table = sort_table(table)
    app.logger.info(f"Sorted : {table}")
    return table

def get_var_elo(table):
    elo = table[2]
    var_elo = [0] * len(elo)
    for i in range(len(elo)-1):
        for j in range(i+1,len(elo)):
            var_elo[i] += (j-i)*(int(table[1][j])-int(table[1][i]))*(abs(elo[j]-elo[i])/elo[i])
            var_elo[j] += -var_elo[i]
            app.logger.info(var_elo[i])
            app.logger.info(var_elo[j])
            app.logger.info(var_elo)
    app.logger.info(f"Var Elo : {var_elo}")
    return var_elo


id = 2
def insertion(table):
    global id
    var_elo = get_var_elo(table)
    for i in range(0, len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        nb_joueurs = len(table[0])
        rang = i+1
        var_elo = var_elo[i]
        p_received = Game(id, nb_joueurs, id_joueur, score, rang, var_elo)
        id += 1
        with lock:
            try:
                Q.add_queue(p_received)
            except Error as e:
                raise f"Error add to queue : {e}"
    Q.display()
    return True

def sort_table(table):
    # Tri par insertion
    n = len(table[1])
    table[1] = [int(score) for score in table[1]]

    try:
        for i in range(1, n):
            cle = table[1][i]
            cle_valeur1 = table[0][i]  # Sauvegarde de la première ligne associée
            cle_valeur2 = table[2][i]  # Sauvegarde de la troisième ligne associée
            j = i - 1
            while j >= 0 and table[1][j] > cle:
                app.logger.info(f"Tri : {table[1][j]} > {cle}")
                table[1][j + 1] = table[1][j]  # Décale la deuxième ligne
                table[0][j + 1] = table[0][j]  # Décale la première ligne associée
                table[2][j + 1] = table[2][j]  # Décale la troisième ligne associée
                j -= 1
            table[1][j + 1] = cle
            table[0][j + 1] = cle_valeur1
            table[2][j + 1] = cle_valeur2
        return table
    except Error as e:
        raise f"Error sorting table : {e}"

@app.route('/save_table', methods=['POST'])
def receive_table():
    data = request.json

    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    app.logger.info("Réussie")
    app.logger.info(table)

    table = format_table(table)

    val = insertion(table)
    Q.empty_queue()
    if val:
        return jsonify({"message": "Game received and stored"}), 200
    else:
        return jsonify({"message": "Unable to store the game"}), 400


is_ready = False
@app.route('/ready', methods=['GET'])
def notify_ready():
    global is_ready
    is_ready = True

    app.logger.info("Notification reçue : Backup terminé et base de données opérationnelle.")

    app.logger.info("Startup...")

    try:
        start_up()
    except:
        app.logger.info("Start up failed")

    get_all_players()
    app.logger.info("Start up successed : App is ready")
    return "App is ready", 200

Q = Queue()
def start_up():
    time.sleep(1)
    connexion = connect_to_database_interro()
    app.logger.info("Connected")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)





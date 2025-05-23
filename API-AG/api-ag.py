from flask import Flask, jsonify, request
import logging
import time
import sys
from webbrowser import Error
from threading import Lock  # To ensure thread-safe operations

import time  # For time-related operations (not explicitly used here)
import mysql.connector  # MySQL library for database connection and operations
import mysql.connector.pooling  # Pooling for optimized connections
import math  # Math utilities (not explicitly used here)


import datetime  # Useful for date-related operations (not used in this code but available)
import os, sys  # OS-level operations for file paths or environmental variables

# Initialize threading lock for thread-safe operations
lock = Lock()


sys.path.append("/utils")
from util import connect_to_database_interro, get_connexion  # Exemple : Import de tes fonctions utilitaires
from exceptions import DatabaseError, NetworkError, StartUpError

# Configuration de Flask
app = Flask(__name__)


# Configure logging to capture INFO-level logs for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)  # Set logging level to INFO
app.logger.propagate = True  # Allow logs to propagate to parent logger

# Global state
is_ready = False

# Class to manage a queue of game sessions
class Queue:
    """
    Manages a queue of game sessions and operations on it.

    Attributes:
        queue (list): A list of Game objects waiting to be processed.

    Methods:
        add_queue(partie): Adds a Game object to the queue.
        empty_queue(): Processes all items in the queue. For each game session, the data is inserted into the MySQL database. Uses a threading lock to ensure operations are thread-safe.
        display(): Returns a list of string representations of the Game objects in the queue.
    """
    def __init__(self):
        self.queue = []  # Initialize an empty queue

    def add_queue(self, partie):
        # Add a Game object to the queue
        self.queue.append(partie)

    def empty_queue(self):
        """
        Processes all items in the queue and inserts them into the database.
        Thread-safe operation using Lock to prevent race conditions.
        """
        with lock:  # Ensure thread-safe operations
            if self.queue:  # Check if the queue is not empty
                for i in range(len(self.queue)):
                    app.logger.info(self.display())  # Log the current queue state
                    p = self.queue[0]  # Take the first element from the queue
                    self.queue.pop(0)  # Remove the first element from the queue
                    try:
                        send_to_database(p)  # Insert game session data into the database
                    except Error as e:  # Catch MySQL errors
                        raise f"Erreur MySQL : {str(e)}"  # Raise the error

            else:
                return None  # If the queue is empty, return None
        return True  # Return True if successful

    def display(self):
        """
        Returns:
            list: String representations of all Game objects in the queue.
        """
        return [str(obj) for obj in self.queue]

# Class representing a game session
class Game:
    """
    Represents a game session with relevant properties.

    Attributes:
        id_game (int): The unique ID of the game session.
        nb_joueurs (int): Number of players in the game session.
        id_joueur (int): ID of the player involved in the game session.
        score (int): The player's score for the game.
        rang (int): The player's ranking within the game session.
        var_elo (float): Variation in the player's ELO rating after the game.

    Methods:
        __str__: Returns a formatted string describing the game instance in the queue.
    """
    def __init__(self, id_game, nb_joueurs, id_joueur, score, rang, var_elo):
        self.score = score  # Player's score in the game
        self.id_game = id_game  # Game session ID
        self.nb_joueurs = nb_joueurs  # Total number of players in the game
        self.id_joueur = id_joueur  # ID of the player participating
        self.rang = rang  # Player's rank in the game
        self.var_elo = var_elo  # ELO variation due to the game

    def __str__(self):
        # Custom string representation of the game instance
        return f"Partie in queue({[(self.id_game, self.nb_joueurs, self.id_joueur, self.score, self.rang, self.var_elo)]})"


# Function to insert game data into the database
def send_to_database(p):
    """
    Inserts game session data into the `Partie` table in the MySQL database.

    Args:
        p (Game):
            A Game object containing data about the session (game ID, player details, score, rank, and ELO variation).

    Raises:
        Error: If a MySQL error occurs during query execution.

    Returns:
        bool: True if the insertion is successful.
    """
    connection = None  # Initialize connection variable
    try:
        connection = get_connexion()  # Get database connection
        cursor = connection.cursor()  # Create a cursor for executing queries

        # SQL query for inserting game session data
        query = """
            INSERT INTO Partie (partie_id, nombre_joueur, joueur_id, joueur_score, rang, var_elo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Prepare data for the query
        data = (p.id_game, p.nb_joueurs, p.id_joueur, p.score, p.rang, p.var_elo)
        cursor.execute(query, data)  # Execute the query with the data
        connection.commit()  # Commit the transaction
    except Error as e:  # Handle MySQL errors
        connection.rollback()  # Rollback in case of error
        app.logger.error(f"Erreur MySQL : {str(e)}")  # Log the error
        raise f"Erreur MySQL : {str(e)}"  # Raise the error
    finally:
        if connection:  # Close the connection if it exists
            connection.close()

    return True  # Return True if successful

@app.route('/api-ag/get_player_info')
def get_player_info():
    """
    Retrieve information about a player from the database using either the player's ID or the player's name.

    Returns:
        JSON: Player details if found, or an error message if not found.
    """
    player = request.args.get('playerId') # Get the playerId/Name parameter from the request
    app.logger.info(f"Nouveau joueur dans la partie: {player}")
    
    try:
        player_id = int(player)
    except ValueError as e:
        app.logger.info("Searching by name in the indexbyname")
        player_id = indexbyname[player]
    except:
        return jsonify({'error': 'Joueur non trouvé'}), 404  # Return an error if not found

    app.logger.info(f"Recherche Joueur : {player_id}")

    connection = get_connexion()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.close()
    connection.close()

    if player:
        return jsonify(player)  # Return player data as JSON
    else:
        return jsonify({'error': 'Joueur non trouvé'}), 404  # Return an error if not found

indexbyname: dict = {}
def get_all_players():
    """
    Establish a hasmap of all players registered allowing to match Name and Id

    Returns:
        list: List of player rows if found, otherwise an empty list.
    """
    app.logger.info(f"Generating new index table...")
    connection = None
    try:
        # Get a connection from the pool
        connection = get_connexion()
        cursor = connection.cursor()

        # Query to fetch all rows from 'Joueurs'
        query = "SELECT joueur_id, joueur_nom FROM Joueurs"
        cursor.execute(query)
        rows = cursor.fetchall()  # Fetch all rows

        if rows is None:
            return []  # Return an empty list if no data found

    except Error as e:
        app.logger.info(f"Erreur lors de la récupération des données : {e}")
        return []  # Handle any errors gracefully

    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use

    for player in rows:
        indexbyname[f"{player[1]}"] = player[0]

    app.logger.info(f"New index table {indexbyname}")
    return rows


def calculate_elo(current_elo, opponent_elo, score_diff, result, k=1):
    """
    Calculate the Elo rating variation based on the given parameters.

    Args:
        current_elo (int): Current Elo rating of the player.
        opponent_elo (int): Opponent's Elo rating.
        score_diff (int): Difference in scores.
        result (float): Game result (1 for win, 0 for loss, 0.5 for draw).
        k (int): Adjustment factor (default: 1).

    Returns:
        float: Elo rating variation.
    """
    # Calculate the expected result based on Elo formula
    expected_result = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))

    # Handle edge case where score_diff is zero (indicating a draw)
    if score_diff == 0:
        result = 0.5
        var_elo = k * ((result - expected_result) * score_diff)  # Elo adjustment for draw
        return var_elo

    # Elo adjustment based on score difference and result
    var_elo = k * score_diff * (result - expected_result)
    return var_elo


def get_var_elo(table):
    """
    Compute Elo variations for all players in a given table.

    Args:
        table (list): Table containing player IDs, scores, and Elo ratings.

    Returns:
        list: List of Elo variations for each player.
    """
    elo = table[2]
    var_elo = [0] * len(elo)  # Initialize Elo variations to zero
    for i in range(len(elo) - 1):
        for j in range(i + 1, len(elo)):
            if j != i:
                current_elo = elo[i]
                opponent_elo = elo[j]
                score_diff = abs(table[1][i] - table[1][j])

                # Update Elo variations based on game result
                var_elo[i] += calculate_elo(current_elo, opponent_elo, score_diff, 1)
                var_elo[j] += calculate_elo(current_elo, opponent_elo, score_diff, 0)
    return var_elo


def insertion(table, id_temp):
    """
    Insert players and game data into a queue for processing.

    Args:
        :param table: Table containing player IDs, scores, and Elo ratings.
        :param id_temp: Id of the game
    Returns:
        bool: True if insertion is successful, otherwise raises an error.
    """
    var_elo = get_var_elo(table)  # Compute Elo variations

    for i in range(0, len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        nb_joueurs = len(table[0])  # Total number of players
        rang = i + 1  # Rank based on score
        var_elo_ = math.floor(var_elo[i] / 10)  # Adjust Elo variation
        p_received = Game(id_temp, nb_joueurs, id_joueur, score, rang, var_elo_)

        with lock:  # Ensure thread-safe access to the queue
            try:
                Q.add_queue(p_received)
            except Error as e:
                raise f"Error add to queue : {e}"  # Handle queue insertion error

    return True


def sort_table(table):
    """
    Sort the player table based on scores using insertion sort.

    Args:
        table (list): Table containing player data.

    Returns:
        list: Sorted table.

    Raises:
        Error: If sorting fails.
    """
    n = len(table[1])
    table[1] = [int(score) for score in table[1]]  # Convert scores to integers

    try:
        for i in range(1, n):
            cle = table[1][i]  # Current score
            cle_valeur1 = table[0][i]  # Associated player ID
            cle_valeur2 = table[2][i]  # Associated Elo rating

            j = i - 1
            # Perform insertion sort
            while j >= 0 and table[1][j] > cle:
                app.logger.info(f"Tri : {table[1][j]} > {cle}")
                table[1][j + 1] = table[1][j]
                table[0][j + 1] = table[0][j]
                table[2][j + 1] = table[2][j]
                j -= 1

            table[1][j + 1] = cle
            table[0][j + 1] = cle_valeur1
            table[2][j + 1] = cle_valeur2

        return table
    except Error as e:
        raise f"Error sorting table : {e}"


@app.route('/api-ag/save_table', methods=['POST'])
def receive_table():
    """
    Process and save a player table received via POST request.

    Returns:
        JSON: Success or error message depending on the result.
    """
    global id
    id_temp = -1
    with lock:
        try:
            id += 1  # Ensure thread-safe access to the global ID variable
            id_temp = id
        except:
            app.logger.error(f"Erreur calcul id_partie")

    data = request.json  # Parse JSON data from the request

    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    table = sort_table(table)  # Sort the table
    val = insertion(table, id_temp)  # Insert data into the queue
    Q.empty_queue()  # Clear the queue

    if val:
        return jsonify({"message": "Game received and stored"}), 200
    else:
        return jsonify({"message": "Unable to store the game"}), 400


@app.route('/ready', methods=['GET'])
def notify_ready():
    """
    Notified that the app is ready and service start up can process.

    Returns:
        str: Success message indicating readiness.
    """
    global is_ready
    is_ready = True

    app.logger.info("Notification reçue : Backup terminé et base de données opérationnelle.")

    app.logger.info("Startup...")

    try:
        start_up()
    except:
        app.logger.info("Start up failed")

    get_all_players()  # Load player data from the database
    app.logger.info("Start up succeeded : App is ready")
    return "App is ready", 200

@app.route('/reload_indexbyname', methods=['GET'])
def reload_mapping():
    """
    Notified that the app is ready and service start up can process.

    Returns:
        str: Success message indicating readiness.
    """
    app.logger.info("Notification reçue : Nouveau joueur ajouté dans la base de données.")

    app.logger.info("Reloading name mapping...")

    try:
        get_all_players()
    except:
        app.logger.info("Reload failed !")
        return

    app.logger.info("Realoding succeeded")
    return "Reload succeeded ready", 200


def get_nb_partie():
    """
    Retrieve the maximum game ID from the database.

    Returns:
        int: Maximum game ID if found, otherwise returns 1.
    """
    connection = mysql.connector.connect(
        host="data_base",
        user="root",
        password="Gabo",
        database="Gabo_base"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT MAX(partie_id) FROM Partie")
    id = cursor.fetchone()
    cursor.close()
    connection.close()

    if id:
        pass
    else:
        id = 1

    return id

Q = Queue()
id = 0
def start_up():
    """
    Initialize the application and set up the database connection.
    """
    global id
    time.sleep(1)

    app.logger.info("Connecting to database...")
    try:
        connect_to_database_interro()  # Establish connection
        app.logger.info("Connected")
    except:
        app.logger.info("Impossible to connect, start_up phase failed")
        raise DatabaseError("Connexion failed.")

    id = get_nb_partie()  # Retrieve maximum game ID
    id = id['MAX(partie_id)'] + 1

    app.logger.info(f"Nombre de partie dans la base : {id}")


# Entry point for the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


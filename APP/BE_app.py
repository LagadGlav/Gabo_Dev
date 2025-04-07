# Import necessary modules

from webbrowser import Error  #
import logging  # For logging purposes
from Front_End.blueprints.main import main_bp  # Importing blueprints for modular routing

from flask import Flask, render_template, request, jsonify  # Flask and utilities for HTTP handling
from threading import Lock  # To ensure thread-safe operations

import datetime  # Useful for date-related operations (not used in this code but available)
import os, sys  # OS-level operations for file paths or environmental variables

# Initialize threading lock for thread-safe operations
lock = Lock()

import time  # For time-related operations (not explicitly used here)
import mysql.connector  # MySQL library for database connection and operations
import mysql.connector.pooling  # Pooling for optimized connections
import math  # Math utilities (not explicitly used here)

# Flask application setup
app = Flask(__name__, template_folder='Front_End/templates', static_folder='Front_End/static')  # Initialize Flask app with folder configurations

# Register the main blueprint for modular routing
app.register_blueprint(main_bp)

# Configure logging to capture INFO-level logs for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)  # Set logging level to INFO
app.logger.propagate = True  # Allow logs to propagate to parent logger

# Function to establish a connection to the MySQL database
def get_connection():
    """
    Establishes a connection to the MySQL database.
    Returns:
        connection (mysql.connector.connection.MySQLConnection):
            A MySQL connection object configured with host, user, password, and database details.
    """
    # Create a new connection with hardcoded database settings (not ideal for production)
    connection = mysql.connector.connect(
        host="data_base",  # Host name (container or server)
        user="root",  # Username for MySQL
        password="Gabo",  # Password for MySQL
        database="Gabo_base"  # Database name
    )
    return connection  # Return the connection object

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
        connection = get_connection()  # Get database connection
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

# Function to insert player data into the database
def send_to_database_j(id_joueur, nom):
    """
    Inserts player data into the `Joueurs` table in the MySQL database.

    Args:
        id_joueur (int): Unique identifier for the player.
        nom (str): Name of the player.

    Raises:
        Error: If a MySQL error occurs during query execution.

    Returns:
        bool: True if the insertion is successful.
    """
    connection = None  # Initialize connection variable
    try:
        connection = get_connection()  # Get database connection
        cursor = connection.cursor()  # Create a cursor for executing queries

        # SQL query for inserting player data
        query = """
            INSERT INTO Joueurs (joueur_id, joueur_nom)
            VALUES (%s, %s)
        """
        # Prepare data for the query
        data = (id_joueur, nom)
        cursor.execute(query, data)  # Execute the query with the data
        connection.commit()  # Commit the transaction
        app.logger.info(f"Joueur inséré : ID={id_joueur}, Nom={nom}")  # Log the successful insertion
    except Error as e:  # Handle MySQL errors
        connection.rollback()  # Rollback in case of error
        app.logger.error(f"Erreur MySQL : {str(e)}")  # Log the error
        raise f"Erreur MySQL : {str(e)}"  # Raise the error
    finally:
        if connection:  # Close the connection if it exists
            connection.close()

    return True  # Return True if successful


def connect_to_database_interro():
    """
    Establish a connection to the MySQL database, retrying up to 10 times in case of disconnection.

    Returns:
        connection: MySQL database connection object if successful.

    Raises:
        Exception: If unable to connect after the maximum number of retries.
    """
    connection = None
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host="data_base",  # Database host
                user="root",  # Database username
                password="Gabo",  # Password for the database
                database="Gabo_base"  # Target database name
            )
            if connection.is_connected():  # Check if the connection is active
                return connection
        except mysql.connector.Error as e:
            # Log the connection attempt failure
            raise Exception(f"Attempt connexion Data_Base {e}/10")

        # Wait for 1 second before retrying
        time.sleep(1)
    # Raise exception if all attempts fail
    raise Exception("Impossible to connect to the database after several attempts")


@app.route('/get_player_info')
def get_player_info():
    """
    Retrieve information about a player from the database using the player's ID.

    Returns:
        JSON: Player details if found, or an error message if not found.
    """
    player_id = request.args.get('playerId')  # Get the playerId parameter from the request
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
        return jsonify(player)  # Return player data as JSON
    else:
        return jsonify({'error': 'Joueur non trouvé'}), 404  # Return an error if not found


@app.route('/save_player', methods=['POST'])
def save_player():
    """
    Save a new player to the database.

    Returns:
        JSON: Success message if the operation is successful, or error message if there are issues.
    """
    data = request.json  # Parse JSON data from the request
    if not data or 'playerId' not in data or 'playername' not in data:
        return jsonify({'error': 'Invalid data'}), 400  # Validate input data

    playerId = data['playerId']
    playername = data['playername']
    app.logger.info(f"Nouveau Joueur : {playername} ({playerId})")

    try:
        # Try saving the player to the database
        send_to_database_j(playerId, playername)
        return jsonify({
            'message': 'Votre profil a été enregistré',  # Profile saved successfully
            'variables': [playerId, playername]  # Send back player details
        }), 200
    except Exception as e:
        app.logger.error(e)  # Log error if saving fails
        return jsonify({'error': 'Id déjà pris'}), 404  # ID already exists




def get_all_players():
    """
    Retrieve all rows from the 'Joueurs' table in MySQL.

    Returns:
        list: List of player rows if found, otherwise an empty list.
    """
    connection = None
    try:
        # Get a connection from the pool
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch all rows from 'Joueurs'
        query = "SELECT * FROM Joueurs"
        cursor.execute(query)
        rows = cursor.fetchall()  # Fetch all rows

        if rows is None:
            return []  # Return an empty list if no data found
        return rows

    except Error as e:
        app.logger.info(f"Erreur lors de la récupération des données : {e}")
        return []  # Handle any errors gracefully

    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use


def calculate_elo(current_elo, opponent_elo, score_diff, result, k=12):
    """
    Calculate the Elo rating variation based on the given parameters.

    Args:
        current_elo (int): Current Elo rating of the player.
        opponent_elo (int): Opponent's Elo rating.
        score_diff (int): Difference in scores.
        result (float): Game result (1 for win, 0 for loss, 0.5 for draw).
        k (int): Adjustment factor (default: 12).

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
    var_elo = score_diff * (result - expected_result)
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


def insertion(table):
    """
    Insert players and game data into a queue for processing.

    Args:
        table (list): Table containing player IDs, scores, and Elo ratings.

    Returns:
        bool: True if insertion is successful, otherwise raises an error.
    """
    global id  # Global game ID variable
    var_elo = get_var_elo(table)  # Compute Elo variations

    for i in range(0, len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        nb_joueurs = len(table[0])  # Total number of players
        rang = i + 1  # Rank based on score
        var_elo_ = math.floor(var_elo[i] / 10)  # Adjust Elo variation
        p_received = Game(id, nb_joueurs, id_joueur, score, rang, var_elo_)

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


@app.route('/save_table', methods=['POST'])
def receive_table():
    """
    Process and save a player table received via POST request.

    Returns:
        JSON: Success or error message depending on the result.
    """
    global id
    with lock:
        try:
            id += 1  # Ensure thread-safe access to the global ID variable
        except:
            app.logger.error(f"Erreur calcul id_partie")

    data = request.json  # Parse JSON data from the request

    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    table = sort_table(table)  # Sort the table
    val = insertion(table)  # Insert data into the queue
    Q.empty_queue()  # Clear the queue

    if val:
        return jsonify({"message": "Game received and stored"}), 200
    else:
        return jsonify({"message": "Unable to store the game"}), 400


@app.route('/ready', methods=['GET'])
def notify_ready():
    """
    Notify that the application is ready and start up processes.

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
    connexion = connect_to_database_interro()  # Establish connection
    app.logger.info("Connected")

    id = get_nb_partie()  # Retrieve maximum game ID
    id = id['MAX(partie_id)'] + 1

    app.logger.info(f"Nombre de partie dans la base : {id}")


# Entry point for the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)






from flask import Flask, jsonify, request
import logging
import time
import sys
from webbrowser import Error
from threading import Lock  # To ensure thread-safe operations

import time  # For time-related operations
import mysql.connector  # MySQL library for database connection and operations
import mysql.connector.pooling  # Pooling for optimized connections
import math  # Math utilities

import os, sys  # OS-level operations for file paths or environmental variables

# Initialize threading lock for thread-safe operations
lock = Lock()


from utils.util import connect_to_database_interro, get_connexion
from utils.exceptions import DatabaseError, StartUpError

# Configuration de Flask
app = Flask(__name__)

# Configure logging to capture INFO-level logs for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)  # Set the logging level to INFO
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
        Removes all elements from the queue and processes them. This method ensures thread-safe execution
        by using a lock and sequentially processes the elements in the queue. Each element is logged
        and then sent to the database. If the queue is empty, the method returns None.

        :param self: The instance of the class containing the queue to be processed.
        :return: Returns True if all elements in the queue are successfully processed, otherwise returns None.
        :rtype: Bool or None
        :raises Exception: Raises an exception in case of any MySQL error triggering during database operations.
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
    Retrieve player information based on a given player ID or name.

    This function handles requests to retrieve details of a player stored in the
    database. The function identifies the player by their `playerId`, either
    directly as an integer or by resolving their name from an indexing structure.
    If the player exists in the database, their data is returned as a JSON object.
    Otherwise, an error message is returned with a 404 status code.

    :param flask.Request.args['playerId']: The unique identifier or name of the
        player to search for.
    :type flask.Request.args['playerId']: str

    :raises ValueError: If the provided input is not convertible to an integer and
        does not match any player name in the indexing structure.
    :raises KeyError: If the player's name cannot be resolved in the
        `indexbyname` dictionary.

    :return: The data of the requested player in JSON format if they exist in the
        database; otherwise returns an error message and a 404 status code.
    :rtype: flask.Response
    """
    player = request.args.get('playerId') # Get the playerId/Name parameter from the request
    app.logger.info(f"Nouveau joueur dans la partie: {player}")
    
    try:
        player_id = int(player)
    except ValueError as e: # Handle a search by name
        app.logger.info("Searching by name in the indexbyname")
        player_id = indexbyname[player]
    except:
        return jsonify({'error': 'Player maybe not load, please try searching by id'}), 400  # Return an error if not found

    app.logger.info(f"Searching Joueur : {player_id}")

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
    Fetches all rows from the 'Joueurs' table and generates an index mapping player names
    to their respective IDs. The main purpose is to handle searcing player by name.
    Dictionary python is actually C-hard code, making passing throughout keys particularly fast.
    This Dictionary allows to SELECT in the db without using WHERE that could slow th request.

    This function retrieves all player records from the database, populates an in-memory
    index table based on player names and their IDs, and returns the list of all rows fetched.

    :raises Error: If an error occurs during database operations.
    :returns: List of tuples where each tuple contains player ID and player name.
    :rtype: list
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
    Calculates the variations in Elo ratings for a list of players based on their
    current ratings and game results. The function iterates through each pair of
    players in the game, compares their scores, and updates their Elo variations
    accordingly.

    :param table: A list where:
                  - table[2] represents a list of Elo ratings for each player.
                  - table[1] represents a list of scores for each player.
    :type table: list
    :return: A list representing the calculated Elo variations for each player.
             Each element corresponds to a player's total variation in Elo due to
             all game results.
    :rtype: list
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
    Insert player data into a queue based on game results and Elo rating calculations.

    This function is designed to process a table of game results and insert the
    processed data for each player into a queue. The function calculates the Elo
    rating variations for each player, organizes the data using a specific game
    structure, and ensures thread-safe queue insertion. It returns a confirmation
    status upon successful execution.

    :param table: Two-dimensional list containing player IDs and scores,
        where `table[0]` is the list of player IDs and `table[1]` is the list
        of corresponding scores.
    :type table: list
    :param id_temp: Identifier for the game instance being processed.
    :type id_temp: int
    :return: Boolean indicating whether the insertion process was successul.
    :rtype: bool
    :raises Error: If an issue occurs during the queue insertion process.
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
    Sorts a given table of data using insertion sort. The input ``table`` is expected
    to contain three rows: player IDs, their scores, and their Elo ratings. The function
    sorts the rows in ascending order with respect to the scores.
    The purpose is to get the rank of each player without having to transport this specific
    information from the front end.

    :param table: A 2D list where:
                  - table[0]: List of player IDs.
                  - table[1]: List of player scores to be used as a sorting key.
                  - table[2]: List of player Elo ratings.
    :type table: list[list[Any]]
    :return: The sorted table, ordered by ascending player scores.
    :rtype: list[list[Any]]
    :raises TypeError: If the input table is not a list or its subelements are not lists.
    :raises ValueError: If player scores (table[1]) contain non-integer values.

    """
    n = len(table[1])

    try:
        table[1] = [int(score) for score in table[1]]  # Convert scores to integers
    except ValueError as e:
        return f"Error scores aren't integers : {e}"

    try:
        for i in range(1, n):
            key = table[1][i]  # Current score
            key_value1 = table[0][i]  # Associated player ID
            key_value2 = table[2][i]  # Associated Elo rating

            j = i - 1
            # Perform insertion sort
            while j >= 0 and table[1][j] > key:
                app.logger.info(f"Tri : {table[1][j]} > {key}")
                table[1][j + 1] = table[1][j]
                table[0][j + 1] = table[0][j]
                table[2][j + 1] = table[2][j]
                j -= 1

            table[1][j + 1] = key
            table[0][j + 1] = key_value1
            table[2][j + 1] = key_value2

        return table
    except Error as e:
        raise f"Error sorting table : {e}"


@app.route('/api-ag/save_table', methods=['POST'])
def receive_table():
    """
    Receives a table corresponding to the game's information and scores
    through a POST request, processes it by sorting and storing in
    a queue, and clears the queue afterwards. Ensures thread-safe handling of a global ID.

    This endpoint is part of the API to handle game data storage. It expects a JSON
    object in the request body with a key `"table"` containing a list. The table is
    processed, stored, and an appropriate response is generated based on the success
    of the operation.

    :raises KeyError: If the 'table' key is missing in the input data
    :raises TypeError: If the value corresponding to 'table' is not a list
    :param request: The HTTP request object containing the JSON data
    :returns: A JSON response with a success or error message
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
    Sets the application status to ready and initializes startup procedures.

    This endpoint is part of the app's readiness lifecycle. When accessed,
    it performs a series of tasks to confirm that the application is ready
    for operation, such as flagging the readiness status, logging progress,
    executing startup routines, and initializing required application data.

    :raises Exception: if the startup process fails during execution
    :return: A tuple containing a string message indicating readiness and an
             HTTP status code 200
    :rtype: tuple[str, int]
    """
    global is_ready
    is_ready = True
    app.logger.info("Notification from Backup service receiveid : DataBase ready.")

    app.logger.info("Service starting...")
    try:
        start_up()
    except StartUpError as e:
        app.logger.error(f"Error du starting : {e}")
        return jsonify({"message": "Start up failed"}), 500

    app.logger.info("Service started. Ready to serve requests.")
    return jsonify({"message": "API-AP is ready"}), 200

@app.route('/patch_mapping_index', methods=['PATCH'])
def patch_mapping_index():

    data = request.get_json()
    if not data or "id" not  in data or "name" not in data:
        app.logger.error(f"Error patch mapping index: {data}")
        return jsonify({"error": "Invalid input: 'id' and 'name' keys are missing"}), 400

    indexbyname[f"{data['name']}"] = data['id']
    app.logger.info(f"New index table patched {indexbyname}")
    return jsonify({"message": "Mapping updated"}), 200

@app.route('/reload_indexbyname', methods=['GET'])
def reload_mapping():
    """
    Handles the reloading of player name mapping when a new player is added to
    the database. Logs the results of the operation to indicate success or failure.

    :return: A tuple containing a success message as a string and the HTTP status
             code 200 if the operation succeeds, or None if the operation fails.
    :rtype: tuple or None
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


def get_nb_game_in_db():
    """
    Retrieve the maximum game ID from the database.

    Returns:
        int: Maximum game ID if found, otherwise returns 1.
    """
    connection = get_connexion()
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
    Starts the application by setting up necessary database connections and initializing
    global variables. The function handles the database connection phase and initializes
    the game ID by determining the highest existing ID in the database.

    :raises DatabaseError: If unable to establish a connection to the database.
    :return: True if function execution is successful.
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

    get_all_players()
    app.logger.info(f"Mapping id:name Index table {indexbyname}")

    id = get_nb_game_in_db()  # Retrieve maximum game ID
    id = id['MAX(partie_id)'] + 1

    app.logger.info(f"Nombre de partie dans la base : {id}")
    return True


# Entry point for the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


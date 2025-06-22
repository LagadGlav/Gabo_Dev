from flask import Flask, jsonify, request
import logging
import requests
import time
import sys
import os
from webbrowser import Error


sys.path.append("/utils")
from util import connect_to_database_interro, get_connexion, notify_service
from exceptions import DatabaseError, NetworkError, StartUpError

API_AP_URL = "http://api-add_player:8010"

# Configuration de Flask
app = Flask(__name__)

API_AG_URL = "http://api-add_game:8020/patch_mapping_index"

# Configure logging to capture INFO-level logs for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)  # Set the logging level to INFO
app.logger.propagate = True  # Allow logs to propagate to parent logger

# Global state
is_ready = False

# Function to insert player data into the database
def send_to_database_j(player_id: str, player_name: str) -> bool:
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
    connection = None
    cursor = None
    try:
        connection = get_connexion()
        cursor = connection.cursor(prepared=True)  # Use prepared statements

        query = """
                INSERT INTO Joueurs (joueur_id, joueur_nom)
                VALUES (%s, %s) \
                """
        cursor.execute(query, (player_id, player_name))
        connection.commit()

        app.logger.info(f"Player inserted: ID={player_id}")

        notify_service(API_AG_URL)
        return True


    except Error as e:
        if connection:
            try:
                connection.rollback()
            except Error:
                app.logger.error("Failed to rollback transaction")
        app.logger.error(f"MySQL Error: {str(e)}")
        raise DatabaseError(f"MySQL Error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def patch_mapping_index(id, name):

    PATCH_URL = API_AG_URL

    json_payload = {'id': id, 'name': name}

    try:
        app.logger.info(f"Sending patch for mapping index for player {id} : {name}")
        response = requests.patch(PATCH_URL, json=json_payload)
        app.logger.info(f"Response from API-AG patch mapping index : {response.status_code}")
        return True
    except NetworkError as e:
        app.logger.error(f"Network error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api-ap/save_player', methods=['POST'])
def save_player():
    """
    Saves player data received from a POST request into the database.

    This function is an API endpoint that handles HTTP POST requests to save
    player data. It expects a JSON payload with `playerId` and `playername` keys.
    Upon successfully saving the player data to the database, it responds with
    a success message and the submitted player details. If the input data is
    invalid, or if the player ID is already taken, an appropriate error is returned
    in the response.

    :param request: The HTTP request containing the JSON payload with player data.
    :type request: Flask.Request
    :return: A JSON response indicating success or failure, along with the respective
        HTTP status code.
    :rtype: Werkzeug.wrappers.response.Response
    """
    try:
        data = request.get_json()
        if not data or 'playerId' not in data or 'playername' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate and sanitize input
        try:
            player_id, player_name = data['playerId'], data['playername']
        except NetworkError as e:
            app.logger.error(f"Network error: {e}")
            return jsonify({'error': str(e)}), 400

        # Try saving to the database
        send_to_database_j(player_id, player_name)

        try:
            patch_mapping_index(player_id, player_name)
        except NetworkError as e:
            return jsonify({'error': str(e)}), 400

        return jsonify({
            'message': 'Player profile saved successfully',
            'data': {'id': player_id, 'name': player_name}
        }), 201

    except DatabaseError as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Player ID already exists'}), 409
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api-ap/get_player_info')
def get_player_info():
    """
    Handles the retrieval of player information based on the provided player ID. This endpoint
    expects a `playerId` argument in the request, fetches the corresponding player's data from
    the database, and returns it as a JSON response. If the player is not found, an error response
    is returned with a 404 status code.

    Raises errors associated with database connectivity, query execution, or JSON response
    construction.

    :returns: A JSON response containing player information if the player is found, otherwise a JSON
        response with an error message, along with a 404 status code.
    :rtype: Flask.Response
    """
    player_id = request.args.get('playerId')  # Get the playerId parameter from the request
    app.logger.info(f"Searching player : {player_id}")

    connection = None
    cursor = None
    try:
        connection = get_connexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (player_id,))
        player = cursor.fetchone()

        if player:
            return jsonify(player), 200
        return jsonify({'error': 'Player not found'}), 404

    except Error as e:
        app.logger.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/api-ap/get_all_players')
def send_all_players():
    """
    Retrieve and return all players in JSON format or an error message if no players
    are found.

    This endpoint fetches a list of all players using the `get_all_players` function.
    If players are successfully retrieved, they are returned as a JSON response. If
    no players are found, an error message is returned with a 404 status code.

    :raises Exception: If there is an internal issue during the retrieval.

    :return: A JSON response containing all players if successful, or a JSON object
        with an error message if no players are found.
    :rtype: Flask.Response
    """
    all_player = get_all_players()

    if all_player != None:
        return  jsonify(all_player)
    else:
        return jsonify({'Error': 'Players not found'}), 404

@app.route('/api-ap/player/<int:player_id>/last-games', methods=['GET'])
def last_ten_games(player_id):
    connection = None
    cursor = None

    try:
        connection = get_connexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT partie_id FROM Partie WHERE joueur_id = %s ORDER BY partie_id DESC LIMIT 10",
            (player_id,)
        )
        last_ten_ids = cursor.fetchall()
        app.logger.info(f"Last ten game ids for player {player_id}: {last_ten_ids}")
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}. Error getting last 10 game ids")
        return jsonify({'error': f'Database error: {str(e)}. Error getting last 10 game ids'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    try:
        connection = get_connexion()
        cursor = connection.cursor(dictionary=True)

        # Extract the game IDs from last_ten_ids (which you have already retrieved)
        game_ids = [record['partie_id'] for record in last_ten_ids]

        if not game_ids:
            app.logger.info("No game IDs found.")
            return jsonify({})  # Return an empty JSON if there are no game IDs to process

        # Build the IN clause with the correct number of placeholders
        placeholders = ", ".join(["%s"] * len(game_ids))
        query = f"""
            SELECT 
                p.*, 
                j.joueur_nom, 
                j.nombre_partie, 
                j.score_total, 
                j.ratio_score, 
                j.ratio_rang, 
                j.elo
            FROM Partie p
            JOIN Joueurs j ON p.joueur_id = j.joueur_id
            WHERE p.partie_id IN ({placeholders})
        """
        cursor.execute(query, tuple(game_ids))
        joined_data = cursor.fetchall()

        # Group the results by partie_id
        games_by_id = {}
        for record in joined_data:
            game_id = record['partie_id']
            if game_id not in games_by_id:
                games_by_id[game_id] = []
            games_by_id[game_id].append(record)

        app.logger.info(f"Last ten games for player {player_id}: {games_by_id}")
        return jsonify(games_by_id)

    except Exception as e:
        app.logger.error(f"Error retrieving joined game data: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_all_players():
    """
    Fetches all players from the 'Joueurs' table in the database and sorts them
    by their 'elo' in descending order, it allows instantly knowing the rank of
     each player without really transporting the info. This function establishes
    a connection with the database via a connection pool, executes a SQL query
    to retrieve the records, and then closes the connection.

    The function handles exceptions related to database operations and ensures
    proper cleanup of resources regardless of execution outcome.

    :return: A list of dictionaries containing player data retrieved from the
        database, with keys corresponding to the column names in the 'Joueurs'
        table. Returns an empty list if an error occurs during execution or
        if no records are found.
    :rtype: List[dict]
    """
    connection = None
    cursor = None
    try:
        connection = get_connexion()
        cursor = connection.cursor(dictionary=True)

        query = """
                SELECT *
                FROM Joueurs
                ORDER BY elo DESC
                """
        cursor.execute(query)
        players = cursor.fetchall()

        return players

    except Error as e:
        app.logger.error(f"Database error: {e}")
        raise DatabaseError(f"Failed to fetch players: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/ready', methods=['GET'])
def notify_ready():
    """
    Notify readiness of the application, initiating the start-up process, and enabling
    the service to handle incoming requests. This endpoint is triggered externally
    to indicate successful backup completion and database readiness.

    Upon invocation, it marks the application as ready, logs the readiness notification,
    attempts the start-up process, and handles any errors during the start-up.

    Global is_ready: A flag indicating whether the application is ready for requests.

    :raises StartUpError: If an error occurs during the start-up process.

    :return: A JSON response with a success or failure message along with the appropriate
        HTTP status code.
    :rtype: Tuple
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

def start_up():
    """
    Initiates the startup process, including attempting to connect to the database.

    This function handles the application's initialization sequence. It attempts
    to connect to the database, providing logging at each step for debugging or
    monitoring purposes. If the database connection is not successful, it raises
    a DatabaseError and logs the failure.

    :raises DatabaseError: If the connection to the database fails.
    :return: None
    """
    time.sleep(1)
    app.logger.info("Connecting to database...")
    try:
        connect_to_database_interro()  # Establish connection
        app.logger.info("Connected")
    except:
        app.logger.info("Impossible to connect, start_up phase failed")
        raise DatabaseError("Connexion failed.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)

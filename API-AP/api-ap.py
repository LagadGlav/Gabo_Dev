from flask import Flask, jsonify, request
import logging
import time
import sys
from webbrowser import Error


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
        connection = get_connexion()  # Get database connection
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

@app.route('/api-ap/save_player', methods=['POST'])
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

@app.route('/api-ap/get_player_info')
def get_player_info():
    """
    Retrieve information about a player from the database using the player's ID.

    Returns:
        JSON: Player details if found, or an error message if not found.
    """
    player_id = request.args.get('playerId')  # Get the playerId parameter from the request
    app.logger.info(f"Searching player : {player_id}")

    connection = get_connexion()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Joueurs WHERE joueur_id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.close()
    connection.close()

    if player:
        return jsonify(player)  # Return player data as JSON
    else:
        return jsonify({'error': 'Player not found'}), 404  # Return an error if not found

@app.route('/api-ap/get_all_players')
def send_all_players():
    all_player = get_all_players()

    if all_player != None:
        return  jsonify(all_player)
    else:
        return jsonify({'Error': 'Players not found'}), 404

def get_all_players():
    """
    Retrieve all rows from the 'Joueurs' table in MySQL.

    Returns:
        list: List of player rows if found, otherwise an empty list.
    """
    connection = None
    all_player = None
    try:
        app.logger.info(f"Querying all players")

        # Get a connection from the pool
        connection = get_connexion()
        # MySQL connector that supports dictionary cursors:
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all rows from 'Joueurs'
        query = "SELECT * FROM Joueurs ORDER BY elo DESC"
        cursor.execute(query)
        all_player = cursor.fetchall()  # Fetch all rows

    except Error as e:
        app.logger.info(f"Erreur lors de la récupération des données : {e}")
        return []  # Handle any errors gracefully

    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use

    if all_player is None:
        return None  # Return an empty list if no data found
    return all_player

@app.route('/ready', methods=['GET'])
def notify_ready():
    """
    Endpoint pour recevoir une notification que l'application est prête.
    """
    global is_ready
    is_ready = True
    app.logger.info("Notification reçue : Backup terminé et base de données opérationnelle.")

    app.logger.info("Démarrage du service...")
    try:
        start_up()
    except StartUpError as e:
        app.logger.error(f"Erreur lors du démarrage : {e}")
        return jsonify({"message": "Start up failed"}), 500

    app.logger.info("Service démarré avec succès.")
    return jsonify({"message": "App is ready"}), 200

def start_up():
    """
    Fonction pour initialiser l'application et établir la connexion à la base de données.
    """
    time.sleep(1)
    app.logger.info("Connecting to database...")
    try:
        connect_to_database_interro()  # Establish connection
        app.logger.info("Connected")
    except:
        app.logger.info("Impossible to connect, restarting start_up phase")
        start_up()
        raise DatabaseError("Connexion failed.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)

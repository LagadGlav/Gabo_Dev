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
    app.logger.info("Tentative de connexion à la base de données...")
    try:
        connexion = connect_to_database_interro()
        app.logger.info("Connexion à la base de données réussie.")
    except DatabaseError as e:
        app.logger.error(f"Erreur lors de la connexion à la base de données : {e}")
        raise DatabaseError("Connexion échouée.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)

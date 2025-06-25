import logging
import time
import mysql.connector
import sys
import requests
import os
from dotenv import load_dotenv

try:
    load_dotenv()
    logging.info("DOTENV LOADED")
except:
    logging.info("DOTENV NOT LOADED")

sys.path.append("/utils")
from exceptions import DatabaseError, NetworkError, StartUpError
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO (adjust as needed: DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)

sys.path.append("/utils")
from exceptions import DatabaseError, NetworkError, StartUpError

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_DATABASE")

def get_connexion():
    """
    Establishes a connection to the MySQL database.
    Returns:
        mysql.connector.connection.MySQLConnection: A MySQL connection object.

    Raises:
        mysql.connector.Error: If unable to connect to the database.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,  # Host name
            user=DB_USER,  # Username
            password=DB_PASSWORD,  # Password
            database=DB_NAME  # Database name
        )
        return connection
    except mysql.connector.Error as e:
        raise mysql.connector.Error(f"Failed to connect to database: {e}")

def build_index_byname():
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
    indexbyname = {}
    logging.info(f"Generating new index table...")
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
            return None

    except Exception as e:
        logging.info(f"Erreur lors de la récupération des données : {e}")
        return None

    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use

    for player in rows:
        indexbyname[f"{player[1]}"] = player[0]

    logging.info(f"New index table {indexbyname}")

    return indexbyname


def connect_to_database_interro():
    """
    Attempt to connect to the MySQL database with retries.

    Returns:
        connection: A MySQL database connection object if successful.

    Raises:
        DatabaseError: If unable to connect after the maximum number of retries.
    """
    max_retries = 10
    for attempt in range(max_retries):
        try:
            logging.info(f"Tentative de connexion... ({attempt + 1}/{max_retries})")
            connection = get_connexion()
            if connection:
                connection.close()
            return connection
        except mysql.connector.Error as e:
            logging.error(f"Erreur lors de la connexion à la base de données : {e}")
            logging.info("Attente avant une nouvelle tentative...")
            time.sleep(1)
    raise DatabaseError("Impossible de se connecter à la base de données après plusieurs tentatives.")

def notify_service(url):
    try:
        logging.info(f"Notifying Flask service at {url}...")
        response = requests.get(url)
        logging.info(f"Notification sent! Flask responded: {response.status_code}")
    except Exception as e:
        logging.info(f"Failed to notify Flask service: {e}")

import logging
import time
import mysql.connector
import sys
import requests
sys.path.append("/utils")
from exceptions import DatabaseError, NetworkError, StartUpError
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO (adjust as needed: DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)

sys.path.append("/utils")
from exceptions import DatabaseError, NetworkError, StartUpError

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
            host="data_base",  # Host name
            user="root",  # Username
            password="Gabo",  # Password
            database="Gabo_base"  # Database name
        )
        return connection
    except mysql.connector.Error as e:
        raise mysql.connector.Error(f"Failed to connect to database: {e}")


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

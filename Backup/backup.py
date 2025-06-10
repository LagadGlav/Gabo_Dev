import os
import time
import subprocess
import datetime
import logging

from utils.util import notify_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO (adjust as needed: DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def wait_for_database(host, port, user, password):
    """
    Waits for a database to become ready by repeatedly sending a ping request until it succeeds.
    This function ensures that the database is ready to accept connections before proceeding
    with further operations. It will continue to wait and check the status in fixed intervals
    until the database responds positively.

    :param host: Database host to connect to
    :type host: str
    :param port: Port where the database is accessible
    :type port: int
    :param user: Username for database authentication
    :type user: str
    :param password: Password for the specified user
    :type password: str
    :return: None
    """
    while True:
        try:
            # Command to check database readiness
            subprocess.run(
                ["mysqladmin", "ping", "-h", host, "-P", str(port), "-u", user, "-p" + password],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            logging.info("Database is ready!")
            break
        except subprocess.CalledProcessError:
            logging.info("Waiting for database to be ready...")
            time.sleep(5)

def restore_latest_backup(backup_path, host, port, user, password, database):
    """
    Restores the latest SQL backup from a specified directory into a MySQL database.

    This function locates the most recently modified `.sql` file in the given backup
    directory and uses the MySQL command-line utility to restore the database from
    that backup. If no `.sql` files exist in the directory, the restoration process
    is skipped and an informational log message is generated. The function assumes
    that the MySQL command-line tool is available and properly configured on the
    system.

    :param backup_path: The directory path where the `.sql` backup files are stored.
    :type backup_path: str
    :param host: The hostname or IP address of the MySQL server.
    :type host: str
    :param port: The port number of the MySQL server.
    :type port: int
    :param user: The username used to authenticate with the MySQL server.
    :type user: str
    :param password: The password corresponding to the MySQL user.
    :type password: str
    :param database: The name of the target database to restore the backup into.
    :type database: str
    :return: None
    """
    # Find the latest backup
    backup_files = [f for f in os.listdir(backup_path) if f.endswith(".sql")]
    if not backup_files:
        logging.info("No backups found. Skipping restoration.")
        return

    latest_backup = max(backup_files, key=lambda f: os.path.getmtime(os.path.join(backup_path, f)))
    latest_backup_path = os.path.join(backup_path, latest_backup)

    logging.info(f"Restoring backup from: {latest_backup_path}")
    restore_command = f"mysql --host={host} --port={port} --user={user} --password={password} {database} < {latest_backup_path}"
    subprocess.run(restore_command, shell=True)
    logging.info("Backup restoration completed.")

def generate_backup(host, port, username, password, database, backup_path, last_backup):
    """
    Generates a backup for a MySQL database using the `mysqldump` command-line
    utility. This function creates a timestamped `.sql` backup file in the
    specified backup directory. If the directory does not exist, it is created
    automatically.

    :param host: Hostname or IP address of the MySQL server.
    :type host: str
    :param port: Port number the MySQL server is listening on.
    :type port: int
    :param username: Username to authenticate with the MySQL server.
    :type username: str
    :param password: Password to authenticate the `username` with the MySQL server.
    :type password: str
    :param database: Name of the database to back up.
    :type database: str
    :param backup_path: Path to the directory where the backup file will be saved.
    :type backup_path: str
    :return: A boolean indicating whether the backup was successful.
    :rtype: bool or None
    """
    # Create a suve if it doesn't exist
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
        logging.info(f"Backup directory '{backup_path}' created.")

    # Name of the backup from date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backup_path, f"{database}_backup_{timestamp}.sql")

    # Commande pour générer la sauvegarde avec mysqldump
    dump_command = [
        "mysqldump",
        "--no-tablespaces",
        f"--host={host}",
        f"--port={port}",
        f"--user={username}",
        f"--password={password}",
        database
    ]

    try:
        # Écrire la sauvegarde dans un fichier
        with open(backup_file, "w") as f:
            subprocess.run(dump_command, stdout=f, check=True)
        logging.info(f"Backup successfully created: {backup_file}")
    except subprocess.CalledProcessError as e:
        logging.info(f"Error during backup: {e}")
        return None

    if last_backup is not None:
        if os.path.exists(last_backup):
            try:
                os.remove(last_backup)
                logging.info(f"{last_backup} removed")
            except OSError as e:
                logging.info(f"Warning {last_backup} has not been removed")

    return backup_file

if __name__ == "__main__":
    DB_HOST = os.getenv("DB_HOST", "data_base")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Gabo")
    DB_NAME = os.getenv("DB_DATABASE", "Gabo_base")
    BACKUP_PATH = os.getenv("BACKUP_PATH", "/Backup/back_up")
    FLASK_URL = os.getenv("FLASK_APP_URL", "http://app:8000/ready")
    API_AP_URL = os.getenv("API_AP_URL", "http://api-add_player:8010/ready")
    API_AG_URL = os.getenv("API_AG_URL", "http://api-add_game:8020/ready")
    API_AG_URL_INDEX = os.getenv("API_AG_URL", "http://api-add_game:8020/reload_indexbyname")


    # Wait for database readiness
    wait_for_database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)

    # Restore the latest backup
    restore_latest_backup(BACKUP_PATH, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    # Notify the Flask service, ready to run
    notify_service(FLASK_URL)

    # Notify the API-AP service, ready to run
    notify_service(API_AP_URL)

    # Notify the API-AG service, ready to run
    notify_service(API_AG_URL)

    backup_status = None
    while True:
        backup_status = generate_backup(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, BACKUP_PATH, backup_status)
        if backup_status is not None:
            time.sleep(3600)
        else:
            wait_for_database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
        time.sleep(3600)
        notify_service(API_AG_URL_INDEX)

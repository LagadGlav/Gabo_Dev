import os
import time
import subprocess
import requests
import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO (adjust as needed: DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def wait_for_database(host, port, user, password):
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

def notify_flask_service(flask_url):
    try:
        logging.info(f"Notifying Flask service at {flask_url}...")
        response = requests.get(flask_url)
        logging.info(f"Notification sent! Flask responded: {response.status_code}")
    except Exception as e:
        logging.info(f"Failed to notify Flask service: {e}")

def generate_backup(host, port, username, password, database, backup_path):
    # Créer le répertoire de sauvegarde s'il n'existe pas
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
        logging.info(f"Backup directory '{backup_path}' created.")

    # Nom du fichier de sauvegarde basé sur la date et l'heure actuelles
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

    return True

if __name__ == "__main__":
    DB_HOST = os.getenv("DB_HOST", "data_base")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Gabo")
    DB_NAME = os.getenv("DB_DATABASE", "Gabo_base")
    BACKUP_PATH = os.getenv("BACKUP_PATH", "/Backup/back_up")
    FLASK_URL = os.getenv("FLASK_URL", "http://app:8000/ready")

    # Wait for database readiness
    wait_for_database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)

    # Restore the latest backup
    restore_latest_backup(BACKUP_PATH, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    # Notify the Flask service
    notify_flask_service(FLASK_URL)

    while True:
        backup_status = generate_backup(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, BACKUP_PATH)
        if backup_status == True:
            time.sleep(60)
        else:
            wait_for_database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)


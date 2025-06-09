import io
import logging
import os

import pandas as pd
import requests
from flask import Flask, jsonify, request
import sys

sys.path.append("/utils")
from exceptions import DatabaseError, NetworkError, StartUpError

from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)
app.logger.propagate = True

# Environment variable for the Kaggle dataset URL
KAGGLE_DATASET_URL = "https://www.kaggle.com/datasets/baptistefougeray/gabo-rules"

# Constants for Kaggle API
DATASET_SLUG = "baptistefougeray/gabo-rules"
DOWNLOAD_DIR = "data"  # Directory where dataset files will be stored
CSV_EN_FILENAME = "Gabo.csv"  # Name of the CSV file inside the dataset
CSV_FR_FILENAME = "Gabo_FR.csv"  # Name of the CSV file inside the dataset
CSV_ES_FILENAME = "Gabo_ES.csv"  # Name of the CSV file inside the dataset
CSV_EUS_FILENAME = "Gabo_EUS.csv"  # Name of the CSV file inside the dataset
CSV_BZH_FILENAME = "Gabo_BR.csv"  # Name of the CSV file inside the dataset
CSV_FILE_PATH_EN = os.path.join(DOWNLOAD_DIR, CSV_EN_FILENAME)
CSV_FILE_PATH_ES = os.path.join(DOWNLOAD_DIR, CSV_ES_FILENAME)
CSV_FILE_PATH_FR = os.path.join(DOWNLOAD_DIR, CSV_FR_FILENAME)
CSV_FILE_PATH_EUS = os.path.join(DOWNLOAD_DIR, CSV_EUS_FILENAME)
CSV_FILE_PATH_BZH = os.path.join(DOWNLOAD_DIR, CSV_BZH_FILENAME)


def download_and_extract_dataset(CSV_FILE_PATH):
    """
    Uses Kaggle API to download and unzip the dataset if it has not been downloaded yet.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Check if the CSV file already exists
    if not os.path.exists(CSV_FILE_PATH):
        app.logger.info("Dataset not found locally. Downloading dataset via Kaggle API...")
        api = KaggleApi()
        api.authenticate()

        # Download dataset files as a ZIP and unzip them automatically
        api.dataset_download_files(DATASET_SLUG, path=DOWNLOAD_DIR, unzip=True)
        app.logger.info("Dataset downloaded and extracted.")
    else:
        app.logger.info("Dataset already exists. Skipping download.")


@app.route('/api-rules/fetch_rules', methods=['GET'])
def fetch_dataset():
    # Get the language parameter, defaulting to English if not provided
    lang = request.args.get('lang', 'en')

    # Select the CSV file based on the language code
    if lang == 'es':
        csv_file_path = CSV_FILE_PATH_ES
    elif lang == 'fr':
        csv_file_path = CSV_FILE_PATH_FR
    elif lang == 'eus':
        csv_file_path = CSV_FILE_PATH_EUS
    elif lang == 'bzh':
        csv_file_path = CSV_FILE_PATH_BZH
    else:
        csv_file_path = CSV_FILE_PATH_EN

    try:
        # Ensure the dataset is downloaded and extracted for the specific language
        download_and_extract_dataset(csv_file_path)

        app.logger.info("Reading CSV file for language: %s", lang)
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame into a JSON-serializable list of records
        data = df.to_dict(orient="records")

        app.logger.info("Dataset fetched and converted successfully for language: %s", lang)
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8030, debug=True)

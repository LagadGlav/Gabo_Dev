import logging
import os

import pandas as pd
import requests
from flask import Flask, jsonify, request

from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.setLevel(logging.INFO)
app.logger.propagate = True

KAGGLE_DATASET_URL = "https://www.kaggle.com/datasets/baptistefougeray/gabo-rules"

# Constants for Kaggle API
DATASET_SLUG = "baptistefougeray/gabo-rules"
DOWNLOAD_DIR = "data"
CSV_EN_FILENAME = "Gabo.csv"
CSV_FR_FILENAME = "Gabo_FR.csv"
CSV_ES_FILENAME = "Gabo_ES.csv"
CSV_EUS_FILENAME = "Gabo_EUS.csv"
CSV_BZH_FILENAME = "Gabo_BR.csv"
CSV_FILE_PATH_EN = os.path.join(DOWNLOAD_DIR, CSV_EN_FILENAME)
CSV_FILE_PATH_ES = os.path.join(DOWNLOAD_DIR, CSV_ES_FILENAME)
CSV_FILE_PATH_FR = os.path.join(DOWNLOAD_DIR, CSV_FR_FILENAME)
CSV_FILE_PATH_EUS = os.path.join(DOWNLOAD_DIR, CSV_EUS_FILENAME)
CSV_FILE_PATH_BZH = os.path.join(DOWNLOAD_DIR, CSV_BZH_FILENAME)


def download_and_extract_dataset(CSV_FILE_PATH):
    """
    Uses Kaggle API to download and unzip the dataset.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    api = KaggleApi()
    api.authenticate()

    # Download dataset files as a ZIP and unzip them automatically
    # Datas are replaced if they already exist locally, allowing for easy updates on rules
    api.dataset_download_files(DATASET_SLUG, path=DOWNLOAD_DIR, unzip=True)
    app.logger.info("Dataset downloaded and extracted.")

@app.route('/api-rules/fetch_rules', methods=['GET'])
def fetch_dataset():
    """
    Retrieves the rules dataset for the specified language.
    """
    lang = request.args.get('lang', 'en')

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

    app.logger.info(f"Fetching rules for language '{lang}' from: {csv_file_path}")

    # Ensure the dataset is downloaded and extracted for the specific language
    download_and_extract_dataset(csv_file_path)

    if not os.path.exists(csv_file_path):
        error_msg = f"CSV file for language '{lang}' not found at {csv_file_path}"
        app.logger.error(error_msg)
        return jsonify({"error": error_msg}), 404

    try:
        app.logger.info("Reading CSV file...")
        # Got some issues with formatting, then try switching to the Python engine and skipping bad lines.
        df = pd.read_csv(csv_file_path, engine='python', on_bad_lines='skip')
        data = df.to_dict(orient="records")
        app.logger.info("Dataset fetched and converted successfully for language: %s", lang)
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8030, debug=True)
import io
import logging
import os

import pandas as pd
import requests
from flask import Flask, jsonify, request
import sys

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
CSV_FILENAME = "Gabo.csv"  # Name of the CSV file inside the dataset
CSV_FILE_PATH = os.path.join(DOWNLOAD_DIR, CSV_FILENAME)


def download_and_extract_dataset():
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
    """
    Fetches a public Kaggle dataset (CSV file) and returns its contents as JSON.
    This endpoint makes an HTTP GET request to the dataset URL, reads the CSV content into
    a pandas DataFrame, and then converts it into a list of dictionary records.
    """
    try:
        # Ensure the dataset is downloaded and extracted
        download_and_extract_dataset()

        app.logger.info("Reading CSV file...")
        # Read the CSV file (the CSV must be properly formatted)
        df = pd.read_csv(CSV_FILE_PATH)

        # Convert DataFrame to a JSON-serializable list of dictionaries
        data = df.to_dict(orient="records")

        app.logger.info("Dataset fetched and converted successfully.")
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        # Log and return any unexpected error
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8030, debug=True)

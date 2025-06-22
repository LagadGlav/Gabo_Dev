from Front_End.blueprints.main import main_bp  # Importing blueprints for routing

from flask import Flask, render_template, request, jsonify  # Flask and utilities for HTTP handling

# Flask application setup
app = Flask(__name__, template_folder='Front_End/templates', static_folder='Front_End/static')  # Initialize Flask app with folder configurations

# Register the main blueprint for modular routing
app.register_blueprint(main_bp)

# Entry point for the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
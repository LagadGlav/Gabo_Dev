from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

saved_tables = []

@app.route('/')
def index():
    return render_template("Chtml.html")

@app.route('/save_table', methods=['POST'])
def save_table():
    data = request.json
    table = data.get("table")
    if table:
        saved_tables.append(table) 
        return jsonify({"message": "Tableau up"})
    else:
        return jsonify({"tabE"}), 400

if __name__ == "__main__":
    app.run(debug=True)


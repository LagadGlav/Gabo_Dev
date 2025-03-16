from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='Front_End/html', static_folder='Front_End')

saved_tables = []

class game:
    def __init__(self, id_game, table):
        self.table = table
        self.id_game = id_game

class queue:
    def __init__(self):
        self.queue = [[]]

    def add_queue(self, partie):
        self.queue.append(partie)
        app.logger.debug(f"Queue: {[(g.id_game, g.table) if isinstance(g, game) else g for g in self.queue]}")


@app.route('/')
def index():
    return render_template("Chtml.html")


@app.route('/save_table', methods=['POST'])
def receive_table():
    app.logger.info("received table")

    data = request.json
    if not data or "table" not in data:
        return jsonify({"error": "Invalid input: 'table' key is missing"}), 400

    table = data.get("table")
    if not table or not isinstance(table, list):
        return jsonify({"error": "Invalid input: 'table' must be a non-empty list"}), 400

    n = len(table[0])//2
    table = [table[0][:n], table[0][n:]]
    app.logger.info(table)
    id = table[0][0][0]
    p_receive = game(id, table)
    Q.add_queue(p_receive)
    return jsonify({"message": "Table received"}), 200

    

if __name__ == "__main__":
    Q = queue()
    app.run(host='0.0.0.0', port=80, debug=True)



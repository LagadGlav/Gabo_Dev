from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='html')

saved_tables = []

class partie:
    def __init__(self, id_partie, table):
        self.id_partie = id_partie
        self.table = table

class queue:
    def __init__(self):
        self.queue = [[]]

    def add_queue(self, partie):
        self.queue.append(partie)

@app.route('/')
def index():
    return render_template("Chtml.html")


@app.route('/save_table', methods=['POST'])
def receive_table():
    data = request.json
    table = data.get("table")
    p_receive = new partie(table[0][0], table)
    Q.add_queue(p_receive)
    

if __name__ == "__main__":
    Q = new queue
    app.run(host='0.0.0.0', port=80, debug=True)



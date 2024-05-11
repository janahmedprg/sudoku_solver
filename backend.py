from flask import Flask, request, jsonify
from flask_cors import CORS
from program2 import backtrack_search, Sudoku
from sudoku_constraints9x9 import constraint9x9

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    print(data['sudokuGrid'])
    sudoku_csp = Sudoku(data['sudokuGrid'])
    sudoku_csp.constraints = constraint9x9
    sudoku_csp.init_adjacency()
    ret = backtrack_search(sudoku_csp)
    print(ret)
    if ret == False:
        ret = "false"
    return ret

if __name__ == '__main__':
    app.run(debug=True)
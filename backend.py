from flask import Flask, request, jsonify, render_template
from program2 import backtrack_search, Sudoku
from sudoku_constraints9x9 import constraint9x9

app = Flask(__name__)

@app.route("/")
def index(name=None):
    return render_template('web.html', name=name)

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    sudoku_csp = Sudoku(data['sudokuGrid'])
    sudoku_csp.constraints = constraint9x9
    sudoku_csp.init_adjacency()
    ret = backtrack_search(sudoku_csp)
    if ret == False:
        ret = "false"
    return ret
from flask import Flask, request, jsonify
from connect4 import playerWon, updateGrid, getValidMoves, boardFull, printGrid
from minimax import minimax
import random

app = Flask(__name__)

cols = 7
rows = 6
grid = [[0 for x in range(cols)] for y in range(rows)]

@app.get("/")
def index():
    return f"Welcome to Connect 4! \n{grid} \n"

@app.get("/game-state")
def game_state():
    return jsonify({"grid": grid})

@app.get("/valid-moves")
def valid_moves():
    return jsonify({"moves": getValidMoves(grid)})

@app.get("/reset")
def reset():
    global grid
    grid = [[0 for x in range(cols)] for y in range(rows)]
    return jsonify({"grid": grid})

@app.post("/setup")
def setup():
    global cols
    global rows
    global grid

    data = request.json
    cols = data.get('cols')
    rows = data.get('rows')
    grid = [[0 for x in range(cols)] for y in range(rows)]
    return jsonify({"grid": grid})

@app.post("/move")
def move():
    data = request.json
    column = data.get('column')
    player = data.get('player')
    #grid = data.get('grid')

    success = True
    win = 0
    tie = False
    player = 1
    winRows = []
    winCols = []

    if column not in getValidMoves(grid):
        return jsonify({"success": False, "grid": grid, "win": win, "tie": tie, "player": player, "winRows": winRows, "winCols": winCols})

    updateGrid(grid, column, player)
    printGrid(grid)

    if playerWon(grid, player, column)[0]:
        success = True
        win = player
        winRows, winCols = playerWon(grid, player, column)[1], playerWon(grid, player, column)[2]

    elif boardFull(grid):
        success = True
        tie = True

    return jsonify({"success": success, "grid": grid, "win": win, "tie": tie, "player": player, "winRows": winRows, "winCols": winCols})

@app.post("/computer-move")
def computer_move():
    data = request.json
    player = data.get('player')
    depth = data.get('depth')
    computer = data.get('computer')
    gameID = data.get('gameID')

    win = 0
    tie = False
    player = 2
    winRows = []
    winCols = []

    if (computer == "minimax"):
        move = minimax(grid, depth, player)[0]
    else:
        possibleMoves = getValidMoves(grid)
        move = possibleMoves[random.randint(0, len(possibleMoves) - 1)]

    #print(request.environ.get('werkzeug.server.shutdown'))
    #if request.environ.get('werkzeug.server.shutdown') is not None:
    #    print("req aborted?")

    print("computer move on backend")
    updateGrid(grid, move, player)

    if playerWon(grid, player, move)[0]:
        win = player
        winRows, winCols = playerWon(grid, player, move)[1], playerWon(grid, player, move)[2]

    elif boardFull(grid):
        tie = True

    return jsonify({"success": True, "grid": grid, "win": win, "tie": tie, "player": player, "winRows": winRows, "winCols": winCols, "gameID": gameID})

if __name__ == "__main__":
    app.run(debug=True)

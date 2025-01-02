from flask import Flask, request, jsonify
from flask_cors import cross_origin
from connect4 import playerWon, updateGrid, getValidMoves, boardFull, printGrid
from minimax import minimax
import random

app = Flask(__name__)

@app.post("/move")
@cross_origin()
def move():
    data = request.json
    column = data.get('column')
    player = data.get('player')
    grid = data.get('grid')

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

    response = jsonify({"success": success, "grid": grid, "win": win, "tie": tie, "player": player, "winRows": winRows, "winCols": winCols})
    return response

@app.post("/computer-move")
@cross_origin()
def computer_move():
    data = request.json
    player = data.get('player')
    depth = data.get('depth')
    computer = data.get('computer')
    gameID = data.get('gameID')
    grid = data.get('grid')

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

    print("computer move on backend")
    updateGrid(grid, move, player)

    if playerWon(grid, player, move)[0]:
        win = player
        winRows, winCols = playerWon(grid, player, move)[1], playerWon(grid, player, move)[2]

    elif boardFull(grid):
        tie = True

    response = jsonify({"success": True, "grid": grid, "win": win, "tie": tie, "player": player, "winRows": winRows, "winCols": winCols, "gameID": gameID})
    return response

if __name__ == "__main__":
    app.run(debug=True)

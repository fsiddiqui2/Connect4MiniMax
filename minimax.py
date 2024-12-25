import random
import copy

player1 = 1
player2 = 2
def evalGrid(grid: list[list[int]]) -> int:
    #check for three in a row with empty spaces (horizontal, vertical, diagonal)
    #check for two in a row with empty spaces (horizontal, vertical, diagonal)
    #check for three in a row of opponent pieces (horizontal, vertical, diagonal)    
    return random.randint(0, 5)

#recursive implementation of minimax
def minimax(grid: list[list[int]], depth: int, player: int) -> list[int, int]:
    #base cases
    if depth == 0:
        return [None, evalGrid(grid)]
    if boardFull(grid):
        return [None, 0]
    
    #maximizer's turn
    if player == player1:
        bestScore = -9999
        bestMove = -1
        for col in getValidMoves(grid):
            
            #copy grid and make a move
            newGrid = copy.deepcopy(grid)
            dropPiece(newGrid, col, player1)

            #evaluate new grid
            if playerWon(newGrid, player1, col):
                score = 9999
            else:
                #recursive call
                score = minimax(newGrid, depth - 1, player2)[1]

            #save the best move and score
            if score > bestScore:
                bestScore = score
                bestMove = col

        return [bestMove, bestScore]

    #minimizer's turn
    else: #player == player2
        bestScore = 9999
        bestMove = -1
        for col in getValidMoves(grid):

            #copy grid and make a move
            newGrid = copy.deepcopy(grid)
            dropPiece(newGrid, col, player2)

            #evaluate new grid
            if playerWon(newGrid, player2, col):
                score = -9999
            else:
                #recursive call
                score = minimax(newGrid, depth - 1, player1)[1]

            #save the best move and score
            if score < bestScore:
                bestScore = score
                bestMove = col

        return [bestMove, bestScore]


def getValidMoves(grid: list[list[int]]) -> list[int]:
    return [col for col in range(len(grid[0])) if grid[0][col] == 0]


def boardFull(grid: list[list[int]]) -> bool:
    return not (0 in grid[0])

def dropPiece(grid: list[list[int]], col: int, player: int):
    for row in range(len(grid) - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = player
            return

def playerWon(grid: list[list[int]], player: int, move: int) -> bool:
    cols = len(grid[0])
    rows = len(grid)

    #find row where move was made
    for row in range(rows):
        if grid[row][move] == player: break

    #check horizontal
    for c in range(cols - 3):
        if grid[row][c] == player and grid[row][c + 1] == player and grid[row][c + 2] == player and grid[row][c + 3] == player:
            return True

    #check vertical
    for r in range(rows - 3):
        if grid[r][move] == player and grid[r + 1][move] == player and grid[r + 2][move] == player and grid[r + 3][move] == player:
            return True

    #check left to right diagonal (start from top left)
    startRow = row - min(move - max(0, move - 3), row - max(0, row - 3))
    startCol = move - min(move - max(0, move - 3), row - max(0, row - 3))
    while startRow + 3 < rows and startCol + 3 < cols:
        if grid[startRow][startCol] == player and grid[startRow + 1][startCol + 1] == player and grid[startRow + 2][startCol + 2] == player and grid[startRow + 3][startCol + 3] == player:
            return True
        startRow += 1
        startCol += 1

    #check right to left diagonal (start from bottom left)
    startRow = row + min(move - max(0, move - 3),  min(rows-1, row + 3) - row)
    startCol = move - min(move - max(0, move - 3), min(rows-1, row + 3) - row)

    while startRow - 3 >=0 and startCol + 3 < cols:
        if grid[startRow][startCol] == player and grid[startRow - 1][startCol + 1] == player and grid[startRow - 2][startCol + 2] == player and grid[startRow - 3][startCol + 3] == player:
            return True
        startRow -= 1
        startCol += 1
    
    return False

def printGrid(grid: list[list[int]]):
    for row in grid:
        print(*row)
        
if __name__ == "__main__":
    '''grid = [[0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 1, 0, 0]]
    
    print(getValidMoves(grid))

    dropPiece(grid, 0, player1)

    printGrid(grid)

    print(playerWon(grid, player1, 0))

    dropPiece(grid, 0, player1)
    dropPiece(grid, 0, player1)
    dropPiece(grid, 0, player1)
    printGrid(grid)
    print(playerWon(grid, player1, 0))'''

    grid = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 2, 2, 1, 0],
            [0, 2, 1, 2, 1]]
    
    printGrid(grid)
    
    
    print(minimax(grid, 2, player1))



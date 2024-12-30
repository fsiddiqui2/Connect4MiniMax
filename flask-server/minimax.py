import random
import copy

player1 = 1
player2 = 2

#calculates score of grid at the start of a given player's turn
def evalGrid(grid: list[list[int]], player: int) -> int:
    #should check if there are two spaces available for a 2-in-a-row

    score = 0;
    n_rows = len(grid)
    n_cols = len(grid[0])

    #check for a vertical two or three in a row with empty space above
    score += verticalEval(grid, player)
    
    #check for a horizontal two or three in a row
    score += horizontalEval(grid, player)
    
    #check for a diagonal two or three in a row with empty space to the left
    score += diagonalEval(grid, player)

    return score

def verticalEval(grid: list[list[int]], player: int):
    score = 0;
    n_rows = len(grid)
    n_cols = len(grid[0])

    #check for a vertical two or three in a row with empty space above
    for col in range(n_cols):
        #find first empty space in column
        row = 0
        while row < n_rows and grid[row][col] == 0:
            row += 1

        #check for three in a row below empty space
        if row != 0 and row < n_rows - 2 and grid[row][col] == grid[row + 1][col] and grid[row][col] == grid[row + 2][col]:
            if player == player1:
                if grid[row][col] == player1:
                    score += 9999 #maximizer can win
                else:
                    score -= 10 
            else:
                if grid[row][col] == player2:
                    score -= 9999 #minimizer can win
                else:
                    score += 10

        #check for two in a row below two empty spaces
        #row > 1 ensures two empty spaces above 
        elif row > 1 and row < n_rows - 1 and grid[row][col] == grid[row + 1][col]:
            if grid[row][col] == player1:
                score += 1
            else:
                score -= 1
    return score

def horizontalEval(grid: list[list[int]], player: int):
    score = 0;
    n_rows = len(grid)
    n_cols = len(grid[0])

    for row in range(n_rows):
        start = 0
        end = 0
        while end < n_cols:
            #find the first non-empty space in the row
            if grid[row][start] == 0:
                start += 1
                end += 1
            else:
                #find the end of connected pieces
                while end + 1 < n_cols and grid[row][end + 1] == grid[row][start]:
                    end += 1
                
                #weight score based on number of empty spaces
                #for three in a row: 0 1 1 1 0 > 0 1 1 1 = 1 1 1 0
                
                spaces = 0
                if (start > 0 and grid[row][start - 1] == 0): spaces += 1
                if (end < n_cols - 1 and grid[row][end + 1] == 0): spaces += 1

                #three in a row
                if end - start == 2:
                    if player == player1:
                        if grid[row][start] == player1:
                            score += 15 * spaces #maximizer not guaranteed to win, unless it can place direcly into the empty spaces
                        else:
                            score -= 15 * spaces 
                    else:
                        if grid[row][start] == player2:
                            score -= 15 * spaces
                        else:
                            score += 15 * spaces

                #two in a row
                elif end - start == 1:
                    #weight based on spaces
                    #for two in a row: 0 0 1 1 = 0 1 1 0 = 1 1 0 0

                    if (start > 1 and grid[row][start - 2] == 0 and grid[row][start - 2] == 0): spaces += 1
                    if (end < n_cols - 2 and grid[row][end + 1] == 0 and grid[row][end + 2] == 0): spaces += 1
                    if grid[row][start] == player1:
                        score += 5 if spaces >= 2 else 0
                    else:
                        score -= 5 if spaces >= 2 else 0
                
                end += 1
                start = end
    return score

def diagonalEval(grid: list[list[int]], player: int):
    score = 0;
    n_rows = len(grid)
    n_cols = len(grid[0])

    return score

#recursive implementation of minimax
def minimax(grid: list[list[int]], depth: int, player: int) -> list[int, int]:
    #base cases
    if depth == 0:
        return [None, evalGrid(grid, player)]
    if boardFull(grid):
        return [None, 0]
    
    #maximizer's turn
    if player == player1:
        bestScore = -99999999
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
        bestScore = 99999999
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

    grid = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 2, 2, 0],
            [0, 2, 1, 1, 1],
            [0, 2, 1, 1, 1]]
    
    printGrid(grid)
    
    
    
    print(evalGrid(grid, player2))
    print(minimax(grid, 2, player2))



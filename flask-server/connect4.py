from minimax import minimax 

#initialize grid
cols = 7
rows = 6
grid = [[0 for x in range(cols)] for y in range(rows)]

turn = 0
boardFull = False
win = False
winRows = []
winCols = []

def printGrid(grid: list[list[int]]):
    for row in grid:
        print(*row)

def getValidMoves(grid: list[list[int]]) -> list[int]:
    return [col for col in range(len(grid[0])) if grid[0][col] == 0]

def getPlayerMove(grid: list[list[int]]) -> int:
    move = int(input("Select a column: ")) 
    while move not in getValidMoves(grid):
        print("Column is invalid or full, select another column")
        move = int(input("Select a column: "))
    return move

def updateGrid(grid: list[list[int]], move: int, player: int):
    for row in range(len(grid) - 1, -1, -1):
        if grid[row][move] == 0:
            grid[row][move] = player
            return

def playerWon(grid: list[list[int]], player: int, move: int) -> tuple[bool, list[int], list[int]]:
    cols = len(grid[0])
    rows = len(grid)

    #find row where move was made
    for row in range(rows):
        if grid[row][move] == player: break

    #check horizontal
    for c in range(cols - 3):
        if grid[row][c] == player and grid[row][c + 1] == player and grid[row][c + 2] == player and grid[row][c + 3] == player:
            win = True
            for i in range(4):
                winRows.append(row)
                winCols.append(c + i)
            return (win, winRows, winCols)

    #check vertical
    for r in range(rows - 3):
        if grid[r][move] == player and grid[r + 1][move] == player and grid[r + 2][move] == player and grid[r + 3][move] == player:
            win = True
            for i in range(4):
                winRows.append(r + i)
                winCols.append(move)
            return (win, winRows, winCols)

    #check left to right diagonal (start from top left)
    startRow = row - min(move - max(0, move - 3), row - max(0, row - 3))
    startCol = move - min(move - max(0, move - 3), row - max(0, row - 3))
    while startRow + 3 < rows and startCol + 3 < cols:
        if grid[startRow][startCol] == player and grid[startRow + 1][startCol + 1] == player and grid[startRow + 2][startCol + 2] == player and grid[startRow + 3][startCol + 3] == player:
            win = True
            for i in range(4):
                winRows.append(startRow + i)
                winCols.append(startCol + i)
            return (win, winRows, winCols)
        
        startRow += 1
        startCol += 1

    #check right to left diagonal (start from bottom left)
    startRow = row + min(move - max(0, move - 3),  min(rows-1, row + 3) - row)
    startCol = move - min(move - max(0, move - 3), min(rows-1, row + 3) - row)

    while startRow - 3 >=0 and startCol + 3 < cols:
        if grid[startRow][startCol] == player and grid[startRow - 1][startCol + 1] == player and grid[startRow - 2][startCol + 2] == player and grid[startRow - 3][startCol + 3] == player:
            win = True
            for i in range(4):
                winRows.append(startRow - i)
                winCols.append(startCol + i)
            return (win, winRows, winCols)
        
        startRow -= 1
        startCol += 1
    
    return (False, [], [])

def boardFull(grid: list[list[int]]) -> bool:
    return not(0 in grid[0])

if __name__ == "__main__":
    printGrid(grid)

    while not(boardFull(grid) or win):
        # -- switch player -- #
        player = 1 if turn % 2 == 0 else 2

        # -- read in move -- #
        if player == 1: #player's move
            move = getPlayerMove(grid)
        else: #computers move
            move = minimax(grid, 4, player)[0]
            print(f"Computer's move: {move}")

        updateGrid(grid, move, player)
            
        # -- check for win -- #
        win, winRows, winCols = playerWon(grid, player, move)
        
        # -- toggle turn -- #
        turn += 1

        printGrid(grid)



    if boardFull(grid) and not win:
        print("Tie!")
    else:
        print(f"{"Computer " if player == 2 else "Player "} wins!")

        for i in range(4):
            grid[winRows[i]][winCols[i]] = "X"

    printGrid(grid)

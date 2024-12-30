import React, {useState, useEffect, use} from 'react';


function App() {
  const [grid, setGrid] = useState([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]);
  const [win, setWin] = useState(0);
  const [turn, setTurn] = useState(0);
  const [tie, setTie] = useState(false);
  const [winRows, setWinRows] = useState([]);
  const [winCols, setWinCols] = useState([]);

  useEffect(() => {
    setUp()
  }, [])

  useEffect(() => {
    if(win != 0 || tie) {
      console.log("game complete!")
    }
  }, [win, tie])

  const setUp = async () => {
    const data = {cols: 7, rows: 6}
    const res = await fetch('/setup', {method: "POST", body: JSON.stringify(data), headers: {"Content-Type": "application/json"}})
    const result = await res.json()
    setGrid(result.grid)
  }

  const playerMove = async (col) => {

    const validFetch = await fetch('/valid-moves')
    const valid = await validFetch.json()
    if (!valid.moves.includes(col) || win != 0 || tie) {
      return
    }

    const data = {column: col, player: 1}
    const res = await fetch('/move', {method: "POST", body: JSON.stringify(data), headers: {"Content-Type": "application/json"}})
    const result = await res.json()
    
    setGrid(result.grid)
    setWin(result.win)
    setTie(result.tie)
    setWinRows(result.winRows)
    setWinCols(result.winCols)

    setTurn(turn + 1)
  }

  useEffect(() => {
    if (turn % 2 == 1) {
      computerMove()
    }
  }, [turn])
  const computerMove = async () => {
    if (win != 0 || tie) {
      return
    }

    const res = await fetch('/minimax', {method: "POST", body : JSON.stringify({player: 2}), headers: {"Content-Type": "application/json"}})
    const result = await res.json()

    setGrid(result.grid)
    setWin(result.win)
    setTie(result.tie)
    setWinRows(result.winRows)
    setWinCols(result.winCols)

    setTurn(turn + 1)
  }

  const resetGame = async () => {
    const res = await fetch('/reset')
    const result = await res.json()
    setGrid(result.grid)
    setWin(0)
    setTie(false)

  }

  return (
    <div style={{margin: "auto", width: "50%", height: "50%", border: "1px solid black", padding: "10px"}}>
      <h1 style={{color: "blue"}}>Connect 4</h1>

      <h2>{win === 1 ? "You Win!" : win === 2 ? "You Lose!" : tie ? "Tie!" : ""}</h2>

      <table>
        <tbody>
          <tr>
            {grid[0].map((col, j) => <th key={j}><button onClick={() => playerMove(j)}></button></th>)}
          </tr>
          {grid.map((row, i) => <tr key={i}>{row.map((val, j) => <td style={{color: val === 1 ? "blue" : val === 2 ? "red" : "black"}} key={j}>{val === 0 ? "•" : "O"}</td>)}</tr>)}
        </tbody>
      </table>

      <button onClick={() => resetGame()}>Reset</button>
    </div>
  );
}

export default App;

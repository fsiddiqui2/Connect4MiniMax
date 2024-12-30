import React, {useState, useEffect, use} from 'react';
import './App.css';
import yellowToken from './media/token-yellow.png'
import redToken from './media/token-red.png'


function App() {
  const [grid, setGrid] = useState([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]);
  const [win, setWin] = useState(0);
  const [turn, setTurn] = useState(0);
  const [tie, setTie] = useState(false);
  const [winRows, setWinRows] = useState([]);
  const [winCols, setWinCols] = useState([]);

  const controller = new AbortController();
  const signal = controller.signal;

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
    if (turn === 0){
      setUp()
    }
    
    if (win != 0 || tie || turn % 2 == 1) {
      return
    }

    const validFetch = await fetch('/valid-moves')
    const valid = await validFetch.json()
    if (!valid.moves.includes(col)) {
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
    try{
      const res = await fetch('/minimax', {method: "POST", body : JSON.stringify({player: 2}), headers: {"Content-Type": "application/json"}, signal: signal})
      const result = await res.json()

      setGrid(result.grid)
      setWin(result.win)
      setTie(result.tie)
      setWinRows(result.winRows)
      setWinCols(result.winCols)

      setTurn(turn + 1)
    }
    catch(err) {
      if (signal.aborted){
        console.log("Fetch Aborted")
      }
      else {
        console.log(err)
      }
    }
  }

  const resetGame = async () => {
    controller.abort()
    const res = await fetch('/reset')
    const result = await res.json()
    setGrid(result.grid)
    setWin(0)
    setTie(false)
    setTurn(0)

  }


  return (
    <div className = "App">
      <h1>Connect 4</h1>

      <h2>{win === 1 ? "You Win!" : win === 2 ? "You Lose!" : tie ? "Tie!" : turn % 2 == 0 ? "Your Turn" : "Computer's Turn"}</h2>

      <table>
        <tbody>
          <tr>
            {grid[0].map((col, j) => <th key={j}><button onClick={() => playerMove(j)}></button></th>)}
          </tr>
          {grid.map((row, i) => <tr key={i}>{row.map((val, j) => <td key = {j}>
            {val === 1 ? <img className="token" src={yellowToken} alt="yellow"/> : val === 2 ? <img className="token" src={redToken} alt="red"/> : null}
          </td>)}</tr>)}
        </tbody>
      </table>

      <br></br>

      <button onClick={() => resetGame()}>Reset</button>

      <footer>
        <p>Made by <a href="https://github.com/fsiddiqui2" target="_blank">fsiddiqui2</a> | Icons from <a href="https://www.freepik.com/" target="_blank" title="freepik.com">Freepik</a></p>
      </footer>
    </div>
    
  );
}

export default App;

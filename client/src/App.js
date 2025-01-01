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
  const [start, setStart] = useState(false);
  const [depth, setDepth] = useState(4);
  const [firstPlayer, setFirstPlayer] = useState(1); // 1 = yellow (player), 2 = red (computer)

  const controller = new AbortController();
  const signal = controller.signal;

  useEffect(() => {
    //setUp()
  }, [])

  useEffect(() => {
    if(win != 0 || tie) {
      console.log("game complete!")
    }
  }, [win, tie])

  function timeout(delay) {
    return new Promise( res => setTimeout(res, delay) );
  }

  const setUp = async () => {
    controller.abort()
    const data = {cols: 7, rows: 6}
    const res = await fetch('/setup', {method: "POST", body: JSON.stringify(data), headers: {"Content-Type": "application/json"}})
    const result = await res.json()
    setGrid(result.grid)
    setWin(0)
    setTie(false)
    setTurn(0)
    setStart(true)
  }

  const stopGame = () => {
    controller.abort()
    setStart(false)
  }

  const playerMove = async (col) => {
    if (turn === 0){
      setUp()
    }
     
    const playerTurn = firstPlayer === 1 ? turn % 2 == 0 : turn % 2 == 1

    if (win != 0 || tie || !playerTurn) {
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
    setTurn(turn + 1)
    setWin(result.win)
    setTie(result.tie)
    await timeout(1000);
    setWinRows(result.winRows)
    setWinCols(result.winCols)
    
  }

  useEffect(() => {
    const computerTurn = firstPlayer === 2 ? turn % 2 == 0 : turn % 2 == 1
    if (computerTurn) {
      computerMove()
    }
  }, [turn, start])
  const computerMove = async () => {
    if (win != 0 || tie) {
      return
    }
    if (turn === 0){
      setUp()
    }
    try{
      const res = await fetch('/minimax', {method: "POST", body : JSON.stringify({player: 2, depth: depth}), headers: {"Content-Type": "application/json"}, signal: signal})
      const result = await res.json()

      setGrid(result.grid)
      setTurn(turn + 1)
      setWin(result.win)
      setTie(result.tie)
      await timeout(1000);
      setWinRows(result.winRows)
      setWinCols(result.winCols)

      
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

  const displayTurn = () =>{
    if (win == 1 || win == 2 || tie) {
      return (win === 1 ? "You Win!" : win === 2 ? "You Lose!" : "Tie!");
    }
    else if ((turn % 2 == 0 && firstPlayer === 1) || (turn % 2 == 1 && firstPlayer === 2)){
      return "Your Turn";
    }
    else {
      return "Computer's Turn";
    }
  }


  return (
    <div className = "App">
      <h1>Connect 4</h1>

      {!start ? 
        <form>
          <label>Computer Depth: </label>
          <select style={{margin: "5px"}} value={depth} onChange={(event) => {setDepth(parseInt(event.target.value))}}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
          </select>



          <label>First to Move: </label>
          <select value={firstPlayer} onChange={(event) => {setFirstPlayer(parseInt(event.target.value))}}>
            <option value="1">Player</option>
            <option value="2">Computer</option>
          </select>
          
        </form>
      : 
        <p>Computer Depth: {depth} | First to Move: {firstPlayer === 1 ? "Player" : "Computer"}</p>
      }

      <br></br>
      <button onClick={() => setUp()}>New Game</button>
      <button onClick={() => stopGame()}>Stop Game</button>

      {start ? (
        <div>
          <h2>{displayTurn()}</h2>

          <table>
            <tbody>
              <tr>
                <th>1</th>
                <th>2</th>
                <th>3</th>
                <th>4</th>
                <th>5</th>
                <th>6</th>
                <th>7</th>
              </tr>
              {grid.map((row, i) => <tr key={i}>{row.map((val, j) => <td key = {j} onClick={() => playerMove(j)}>
                {val === 1 ? <img className={"token" + " row" + (i + 1)} src={yellowToken} alt="yellow"/> : val === 2 ? <img className={"token" + " row" + (i + 1)} src={redToken} alt="red"/> : null}
              </td>)}</tr>)}
            </tbody>
          </table>

          <br></br>

          <button onClick={() => resetGame()}>Reset</button>
        </div>
      ) : null}

      <footer>
        <p>Made by <a href="https://github.com/fsiddiqui2" target="_blank">fsiddiqui2</a> | Icons from <a href="https://www.freepik.com/" target="_blank" title="freepik.com">Freepik</a></p>
      </footer>
    </div>
    
  );
}

export default App;

import React, {useState, useEffect, useRef} from 'react';
import './App.css';
import yellowToken from './assets/token-yellow.png'
import redToken from './assets/token-red.png'

//python flask server
const proxy = "http://127.0.0.1:5000";

function App() {
  //game variables
  const [grid, setGrid] = useState([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]);
  const [win, setWin] = useState(0);
  const [turn, setTurn] = useState(0);
  const [tie, setTie] = useState(false);
  const [winRows, setWinRows] = useState([]);
  const [winCols, setWinCols] = useState([]);
  const [start, setStart] = useState(false);
  const [depth, setDepth] = useState(4); //depth of minimax
  const [firstPlayer, setFirstPlayer] = useState(1); // 1 =  player, 2 = computer
  const [computer, setComputer] = useState("minimax")
  const [gameID, setGameID] = useState(0);
  const [playerColor, setPlayerColor] = useState("yellow");

  const idref = useRef();
  idref.current = gameID;

  useEffect(() => {
    if(win != 0 || tie) {
      console.log("game complete!")
    }
  }, [win, tie])

  //helper functions

  //delay function to wait for animation
  function timeout(delay) {
    console.log("timeout")
    return new Promise( res => setTimeout(res, delay) );
  }

  //set up game
  const setUp = () => {
    console.log("setup")
    setGameID(gameID + 1) //increment gameID

    const data = {cols: 7, rows: 6}
    const newGrid = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    
    //reset game variables
    setGrid(newGrid)
    setWin(0)
    setTie(false)
    setTurn(0)
    setStart(true)
  }

  //stop game
  const stopGame = async () => {
    console.log("stop game")
    setStart(false)
  }


  //gets player move and updates variables and grid accordingly
  //must be async for fetch request
  const playerMove = async (col) => {
    console.log("player move")
    
    const playerTurn = firstPlayer === 1 ? turn % 2 == 0 : turn % 2 == 1

    //skip player move if it is not their turn or game is over
    if (win != 0 || tie || !playerTurn) {
      return
    }

    //send data as json to server
    const data = {column: col, player: 1, grid: grid}
    const res = await fetch(proxy +'/move', {method: "POST", body: JSON.stringify(data), headers: {"Content-Type": "application/json"}})
    console.log(res)
    const result = await res.json()
    
    //update variables
    setGrid(result.grid)
    setTurn(turn + 1)
    setWin(result.win)
    setTie(result.tie)
    await timeout(1000); //delay to wait for player token animation
    setWinRows(result.winRows)
    setWinCols(result.winCols)
    
  }

  //runs every time turn changes or game is started/stopped 
  useEffect(() => {
    console.log("use effect: computer move?")
    const computerTurn = firstPlayer === 2 ? turn % 2 == 0 : turn % 2 == 1
    //check if its the computer's turn and the game is started; if so, make a move
    if (computerTurn && start) {
      computerMove()
    }
  }, [turn, start])
  const computerMove = async () => {
    console.log("computer move")
    if (win != 0 || tie) {
      return
    }
    try{
      await timeout(1000); //wait for player's token animation to finish
      const res = await fetch(proxy + '/computer-move', {method: "POST", body : JSON.stringify({player: 2, computer: computer, depth: depth, gameID: gameID, grid: grid}), headers: {"Content-Type": "application/json"}})
      const result = await res.json()
      console.log("gameID: " + gameID + " result gameID: " + result.gameID + " gameIDref: " + idref.current)
      
      //ignore a response from a previous game
      if(idref.current !== result.gameID) {
        return
      }
      //update variables
      console.log("computer moving...")
      setGrid(result.grid)
      setTurn(turn + 1)
      setWin(result.win)
      setTie(result.tie)
      await timeout(1000); //delay to wait for computer token animation
      setWinRows(result.winRows)
      setWinCols(result.winCols)
    }
    catch(err) {
      console.log(err)
    }
  }


  //function to display whose turn it is or who won
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
          <label>Computer Type: 
          <select value={computer} onChange={(event) => {setComputer(event.target.value)}}>
            <option value="minimax">minimax algorithm</option>
            <option value="random">random moves</option>
          </select>
          </label>
          
          {computer === "minimax" ? 
          <label>Computer Difficulty: 
          <select value={depth} onChange={(event) => {setDepth(parseInt(event.target.value))}}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
          </select>
          </label>
          : null}

          <label>First to Move: 
          <select value={firstPlayer} onChange={(event) => {setFirstPlayer(parseInt(event.target.value))}}>
            <option value="1">Player</option>
            <option value="2">Computer</option>
          </select>
          </label>

          <label>Player Color:
          <select value={playerColor} onChange={(event) => {setPlayerColor(event.target.value)}}>
            <option value="yellow">Yellow</option>
            <option value="red">Red</option>
          </select>
          </label>
          
        </form>
      : 
        <p>Algorithm: {computer} | Computer Depth: {depth} | First to Move: {firstPlayer === 1 ? "Player" : "Computer"}</p>
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
                {val === 1 ? <img className={"token" + " row" + (i + 1)} src={playerColor === "yellow" ? yellowToken : redToken} alt="player"/> : val === 2 ? <img className={"token" + " row" + (i + 1)} src={playerColor === "yellow" ? redToken : yellowToken} alt="computer"/> : null}
              </td>)}</tr>)}
            </tbody>
          </table>

          <br></br>
        </div>
      ) : null}

      <footer>
        <p>Made by <a href="https://github.com/fsiddiqui2" target="_blank">fsiddiqui2</a> | Icons from <a href="https://www.freepik.com/" target="_blank" title="freepik.com">Freepik</a></p>
      </footer>
    </div>
    
  );
}

export default App;

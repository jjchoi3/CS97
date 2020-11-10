import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props){
    return(
	<button
	    className="square"
	    onClick={props.onClick}
	>
	    {props.value}
	</button>
    );
}

function calculateWinner(squares){
    const lines = [
	[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8],
	[0, 3, 6],
	[1, 4, 7],
	[2, 5, 8],
	[0, 4, 8],
	[2, 4, 6],
    ];
    for(let i = 0; i < lines.length; i++){
	const [a, b, c] = lines[i];
	if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]){
	    return squares[a];
	}
    }
    return null;
}

function isValidMove(movePieceLocation, i){ //NEW//
    /*[0, 1, 2]
      [3, 4, 5]
      [6, 7, 8]*/
    if(movePieceLocation === 0){
	return (i === 1 || i === 3 || i === 4);
    }else if(movePieceLocation === 1){
	return (i === 0 || i === 2 || i === 3 || i === 4 || i === 5);
    }else if(movePieceLocation === 2){
	return (i === 1 || i === 4 || i === 5);
    }else if(movePieceLocation === 3){
	return (i === 0 || i === 1 || i === 4 || i === 6 || i === 7);
    }else if (movePieceLocation === 4){
	return (i === 0 || i === 1 || i === 2 || i === 3 || i === 5 || i === 6 || i === 7 || i === 8);
    }else if(movePieceLocation === 5){
	return (i === 1 || i === 2 || i === 4 || i === 7 || i === 8);
    }else if(movePieceLocation === 6){
	return (i === 3 || i === 4 || i === 7);
    }else if(movePieceLocation === 7){
	return (i === 3 || i === 4 || i === 5 || i === 6 || i === 7);
    }else if (movePieceLocation === 8){
	return (i === 4 || i === 5 || i === 7);
    }
}
class Board extends React.Component{
    renderSquare(i){
	return (
	    <Square
		value={this.props.squares[i]}
		onClick={() => this.props.onClick(i)}
	    />
	);
    }

    render(){
	return (
	   <div>
		<div className="board-row">
		 {this.renderSquare(0)}
	         {this.renderSquare(1)}
	         {this.renderSquare(2)}
	         </div>
		<div className="board-row">
	         {this.renderSquare(3)}
	         {this.renderSquare(4)}
	         {this.renderSquare(5)}
	        </div>
		<div className="board-row">
	         {this.renderSquare(6)}
	         {this.renderSquare(7)}
	         {this.renderSquare(8)}
	        </div>
            </div>
	);
    }
}
class Game extends React.Component{
    constructor(props){
	super(props);
	this.state ={
	    history: [{
		squares: Array(9).fill(null),
	    }],
	    stepNumber: 0,
	    movePieceLocation: null,
	    movePieceSet: false,
	    xIsNext: true,
	    
	};
    }
    handleClick(i){
	const history = this.state.history.slice(0, this.state.stepNumber + 1);
	const current = history[history.length - 1];
	const squares = current.squares.slice();

	if(calculateWinner(squares)){
	    return;
	}
	if(history.length <= 6){
	    if(squares[i]){
		return;
	    }

	    squares[i] = this.state.xIsNext ? 'X' : 'O';
	    this.setState({
		history: history.concat([{
		    squares: squares,
		}]),
		stepNumber: history.length,
		xIsNext: !this.state.xIsNext,
	    });
	}else if(!this.state.movePieceSet){ // If piece to move wasn't chosen
	    if(squares[i] !== (this.state.xIsNext ? 'X' : 'O')){
		return;
	    }else{
		this.setState({
		    movePieceLocation: i,
		    movePieceSet: true,
		});
	    }
	}else if(this.state.movePieceSet){ // If piece to move was chosen
	    if(squares[i] || !isValidMove(this.state.movePieceLocation, i)){
		this.setState({ // Reset just in case player is soft locked
		    movePieceLocation: null,
		    movePieceSet: false,
		});
		return;
	    }
	    if(squares[4] === (this.state.xIsNext ? 'X' : 'O') && this.state.movePieceLocation !== 4){
		const nextSquares = squares;
		nextSquares[i] = this.state.xIsNext ? 'X' : 'O';
		nextSquares[this.state.movePieceLocation] = null;
		if(!calculateWinner(nextSquares)){
		    alert('Please win on the next turn or vacate the middle square please!');
		    this.setState({
			movePieceLocation: null,
			movePieceSet : false,
		    });
		    return;
		}
	    }
	    squares[i] = this.state.xIsNext ? 'X' : 'O';
	    squares[this.state.movePieceLocation] = null
	    this.setState({
		history: history.concat([{
		    squares:squares,
		}]),
		stepNumber: history.length,
		xIsNext: !this.state.xIsNext,
		movePieceLocation: null,
		movePieceSet: false,
	    });
	}
    }
    
    jumpTo(step){
	this.setState({
	    stepNumber: step,
	    xIsNext: (step % 2) === 0,
	});
    }
    
    render(){
	const history = this.state.history;
	const current = history[this.state.stepNumber];
	const winner = calculateWinner(current.squares);

	const moves = history.map((step, move) => {
	    const desc = move ? 'Go to move #' + move : 'Go to game start';
	    return(
		<li key={move}>
		    <button onClick={() => this.jumpTo(move)}>{desc}</button>
		</li>
	    );
	});
	
	let status;
	if(winner){
	    status = 'Winner: ' + winner;
	}else{
	    const playerTurn = 'Next Player : ' + (this.state.xIsNext ? 'X' : 'O');
	    if(history.length <= 6){ //NEW// 6
		status = playerTurn;
	    }else{
		status = playerTurn + ' ' +  (this.state.movePieceSet ? 'Where do you want to move it?' : 'Pick a piece to move');
	    }
	}
	    
	return(
	  <div className="game">
	    <div className="game-board">
		<Board
		    squares = {current.squares}
		    onClick={(i) => this.handleClick(i)}
		/>
	    </div>
	    <div className="game-info">
		<div>{status}</div>
		<ol>{moves} </ol>
		</div>
		</div>
	);
    }
}

// =================
ReactDOM.render(
    <Game />,
	document.getElementById('root')
);

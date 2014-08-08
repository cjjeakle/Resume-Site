function loadExampleBoard(board) {
	var evilExample = [[0,0,0,6,0,0,0,0,1], 
						[7,0,0,0,9,4,5,0,0], 
						[4,0,0,0,0,2,0,0,0], 
						[0,5,0,0,1,0,7,0,2], 
						[0,2,0,0,0,0,0,6,0], 
						[3,0,6,0,8,0,0,9,0], 
						[0,0,0,8,0,0,0,0,7], 
						[0,0,3,7,6,0,0,0,8], 
						[9,0,0,0,0,3,0,0,0]];

	clearBoard();
	if (board == null) {
		board = evilExample;
	}
	for (i = 0; i < 9; i++) {
		for (j = 0; j < 9; j++) {
			if (board[i][j] != null && board[i][j] != 0) {
				document.getElementById('sq'+(i*9+j)).value = board[i][j];
			}
		}
	}
}

function clearBoard() {
	for (i = 0; i < 9; i++) {
		for (j = 0; j < 9; j++) {
			document.getElementById('sq'+(i*9+j)).value = "";
		}
	}
	document.getElementById('sudokuInfo').innerHTML = "<br/>";
}

function attemptSolve() {
	document.getElementById('sudokuInfo').innerHTML = '<br>';
	try {
		var board = populateBoardBuffer();
		sufficentGivens(board);
		if(!validBoard(board)) {
			throw ('There is a conflict on the board');
		}
	} catch (err) {
		document.getElementById('sudokuInfo').innerHTML = err + '<br/><br/>';
		return;
	}
}

// populate a buffer array wiht the board's contents.
// returns null if the board contains any spaces that aren't blank or a number <= 9 and > 0.
function populateBoardBuffer() {
	var board = new Array(9*9);
	for (i = 0; i < 9; i++) {
		for (j = 0; j < 9; j++) {
			var idx = i*9+j;
			board[idx] = document.getElementById('sq'+idx).value;
			if (board[idx]!= '' && (board[idx] < 1 || board[idx] > 9 || isNaN(board[idx]))) {
				console.log((board[idx]), idx);
				throw('Invalid Board State!');
			}
		}
	}
	return board;
}

function sufficentGivens(board) {
	var count = 0;
	for (i = 0; i < 81; i++) {
		if(board[i] != '') {
			++count;
		}
	}
	if(count < 17) {
		throw ('Not Enough Givens (min 17)');
	}
}

// Ensure the board is valid by checking for conflicting nubmers
function validBoard(board) {
	for (var i = 0; i < 9; i++) {
		for (var j = 0; j < 9; j++) {
			if (checkRowForNum(board, i, j, board[i*9+j]) ||
				checkColForNum(board, i, j, board[i*9+j]) ||
				checkSubBoardForNum(board, i, j, board[i*9+j])) {
				return false;
			}
		}
	}
	return true;
}

function checkRowForNum(board, row, col, val) {
	if(val == '') {
		return false;
	}
	for(var j = 0; j < 9; j++) {
		if(board[row*9 + j] == val && j != col) {
			return true;
		}
	}
	return false;
}

function checkColForNum(board, row, col, val) {
	if(val == '') {
		return false;
	}
	for(var i = 0; i < 9; i++) {
		if(board[i*9 + col] == val && i != row) {
			return true;
		}
	}
	return false;
}

function checkSubBoardForNum(board, row, col, val) {
	subBoardRow = Math.floor(row/3);
	subBoardCol = Math.floor(col/3);
	for(var i = 0; i < 9; i++) {
		if((Math.floor(i/3) == subBoardRow && Math.floor(j/3) == subBoardCol) && 
			(i != row && j != col && board[i*9 + j] == val)) {
			return true;
		}
	}
	return false;
}





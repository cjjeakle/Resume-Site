function findByClass(className, domNode, tagName) {
	if (domNode == null)
	{
		domNode = document;
	}
	if (tagName == null)
	{
		tagName = '*';
	}
	var elts = new Array();
	var tags = domNode.getElementsByTagName(tagName);
	var findThis = " "+className+" ";
	for(i = 0, j = 0; i < tags.length; i++) {
		var test = " " + tags[i].className + " ";
		if (test.indexOf(findThis) != -1)
		{
			elts[j++] = tags[i];
		}
	}
	return elts;
}

var hidden = false;
function toggleShow(obj)
{
	hidden = !hidden;
	titles = findByClass('navHeader', null, null);
	elts = findByClass(obj, null, 'div');
	for (i = 0; i < elts.length; i++)
	{	
		if (hidden)
		{
			titles[i].innerHTML = "Navigation &#9658";
		    elts[i].style.display = 'none';
		}
		else
		{
			titles[i].innerHTML = 'Navigation &#9660';
		    elts[i].style.display = 'inherit';
		}
	}
}


function loadExampleBoard(board)
{
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
	if (board == null)
	{
		board = evilExample;
	}
	for (i = 0; i < 9; i++)
	{
		for (j = 0; j < 9; j++)
		{
			if (board[i][j] != null && board[i][j] != 0)
			{
				document.getElementById('sq'+(i*9+j)).value = board[i][j];
			}
		}
	}
}

function clearBoard()
{
	for (i = 0; i < 9; i++)
	{
		for (j = 0; j < 9; j++)
		{
			document.getElementById('sq'+(i*9+j)).value = "";
		}
	}
	document.getElementById('sudokuInfo').innerHTML = "<br/>";
}



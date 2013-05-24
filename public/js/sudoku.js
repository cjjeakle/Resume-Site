function set_9x9(str) { // set the grid given a sudoku string
	if (str != null && str.length >= 81) {
		document.getElementById('9x9info').innerHTML = 'Input or select in the textarea to fill the grid'
		for (var i = 0; i < 81; ++i) document.getElementById('C'+i).value = ''
		for (var i = 0; i < 81; ++i)
			if (str.substr(i, 1) >= 1 && str.substr(i, 1) <= 9)
				document.getElementById('C'+i).value = str.substr(i, 1)
	}
}
function draw_9x9() { // generate the grid and fill it (called "onLoad")
	// generate the grid
	var s = '<table class="table">\n'
	for (var i = 0; i < 9; ++i) {
		s += '<tr>'
		for (var j = 0; j < 9; ++j) {
			var c = 'cell'
			if ((i+1)%3 == 0 && j%3 == 0) c = 'cell3'
			else if ((i+1)%3 == 0) c = 'cell1'
			else if (j%3 == 0) c = 'cell2'
			s += '<td class="' + c + '"><input class="input" type="text" size="1" maxlength="1" id="C' + (i*9+j) + '"></td>';
		}
		s += '</tr>\n'
	}
	s += '</table>'
	document.getElementById('9x9').innerHTML = s
	// fill the grid if the puzzle is given in the URL
	var inp = document.URL
	var set = false
	if (inp.indexOf('?') >= 0) {
		var match = /[?&]q=([^\s&]+)/.exec(inp)
		if (match.length == 2 && match[1].length >= 81) {
			document.getElementById('text').value = match[1]
			set_9x9(match[1])
			set = true
		}
	}
	// if the grid is empty, set the grid with "Easter Monster"
}
function clear_input() {
	document.getElementById('text').value = ''
	document.getElementById('9x9info').innerHTML = 'Input or select in the rextarea to fill the grid'
	for (var i = 0; i < 81; ++i)
		document.getElementById('C'+i).value = ''
}
--></script>

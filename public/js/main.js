$(function()
{

});

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


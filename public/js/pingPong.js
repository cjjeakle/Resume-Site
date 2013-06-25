//Canvas
var canvas = document.createElement("canvas");
var context = canvas.getContext("2d");
canvas.width = 450;
canvas.height = 350;
var div = document.getElementById('pingPong');
div.appendChild(canvas);
div.appendChild(document.createElement("br"));

//Game components (speed is in px per sec)
var aiAccuracy = 1.15; //how accurate predictions are for the AI (1 is real time, 1.5 is psychic more or less)
var aiSpeed = 115; //the speed of the AI's paddle movement, left paddle defaults to 192 
var score = 0;
var then;

var left = {//left paddle
	speed: 192,
	width: 10,
	height: 50,
	x: 0,
	y: 0,
};
var right = {//right paddle
	speed: aiSpeed,
	width: 10,
	height: 50,
	x: canvas.width - 10,
	y: 0,
};
var ball = {
	xSpeed: 128,
	ySpeed: 128,
	width: 15,
	height: 15,
	x: left.width,
	y: canvas.height / 2,
};
var aiBall = {
	xSpeed: (ball.xSpeed * aiAccuracy),
	ySpeed: (ball.ySpeed * aiAccuracy),
	width: ball.width,
	height: ball.height,
	x: left.width,
	y: canvas.height / 2,
};

//Watch for keyboard input
var up = false, dn = false;
addEventListener("keydown", function (e) {
	
    if([38, 40].indexOf(e.keyCode) > -1)
    {
        e.preventDefault(); //prevent arrow key nav on the page
    }
	if(e.keyCode == 38)
	{
		up = true;
	}
	if(e.keyCode == 40)
	{
		dn = true;
	}
}, false);

addEventListener("keyup", function (e) {
	if(e.keyCode == 38)
	{
		up = false;
	}
	if(e.keyCode == 40)
	{
		dn = false;
	}
}, false);

//watch for mouse/touch input
var mouse = false;
var mouseY = 0;
canvas.addEventListener("mousemove", function (e) {
	mouse = true;
	mouseY = e.offsetY; 
}, false);

canvas.addEventListener("mouseout", function (e) {
	mouse = false;
}, false);

//Update game objects
function update (seconds) {
	var positiveSpeed = (ball.xSpeed > 0);
	var inRightCourt = (ball.x > canvas.width / 2);
	
	//update ball locations	
	ball.x += ball.xSpeed * seconds;
	ball.y += ball.ySpeed * seconds;
	aiBall.x += aiBall.xSpeed * seconds;
	aiBall.y += aiBall.ySpeed * seconds;

	//Use keyboard and mouse input
	if (up || (mouse && mouseY <= left.y + (left.height * 3 / 4))) {
		left.y -= left.speed * seconds;
		if (left.y < 0)
		{
			left.y = 0;
		}
	}
	if (dn || (mouse && mouseY >= left.y + (left.height / 4))) {
		left.y += left.speed * seconds;
		if (left.y + left.height > canvas.height)
		{
			left.y = canvas.height - left.height;
		}
	}
	
	simulateAi(seconds);
	
	collisions(ball);
	collisions(aiBall);
	
	//Scoring
	if (ball.x <= 0)
	{
		score -= 1;
		ball.x = (canvas.width - (right.width + ball.width));
		ball.y = Math.floor(Math.random() * canvas.height + 1);
	}
	else if (ball.x >= canvas.width)
	{
		score += 1;
		ball.x = left.width;
		ball.y = Math.floor(Math.random() * canvas.height + 1);
	}
	if ((!positiveSpeed && ball.xSpeed > 0) || 
		(inRightCourt && ball.x < canvas.width / 2 && ball.xSpeed > 0))
	{
		refreshAi();
	}
}

//simulate AI by predicting where the ball will be
function refreshAi()
{
	aiBall.x = ball.x;
	aiBall.y = ball.y;
	aiBall.xSpeed = ball.xSpeed * aiAccuracy;
	aiBall.ySpeed = ball.ySpeed * aiAccuracy;
}

function simulateAi(seconds)
{
	if(aiBall.x + aiBall.width >= canvas.width - right.width)
	{
		aiBall.xSpeed = 0;
		aiBall.ySpeed = 0;
	}
	var diff = (right.y + (right.height / 2) - aiBall.y + (aiBall.height / 2));
	if  (diff >= right.speed * seconds && aiBall.xSpeed >= 0)
	{
		right.y -= right.speed * seconds;
		if (right.y < 0)
		{
			right.y = 0;
		}
	}
	else if (diff < -right.speed * seconds && aiBall.xSpeed >= 0)
	{
		right.y += right.speed * seconds;
		if (right.y + right.height > canvas.height)
		{
			right.y = canvas.height - right.height;
		}
	}
}

function collisions (inputBall)
{
	//Paddle Collisions
	if ((inputBall.x < left.width && (inputBall.y + inputBall.height > left.y) && 
		(inputBall.y <= left.y + left.height)))
	{	
		inputBall.x = left.width;
		inputBall.xSpeed = -inputBall.xSpeed;
	}
	else if (((inputBall.x + inputBall.width > canvas.width - right.width) && 
		(inputBall.y + inputBall.height > right.y) && 
		(inputBall.y <= right.y + right.height)))
	{
		inputBall.x = canvas.width - right.width - inputBall.width;
		inputBall.xSpeed = -inputBall.xSpeed;
	}
	//Ceiling and floor collisions
	if (inputBall.y < 0)
	{
		inputBall.y = 0;
		inputBall.ySpeed = -inputBall.ySpeed;
	}
	else if (inputBall.y + inputBall.height > canvas.height)
	{
		inputBall.y = canvas.height - inputBall.height;
		inputBall.ySpeed = -inputBall.ySpeed;
	}
	return inputBall;
}

//Draw everything
function draw () {
	//Clear the canvas for the next drawing cycle
	context.clearRect(0, 0, canvas.width, canvas.height);
	
	//The left paddle
	context.beginPath();
	context.rect(left.x, left.y, left.width, left.height);
	context.fillStyle = 'black';
	context.fill();
	
	//The right paddle
	context.beginPath();
	context.rect(right.x, right.y, right.width, right.height);
	context.fillStyle = 'black';
	context.fill();
	
	//The ball
	context.beginPath()
	context.rect(ball.x, ball.y, ball.width, ball.height);
	context.fillStyle = 'grey';
	context.fill();
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
	
	//the aiBall, for debugging
	/*
	context.beginPath()
	context.rect(aiBall.x, aiBall.y, aiBall.width, aiBall.height);
	context.fillStyle = 'red';
	context.fill();
	*/
	
	//Score
	context.fillStyle = "#000000";
	context.font = "12px Helvetica";
	context.textAlign = "center";
	context.textBaseline = "top";
	context.fillText("Score: " + score, canvas.width / 2.05, 0);
}

//Game driving function
function pingPong()
{
	var now = Date.now();
	var timer = now - then;
	update(timer / 1000);
	draw();

	right.speed = aiSpeed;
	then = now;
}

//Run the game
function initPingPong()
{
	then = Date.now();
	setInterval(pingPong, 1); //Loop the pingPong() function as quickly as possible
}

//run one iteration of the game to display its starting state
draw();






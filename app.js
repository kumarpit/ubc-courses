const canv = document.getElementById("gameCanvas")
const ctx  = canv.getContext("2d")
const BIRD_RADIUS = 12
const PIPE_SPEED = 2
const PIPE_WIDTH = 30
const MAX_FALL_SPEED = 10
const GAP = 120
const GRAVITY = 0.3
const JUMP = 5
const MIN_TOP_HEIGHT = 10
let pipes = []

//define classes
class Bird{
	constructor(x, y){
		this.x = x;
		this.y = y;
		this.r = BIRD_RADIUS;
		this.fallSpeed = 0
	}
	drawBird(){
		ctx.fillStyle = "rgb(255, 0, 100)"
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
		ctx.fill();
		ctx.fillStyle = "blue"
		ctx.fillRect(this.x, this.y, 1, 1)
	}
	fall(){
		if(this.fallSpeed < MAX_FALL_SPEED){
			this.fallSpeed += GRAVITY
		}
		this.y += this.fallSpeed
	}
	jump(){
		if(this.y > 0){
			this.fallSpeed = -JUMP
		}
		this.y += this.fallSpeed
	}
}

class Pipe{
	constructor(){
		this.top = Math.random() * canv.height / 2 + MIN_TOP_HEIGHT;
		this.bottom = this.top + GAP
		this.x = canv.width + PIPE_WIDTH
		this.color = "white"
	}
	drawPipe(){
		ctx.fillStyle = this.color
		ctx.fillRect(this.x, 0, PIPE_WIDTH, this.top)
		ctx.fillRect(this.x, this.bottom, PIPE_WIDTH, canv.height - this.bottom)
	}
	movePipe(){
		this.x -= PIPE_SPEED
	}
	hits(bird){
		if((bird.y - bird.r < this.top || bird.y + bird.r > this.bottom) && 
		   (bird.x + bird.r > this.x && !(bird.x - bird.r > this.x + PIPE_WIDTH))){
			return true
		}
	}
}

let lastTime = 0
let deltaTime = 0
let spawnInterval = 2000
let spawnCounter = 0

//main game loop
function update(time){
	if(time){
		deltaTime = time - lastTime
		lastTime = time
		spawnCounter += deltaTime

		if(spawnCounter > spawnInterval){
			pipes.push(new Pipe)
			spawnCounter = 0
		}
	}

	ctx.fillStyle = "#333"
	ctx.fillRect(0, 0, canv.width, canv.height)

	//move the bird - gravity, jump
	if(bird.y <= canv.height - bird.r){
		bird.fall()
	}

	//move the pipes, remove if they go beyond screen
	// check colision between bird and pipes
	for(let i = pipes.length - 1; i >= 0; i--){
		if(pipes[i].x + PIPE_WIDTH < 0){
			pipes.splice(i, 1)
		}else pipes[i].movePipe()

		if(pipes[i].hits(bird)){
			console.log("hit")
			pipes[i].color = "red"
		} else pipes[i].color = "white"
	}

	//draw the pipes, bird
	bird.drawBird()
	pipes.forEach(pipe => {
		pipe.drawPipe()
	})

	requestAnimationFrame(update)
}

//initialize game
let bird = new Bird(BIRD_RADIUS*4, canv.height/2)
pipes.push(new Pipe)

document.addEventListener("keydown", e => {
	if(e.keyCode == 32){
		bird.jump()
	}
})

window.requestAnimationFrame(update)



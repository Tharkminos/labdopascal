let x = 0;
let y = 0;

function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(100,170,200);
  x += frameRate()/240
  
  fill(60,130,160)
  rect(0,0,400,50)
  fill(80,150,180)
  rect(0,50,400,50)
  fill("#FFDD00")
  circle(0,0,200);
  fill("#FFFFFFF")
  noStroke();
  
  circle(-50+x,100,75)
  circle(0+x,100,75)
  
  fill("#AA2235")
  triangle(0,400,300,150,450,300);
  fill("#FFFFFFF")
  circle(200+x,100+75,75)
  circle(250+x,100+75,75)
  fill("#66AA66")
  rect(0,300,400,400)
  if (x>600){
  x = -20 
  }
}


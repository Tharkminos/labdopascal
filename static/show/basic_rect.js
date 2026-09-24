function basic_rect(sim){
let x = 200;
let y = 200;
let ad_x = 0;
let ad_y = 0;
let size_x = 50
let size_y = 50
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,450)
}
sim.draw = function(){
if (sim.mouseIsPressed === true && sim.mouseY>0 && sim.mouseY<500) {
    x = sim.constrain(sim.mouseX,0,400)
    y = sim.constrain(sim.mouseY,50,450)
    ad_x = 5-Math.floor(sim.mouseX)%5
    ad_y = 5-Math.floor(sim.mouseY)%5
}


sim.background(220);
sim.fill(200,150,80);

sim.rect(x,y,size_x,size_y)
sim.fill(255);
sim.noStroke();
sim.rect(0,0,400,50)
sim.stroke(0);
sim.fill(0);
sim.textSize(18)

string = "rect("+Math.floor(x+ad_x-5)+","+Math.floor(y-50+ad_y-5)+","+size_x+","+size_y+")"
sim.text(string,100,20)
}
sim.keyPressed = function(){
if (sim.keyCode === 37) { // Left arrow key
    size_x+=5;
  } else if (sim.keyCode === 39) { // Right arrow key
    size_x-=5;
  }
if (sim.keyCode === 38) { // Up arrow key
    size_y+=5;
  } else if (sim.keyCode === 40) { // Down arrow key
    size_y-=5;
  }
    
}

  
}

function basic_circle(sim){
let x = 0;
let y = 0;
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,500)
}
sim.draw = function(){
sim.background(220);
sim.fill(0);
if (sim.mouseIsPressed === true) {
    x = sim.mouseX
    y = sim.mouseY
  } 
sim.circle(x,y,50)
sim.fill(255);
sim.noStroke();
sim.rect(0,0,400,100)
sim.stroke(0);
    sim.fill(0);
sim.textSize(18)
string = "circle("+Math.floor(x)+","+Math.floor(y-100)+",50)"
sim.text(string,100,20)
}
}

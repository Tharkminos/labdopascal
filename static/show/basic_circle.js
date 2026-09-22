function basic_circle(sim){
let x = 200;
let y = 200;
let ad_x = 0;
let ad_y = 0;
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,450)
}
sim.draw = function(){
ad_x = Math.floor(x)%5
ad_y = Math.floor(y)%5
sim.background(220);
sim.fill(200,150,80);
if (sim.mouseIsPressed === true) {
    x = sim.mouseX+ad_x
    y = sim.mouseY+ad_y
  } 
sim.circle(x,y,50)
sim.fill(255);
sim.noStroke();
sim.rect(0,0,400,100)
sim.stroke(0);
sim.fill(0);
sim.textSize(18)

string = "circle("+Math.floor(x+ad_x)+","+Math.floor(y-50+ad_y)+",50)"
sim.text(string,100,20)
}
}

function basic_triang(sim){
let x1 = 150;
let y1 = 100;
let x2 = 250;
let y2 = 100;
let x3 = 200;
let y3 =  50;

let p1 = 100
let p2 = 100
let p3 = 100
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,450)
}
sim.draw = function(){
sim.background(220);
sim.fill(200,150,80);
p1 = sim.dist(x1,y1,sim.mouseX,sim.mouseY);
p2 = sim.dist(x1,y1,sim.mouseX,sim.mouseY);
p3 = sim.dist(x1,y1,sim.mouseX,sim.mouseY);
if(sim.mouseIsPressed===true){
  if(p1<20){
    x1 = sim.mouseX +5-Math.floor(sim.mouseX)%5
    y1 = sim.mouseY +5-Math.floor(sim.mouseY)%5
  }
  if(p2<20){
    x2 = sim.mouseX +5-Math.floor(sim.mouseX)%5
    y2 = sim.mouseY +5-Math.floor(sim.mouseY)%5
  }
  if(p1<20){
    x3 = sim.mouseX +5-Math.floor(sim.mouseX)%5
    y3 = sim.mouseY +5-Math.floor(sim.mouseY)%5
  }
}
sim.fill(255);
sim.noStroke();
sim.rect(0,0,400,50)
sim.stroke(0);
sim.fill(0);
sim.textSize(18)
sim.fill(200,0,0);
sim.circle(x1,y1,20);
sim.circle(x2,y2,20);
sim.circle(x3,y3,20);
sim.fill(0,200,0);
sim.triangle(x1,y1,x2,y2,x3,y3)
string = "triangle("+x1+","+y1+","+x2+","+y2+","+x3+","+x3+")"
sim.text(string,100,20)
}


  
}

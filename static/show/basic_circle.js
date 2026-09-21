function basic_circle(sim){
let x = 0;
let y = 0;
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,500)
}

sim.draw = function(){
x = sim.mouseX
y = sim.mouseY
sim.background(220);
sim.circle(x,y,50)
sim.textSize(18)
string = "circle("+Math.floor(x)+","+Math.floor(y)+50+",50)"
sim.text(string,175,20)
}
}

function basic_circle(sim){
let x = 0;
let y = 0;
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,500)
}

sim.draw = function(){
x = mouseX
y = mouseY
sim.background(220);
string = "circle("+x+","+y+")"
text("circle({x},{y})")
}
}

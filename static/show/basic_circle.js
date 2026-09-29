function basic_circle(sim){
let x = 200;
let y = 200;
let radius = 50
let ad_x = 0;
let ad_y = 0;
let string = "";
sim.setup = function(){
sim.canvas = sim.createCanvas(400,450)
}
sim.draw = function(){
if (sim.mouseIsPressed === true && sim.mouseY < 500 && sim.mouseY>0) {
    x = sim.constrain(sim.mouseX,0,400)
    y = sim.constrain(sim.mouseY,50,450)
    ad_x = 5-Math.floor(sim.mouseX)%5
    ad_y = 5-Math.floor(sim.mouseY)%5
}

if(sim.mouseIsPressed === true){
    if(sim.mouseX>410 && sim.mouseX<410-25 && sim.mouseY>50 && sim.mouseY < 50+25){
     radius+=1   
    }
    if(sim.mouseX>410 && sim.mouseX<410-25 && sim.mouseY>80 && sim.mouseY < 80+25){
     radius+=-1   
    }
    
}

sim.background(220);
sim.fill(200,150,80);

sim.circle(x,y,radius)
sim.fill(255);
sim.noStroke();
sim.rect(0,0,400,50)
sim.stroke(0);
sim.fill(0);
sim.textSize(18)

string = "circle("+Math.floor(x+ad_x-5)+","+Math.floor(y-50+ad_y-5)+","+radius+")"
sim.text(string,100,20)
sim.fill(200);
sim.fill(0);

}
    
sim.keyPressed = function(){
if (sim.keyCode === 38) { // Up arrow key
    radius+=5;
  } else if (sim.keyCode === 40) { // Down arrow key
    radius-=5;
  }
}

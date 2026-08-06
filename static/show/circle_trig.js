function circle_trig(sim) {

let alpha = 0
let X = 200
let Y = 200
let mode = 3
let work  = [false,false,false,false]
let pressed = false
rad = function(angle){
  return angle*3.14159265358979/180
}
deg = function(angle){
  return angle*180/3.14159265358979
}

sim.setup = function() {
    sim.canvas = sim.createCanvas(400, 400);
  
};
sim.simulacaoConcluida = function(){
  return true
}
sim.draw = function() {
    if(sim.mouseIsPressed === false){
      pressed = false
    }
    sim.background(220);
    sim.fill(220)
    sim.circle(X,Y,200) 
    sim.fill(0)
    sim.line(0,200,400,200)
    sim.line(200,0,200,400)
    sim.textSize(15)
    sim.text("x = cos(α)",325,195)
    sim.text("y = sin(α)",205,25)
    sim.triangle(300+5,205,300+5,195,320+5,200)
    sim.triangle(195,100-5,205,100-5,200,80-5)
    if(work[3]){
      alpha -= rad(1)
      }
    if(alpha<-2*3.14159265358979424){
      alpha=0
    }
    sim.textSize(24)
    sim.text("α:"+String(-1*Math.floor(deg(alpha)))+'º',0,20)
    if(work[0]){
      sim.fill(255,90,90)
      sim.stroke(255,90,90)
      sim.line(X+100*Math.cos(alpha),Y,X,Y)  
    sim.stroke(0)

      sim.circle(X+100*Math.cos(alpha),Y,15)
    }if(work[1]){
      sim.fill(90,90,255)
      sim.stroke(90,90,255)
      sim.line( X,
             Y,
             X,
             Y+100*Math.sin(alpha))
      sim.stroke(0)
sim.circle(X,Y+100*Math.sin(alpha),15)
      
    }if(work[2]){
      sim.fill(255+90/2,90,255+90/2)
              sim.circle(X+100*Math.cos(alpha),Y+100*Math.sin(alpha),15)
    }
    sim.fill(255-work[0]*50,90,90)
    sim.rect(5,350,100,30)
    if(sim.mouseIsPressed && sim.mouseX >5 && sim.mouseX < 100  &&  sim.mouseY >350 && sim.mouseY < 380 && pressed === false){
      work[0] = !work[0]
      pressed = true
    }if(sim.mouseIsPressed && sim.mouseX >120 && sim.mouseX < 220  &&  sim.mouseY >350 && sim.mouseY < 380 && pressed === false){
      work[1] = !work[1]
      pressed = true
    }if(sim.mouseIsPressed && sim.mouseX >5+115*3  &&  sim.mouseY >350 && sim.mouseY < 400 && pressed === false){
      work[3] = !work[3]
      pressed = true
      
    }
  if(sim.mouseIsPressed && sim.mouseX >120+115 && sim.mouseX < 220+115  &&  sim.mouseY >350 && sim.mouseY < 380 && pressed === false){
      work[2] = !work[2]
      pressed = true
    }
    sim.fill(90,90,255-work[1]*50)
    sim.rect(5+115,350,100,30)
    sim.fill(255-work[2]*50,90,255-work[2]*50)
    sim.rect(5+115*2,350,100,30)
    sim.fill(90,255-work[3]*50,90)
    sim.rect(5+115*3,350,30)
    sim.fill(0)
    sim.text("cos(α)",25,372)
    sim.text("sin(α)",25+115,372)
    sim.text("ambos",25+2*112,372)
    if(work[3]){
    sim.text("ǀǀ",23+3*112,374)
    }else{
    sim.text("»",23+3*112,372)
    }
    if(work[2] === true){
    sim.stroke(255,90,90,255*work[0])  
    sim.line(X+100*Math.cos(alpha),
             Y+100*Math.sin(alpha),
             X,
             Y+100*Math.sin(alpha))
    sim.stroke(90,90,255,255*work[1])  
    sim.line(X+100*Math.cos(alpha),Y+100*Math.sin(alpha),X+100*Math.cos(alpha),Y)  
    }
    sim.stroke(0)
    
}; // DRAW
};

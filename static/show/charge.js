function setup() {
  canvas = createCanvas(300,400)
  canvas.parent('canvas-charge')
}
let grid = []
let cable1 = [[50,240],[50,120],[143,120]]
let cable2 = [[155,136],[155,210],[103,210],[103,246]]
let path = [[50,240],[50,120],[143,120],[143,50],[155,50],[155,136],[155,210],[103,210],[103,246]]
function mouseClicked(){  
  console.log(mouseX,mouseY)
}
function battery(x,y){
  fill(255,140,60);
  rect(x,y,100,125)
  fill(0,0,0)
  rect(x,y+45,100,80)
  fill(120)
  rect(x+18,y-10,15,10)
  rect(x+10,y-15,20,10)
  rect(x+20,y-15,15,10)
  rect(x+30,y-15,10,10)
  rect(x+68,y-15,20,15)
  fill(0)
  textSize(30)
  text("+",x+70,y+25)
  textSize(50)
  text("-",x+20,y+30)
  return [[x+20,y-15],[x+68,y-15]] 

}
function led(x,y,state,size,time,volt){
  stroke(0,0,0,0)
  if(state===true){
    fill(255,0,0,30) // Luz
    arc(x, y+20*size, 50, 100*(1+0.1*abs(cos(time))), PI+0.1, -0.1);
    arc(x, y+20*size, 100,120*(1+0.1*abs(cos(time))), PI+0.1, -0.1);
    arc(x, y+20*size, 150,180*(1+0.1*abs(cos(time))), PI+0.1, -0.1);
    
  }
  fill(255,64,64)
  circle(x,y,20*size)
  
  
  
  rect(x-20*size/2,y,20*size)
  rect(x-20*size/2,y-20*size/2,8*size,10*size)
  fill(128,0,0,128)
  // TOPO LED /\
  fill(128)
  rect(x+2*size,y+20*size,3*size,50*size) //perna anodo
  rect(x-6*size,y+20*size,3*size,40*size) //perna catodo
  
  //led interno
  fill(128,0,0,128)
  rect(x-6*size,y,7*size,20*size)
  rect(x+2*size,y,3*size,20*size)
    stroke(0)

}
function drawCable(corners,color){
  for (let i = 0; i < corners.length ; i++ ){
    if(i>0){
       stroke(color)
       strokeWeight(5)
       line(corners[i-1][0],corners[i-1][1],corners[i][0],corners[i][1])
       strokeWeight(1)
       stroke(0)
    }
  }
}
function drawCharge(corners, charges){
  let isLed = false
  
  for(let charge of charges){
    if (charge[2]>2 && charge[2]<5){
      isLed = true
    }
    fill(120,120,255);
    let index = charge[2];

    if(index >= corners.length - 1){
    charge[2] = 0;
    charge[0] = corners[0][0];
    charge[1] = corners[0][1];

    index = 0;
    }

    let p1 = corners[index];
    let p2 = corners[index + 1];

    // Movimento vertical
    if(charge[0] === p2[0] && charge[1] !== p2[1]){
      let a = 0;

      if(p1[1] > p2[1]) a = -1;
      if(p1[1] < p2[1]) a = 1;

      charge[1] += a;
    }

    // Movimento horizontal
    if(charge[0] !== p2[0] && charge[1] === p2[1]){
      let b = 0;

      if(p1[0] > p2[0]) b = -1;
      if(p1[0] < p2[0]) b = 1;

      charge[0] += b;
    }

    // Chegou ao próximo vértice
    if(charge[0] === p2[0] && charge[1] === p2[1]){
      charge[2]++;
    }
    if (charge[1]<250) {
    circle(charge[0], charge[1], 20);
    fill(0)
    rect(charge[0]-4,charge[1]-1,8,2)
    
    }
  }

  return isLed;
}
let charges = []
let time = 0
let x_battery = 0
let y_battery = 0
let x_led     = 0
let y_led     = 0
let led_on = false
let init_cond = true
let n = 14// Nº de Cargas
function draw() {
  if(init_cond === true){
    for(let i = 0; i<n ; i++ ){
      charges.push([50,260+3+i*40,0])
    }
     init_cond = false
  }
  background(255);
  drawCable(cable1,[  0,  0,  0])
  drawCable(cable2,[255,  0,  0])
  led(150,30,led_on,1.5,time,9)
  led_on = drawCharge(path,charges)
  battery(25,250)

}       

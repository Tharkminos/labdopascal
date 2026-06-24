
function setup() {
  canvas = createCanvas(350, 500);
  canvas.parent("canvas-atom");
}
let pi = 3.14
let atoms = [[207,200,''],
            [155,200,'+'],
            [180,176,''],
            [180,225,'+'],
            [0,0,''],
            [0,0,'+'],
            [0,0,'+']
]
let finished = false

function simulacaoConcluida(){

    return finished

}
function mouseClicked(){
  Mx = mouseX
  My = mouseY
  for(var at of atoms){
    Obx = at[0]
    Oby = at[1]
    dS =  dist(Mx,My,Obx,Oby)
    if(dS < 10){
      if(at[2]==='+'){
        interact[0] = true
      }if(at[2]===''){
        interact[1] = true
      }
    }
  }
  let k = 0
  for(let i = 0;i<11; i++){    if(i<2){
    x = 180+90*sin(i*3.14+angle)
    y = 200+90*cos(i*3.14+angle)
    textSize(50)
      }
    if(i>2){
    x = 180-140*sin(i*3.14/4+angle)
    y = 200+140*cos(i*3.14/4+angle)
    }
    dS =  dist(Mx,My,x,y)
    if(dS<20){interact[2]= true}
    fill(120,120,255)
    circle(x,y,22)
    fill(0)
    text("-",x-8,y+12);
  }
  }
let angle=0
let x = 0
let y = 0
let back = 220
let tx = 100
let ty = 375
let nucleus_radio = 24
let interact = [false,false,false] // Mostra se interagiu com o átomo
function draw() {
  
  for(let n= 0 ; n < 7 ;n++){ 
    if(n < 6){
      atoms[n][0] = 180+nucleus_radio*sin(n-1*3.14/3) || 0
      atoms[n][1] = 200+nucleus_radio*cos(n-1*3.14/3) || 0   
       }else{
         atoms[n][0] = 180
         atoms[n][1] = 180+20
       }
    
  }

  back = 255
  background(back);
  fill(back)
  circle(180,200,280)
  circle(180,200,180)

  angle += 0.03
  for(let j=0; j<atoms.length;j++){
      if (atoms[j][2]==='+'){
      fill(255,120,120)
    } if (atoms[j][2]===''){
      fill(200,120,200)
    } if (atoms[j][2]==='-'){
      fill(100,100,255)
    }
    circle(atoms[j][0],atoms[j][1],30)
    fill(0)
    textSize(30)
    text(atoms[j][2],atoms[j][0]-8,atoms[j][1]+10)
  }
  let k = 0
  for(let i = 0;i<11; i++){    if(i<2){
    x = 180+90*sin(i*3.14+angle)
    y = 200+90*cos(i*3.14+angle)
    textSize(50)
      }
    if(i>2){
    x = 180-140*sin(i*3.14/4+angle)
    y = 200+140*cos(i*3.14/4+angle)
    }
    fill(120,120,255)
    circle(x,y,22)
    fill(0)
    text("-",x-8,y+12);
  } // Atomo
  if (interact[0]===true){
    textSize(24)
    fill(255,120,120)
    circle(tx,ty,30)
    fill(0)
    
    textSize(30)
    text("+",tx-8,ty+10)
    textSize(24)
    text("→",tx+20,ty+5)
    text(" Próton",tx+35,ty+10)
  }if (interact[1]===true){
    textSize(24)
    fill(200,120,200)
    circle(tx,ty+40,30)
    fill(0)
    text("→",tx+20,ty+5+40)
    text(" Neutron",tx+35,ty+10+40)
  }if (interact[2]===true){
    
    fill(120,120,255)
    circle(tx,ty+80,22)
    fill(0)
    textSize(50)
    text("-",tx-8,ty+80+12)
    textSize(24)
    text("→",tx+10,ty+85)
    text(" Elétron",tx+30,ty+10+80)
  }
    if (interact === [true,true,true]){
        finished = true        
    }
  
}


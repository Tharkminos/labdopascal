  function x(value){
    return value + 50
  }
  function y(value){
    return 350-value
  }
  function xy(){
    for(let a=1;a<21;a++){
      line(x(a*15),y(0),x(a*15),y(-5))
      textSize(10)
      if( a % 2 == 0){
      text(a,x(a*15-10),y(-20))
      text(a,x(-20),y(a*15-5))  
      }
      line(x(-5),y(a*15),x(0),y(a*15))
    } text(0,x(-10),y(-13))
  }
  function distance(x1,y1,x2,y2){
    return ((x2-x1)**2+(y2-y1)**2)**0.5
  }
  function setup() {
    createCanvas(400, 400);
  }
  function mouseClicked() {
    if(distance(mouseX,mouseY,215,95) < 20){
      cy = 10*15
      v  = 0
    }
    if(distance(mouseX,mouseY,205+45,98) < 20){
      flag_g = !flag_g
      if(flag_g == false){index = 0}else{index = 1}
    }
    if(distance(mouseX,mouseY,290+15,60+15+20) < 20){
      flag_m = !flag_m
      if(flag_m == false){index2 = 0}else{index2 = 1}
    }


  }

  let cy = 10*15
  let a = 0 // Aceleração
  let g = 1 // Gravidade
  let v = 0 // Velocidade
  let m = 1 // Massa
  let index = 0
  let index2= 0 
  let txt = ["Q","L"]
  let start = [[255,50,50],[50,220,50]]
  let tempo = 5
  let correc = [[10,2],[7,0]]
  let flag_g = false
  let flag_m = false
  let flag_m2= false
  // S = S0 - g*t*t/2

  function draw() {
    background(220);
    fill(0)
    stroke(0,0,0,255)
    textSize(10)
    line(50,350,350,350)
    text("Y",35,45)
    text("X",360,365)
    line(50,350,50,50)
    xy()
    circle(x(150),y(cy+15),30)
    if(flag_g === true){
      if(flag_m === false){
      g = 1
      v += g
      cy = cy -v
         }else{
           v = 5
           g = 0
           cy = cy -v}
    }


    if(cy <= 0.3) {
      cy = 0
      v = -v*0.7
    } 

    textSize(20)
    text('Altura:'+Math.round(cy/15)+'m',200,20)
    if(flag_m === true){v=0}
    text('Velocidade:'+Math.round(v)+'m/s',200,40)
    text("Aceleração:"+Math.round(g*10)+'m/s²',200,60)
    fill(start[index])
    rect(245,60+20,30)

    fill(start[index2])
    rect(290,60+20,30)


    fill(255)
    stroke(0,0,0)
    if(cy != 150){
      fill(50,50,200)}else{fill(150)}
    rect(200,60+20,30)  
    fill(255)
    text("A",208,81+20)
    text("→",205+45,78+20)

    if(flag_m === true){}

    text(txt[index2],200+90+correc[index2][0],80+correc[index2][1]+20)



  }

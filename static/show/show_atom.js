
function seno(angle){
  return Math.sin(angle)
}
function cos(angle){
  return Math.cos(angle)
}
function show_atom(sim) {
    let x = 100;
    let y = 100;
    let angle=0
    let pi = 3.14
let atoms = [[207,200,''],
            [155,200,'+'],
            [180,176,''],
            [180,225,'+'],
            [0,0,''],
            [0,0,'+'],
            [0,0,'+']
]
let nucleus_radio = 24
sim.simulacaoConcluida = function (){return true}
sim.setup = function () {
        sim.canvas = sim.createCanvas(370, 370);
        sim.canvas.parent("canvas-show_atom");

    };

sim.draw = function () {
        sim.simulacaoConcluida()
        sim.fill(220)
        sim.background(220)
        sim.circle(180, 200, 280);
        sim.circle(180, 200, 180);
        angle += 0.03
        for(let n= 0 ; n < 7 ;n++){ 
          if(n < 6){
            atoms[n][0] = 180+nucleus_radio*seno(n-1*3.14/3) || 0
            atoms[n][1] = 200+nucleus_radio*cos(n-1*3.14/3) || 0   
             }else{
               atoms[n][0] = 180
               atoms[n][1] = 180+20
             }};
      for(let j=0; j<atoms.length;j++){
        if (atoms[j][2]==='+'){
        sim.fill(255,120,120)
      } if (atoms[j][2]===''){
        sim.fill(200,120,200)
      } if (atoms[j][2]==='-'){
        sim.fill(100,100,255)
      }
      sim.circle(atoms[j][0],atoms[j][1],30)
      sim.fill(0)
      sim.textSize(30)
      sim.text(atoms[j][2],atoms[j][0]-8,atoms[j][1]+10)
    } // FOR LET J
    let k = 0
    for(let i = 0;i<11; i++){    if(i<2){
      x = 180+90*seno(i*3.14+angle)
      y = 200+90*cos(i*3.14+angle)
      sim.textSize(50)
        }
      if(i>2){
      x = 180-140*seno(i*3.14/4+angle)
      y = 200+140*cos(i*3.14/4+angle)
      }
      sim.fill(120,120,255)
      sim.circle(x,y,22)
      sim.fill(0)
      sim.text("-",x-8,y+12);
    } // Atomo  
  } // DRAW
} // SIMULAçÃO


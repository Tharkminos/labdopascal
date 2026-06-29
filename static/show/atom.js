function criarSimulacao(sim){

let pi = 3.14;

let atoms = [
    [207,200,''],
    [155,200,'+'],
    [180,176,''],
    [180,225,'+'],
    [0,0,''],
    [0,0,'+'],
    [0,0,'+']
];

let finished = false;
let contabilizada = false;

let angle = 0;
let x = 0;
let y = 0;
let back = 220;
let tx = 100;
let ty = 375;
let nucleus_radio = 24;

let interact = [false,false,false];

sim.simulacaoConcluida = function(){
    return finished;
}

sim.setup = function(){

    sim.canvas = sim.createCanvas(350,500);
    sim.canvas.parent("canvas-atom");

}

sim.mouseClicked = function(){

    let Mx = sim.mouseX;
    let My = sim.mouseY;

    for(let at of atoms){

        let Obx = at[0];
        let Oby = at[1];

        let dS = sim.dist(Mx,My,Obx,Oby);

        if(dS < 10){

            if(at[2] === '+'){
                interact[0] = true;
            }

            if(at[2] === ''){
                interact[1] = true;
            }

        }

    }

    for(let i=0;i<11;i++){

        if(i<2){

            x = 180+90*Math.sin(i*pi+angle);
            y = 200+90*Math.cos(i*pi+angle);

        }

        if(i>2){

            x = 180-140*Math.sin(i*pi/4+angle);
            y = 200+140*Math.cos(i*pi/4+angle);

        }

        let dS = sim.dist(Mx,My,x,y);

        if(dS<20){
            interact[2]=true;
        }

    }

}

sim.draw = function(){

    for(let n=0;n<7;n++){

        if(n<6){

            atoms[n][0]=180+nucleus_radio*Math.sin(n-pi/3);
            atoms[n][1]=200+nucleus_radio*Math.cos(n-pi/3);

        }else{

            atoms[n][0]=180;
            atoms[n][1]=200;

        }

    }

    back=255;

    sim.background(back);

    sim.fill(back);
    sim.circle(180,200,280);
    sim.circle(180,200,180);

    angle+=0.03;

    for(let j=0;j<atoms.length;j++){

        if(atoms[j][2]==='+') sim.fill(255,120,120);
        if(atoms[j][2]==='') sim.fill(200,120,200);
        if(atoms[j][2]==='-') sim.fill(100,100,255);

        sim.circle(atoms[j][0],atoms[j][1],30);

        sim.fill(0);
        sim.textSize(30);
        sim.text(atoms[j][2],atoms[j][0]-8,atoms[j][1]+10);

    }

    for(let i=0;i<11;i++){

        if(i<2){

            x=180+90*Math.sin(i*pi+angle);
            y=200+90*Math.cos(i*pi+angle);

            sim.textSize(50);

        }

        if(i>2){

            x=180-140*Math.sin(i*pi/4+angle);
            y=200+140*Math.cos(i*pi/4+angle);

        }

        sim.fill(120,120,255);
        sim.circle(x,y,22);

        sim.fill(0);
        sim.text("-",x-8,y+12);

    }

    if(interact[0]){

        sim.textSize(24);

        sim.fill(255,120,120);
        sim.circle(tx,ty,30);

        sim.fill(0);

        sim.textSize(30);
        sim.text("+",tx-8,ty+10);

        sim.textSize(24);
        sim.text("→",tx+20,ty+5);
        sim.text(" Próton",tx+35,ty+10);

    }

    if(interact[1]){

        sim.textSize(24);

        sim.fill(200,120,200);
        sim.circle(tx,ty+40,30);

        sim.fill(0);

        sim.text("→",tx+20,ty+45);
        sim.text(" Neutron",tx+35,ty+50);

    }

    if(interact[2]){

        sim.fill(120,120,255);
        sim.circle(tx,ty+80,22);

        sim.fill(0);

        sim.textSize(50);
        sim.text("-",tx-8,ty+92);

        sim.textSize(24);
        sim.text("→",tx+10,ty+85);
        sim.text(" Elétron",tx+30,ty+90);

    }

    if(interact[0] && interact[1] && interact[2]){

        finished = true;

        if(!contabilizada){

            acertos++;
            contabilizada = true;

        }

    }

}

}
let simulacaoAtual = p5(criarSimulacao)

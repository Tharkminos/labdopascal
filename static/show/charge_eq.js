function charge_eq(sim){

let atoms = [];
let rects = [];

let n_e = 10;
let n_p = 2;
let nucleo = 7;

let angle = 0;
let new_angle = 0;

let bc = [[255,255,255],[255,80,80],[80,255,80]];
let bci = 0;

let answers = [3,4,5,6,7,8,9,10];
let index = 0;

let finished = false;
let contabilizada = false;

const nucleus_radio = 24;

function rectangle(x,y,sz,n){

    sim.fill(70);
    sim.rect(x,y,sz[0],sz[1]);

    sim.fill(255);
    sim.stroke(0);
    sim.textSize(50);

    if(n>9){

        sim.text(n,x+sz[0]/8,y+sz[1]/1.25);

    }else{

        sim.text(n,x+sz[0]/3,y+sz[1]/1.25);

    }

}

sim.simulacaoConcluida = function(){

    return finished;

}

sim.setup = function(){

    sim.canvas = sim.createCanvas(350,600);
    sim.canvas.parent("canvas-charge_eq");

    sim.shuffle(answers,true);

    for(let count=0;count<3;count++){

        n_p = sim.floor(sim.random(3,7));
        rects.push([350*count/3+21,450,answers[count],[75,60]]);

    }

    for(let i=0;i<nucleo;i++){

        if(i<n_p){

            atoms.push([0,0,"+"]);

        }else{

            atoms.push([0,0,""]);

        }

    }

    sim.shuffle(atoms,true);

    index = sim.floor(sim.random(0,3));

    if(![answers[0],answers[1],answers[2]].includes(n_p)){

        rects[index][2]=n_p;

    }

    rects.push([21,520,"→",[75*4.1,60]]);

}

sim.mouseClicked = function(){

    let Mx = sim.mouseX;
    let My = sim.mouseY;

    for(let ret of rects){

        let x = ret[0];
        let y = ret[1];

        if(Mx>=x &&
           Mx<=x+ret[3][0] &&
           My>=y &&
           My<=y+ret[3][1]){

            if(!isNaN(ret[2])){

                n_e = ret[2];
                bci = 0;

            }else{

                if(n_e===n_p){

                    bci = 2;
                    finished = true;

                    if(!contabilizada){

                        acertos++;
                        contabilizada = true;

                    }

                }else{

                    bci = 1;

                }

            }

        }

    }

}

sim.draw = function(){

    for(let n=0;n<7;n++){

        if(n<6){

            atoms[n][0]=180+nucleus_radio*Math.sin(n-Math.PI/3);
            atoms[n][1]=250+nucleus_radio*Math.cos(n-Math.PI/3);

        }else{

            atoms[n][0]=180;
            atoms[n][1]=250;

        }

    }

    sim.background(bc[0]);

    sim.fill(bc[bci]);
    sim.circle(180,250,280);
    sim.circle(180,250,180);

    angle += 0.03;

    for(let atom of atoms){

        if(atom[2]==="+"){

            sim.fill(255,120,120);

        }else if(atom[2]===""){

            sim.fill(200,120,200);

        }else{

            sim.fill(100,100,255);

        }

        sim.circle(atom[0],atom[1],30);

        sim.fill(0);
        sim.textSize(30);
        sim.text(atom[2],atom[0]-8,atom[1]+10);

    }

    for(let i=0;i<n_e+1;i++){

        let x,y;

        new_angle=i*2*Math.PI/(n_e-2);

        if(i<2){

            x=180+90*Math.sin(i*Math.PI+angle);
            y=250+90*Math.cos(i*Math.PI+angle);

        }

        if(i>=2){

            x=180-140*Math.sin(new_angle+angle);
            y=250+140*Math.cos(new_angle+angle);

        }

        sim.fill(120,120,255);
        sim.circle(x,y,22);

        sim.fill(0);
        sim.text("-",x-6,y+8);

    }

    sim.textSize(25);
    sim.text(" Equilibre a carga do átomo\n abaixo:",0,30);

    for(let ret of rects){

        rectangle(ret[0],ret[1],ret[3],ret[2]);

    }

}

}



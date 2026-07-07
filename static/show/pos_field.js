function pos_field(sim){

let grid = [];

let charges = [
    [6,10,7,"+"],
    [14,10,7,"-"]
];

let row = [];

let grid_div = 5;
let grid_size = 20;

sim.simulacaoConcluida = function(){

    return false;

}

function Ini(){

    for(let i=0;i<(400/grid_div);i++){

        row = [];

        for(let j=0;j<(400/grid_div);j++){

            row.push([0,0,""]);

        }

        grid.push(row);

    }

}

function field(){

    for(let a=0;a<grid.length;a++){

        for(let b=0;b<grid[a].length;b++){

            grid[a][b][0]=0;
            grid[a][b][1]=0;
            grid[a][b][2]="";

        }

    }

    for(let index in charges){

        const i = charges[index][0];
        const j = charges[index][1];
        const raio = charges[index][2];

        for(let a=0;a<grid.length;a+=2){

            for(let b=0;b<grid[a].length;b+=2){

                if(sim.dist(a*grid_size,b*grid_size,i*grid_size,j*grid_size)<=raio*grid_size){

                    grid[i][j][2]=charges[index][3];

                    let dx=(a-i)*grid_size;
                    let dy=(b-j)*grid_size;
                    let d=Math.sqrt(dx*dx+dy*dy);

                    if(d!==0){

                        let mult = charges[index][3]==="+" ? 1 : -1;

                        grid[a][b][0]+=mult*dx/d;
                        grid[a][b][1]+=mult*dy/d;

                    }

                }

            }

        }

    }

}

function paint2(){

    const m = grid_size/2;

    for(let i=0;i<grid.length;i++){

        for(let j=0;j<grid[i].length;j++){

            const x=i*grid_size;
            const y=j*grid_size;

            let check=false;
            let ch="";

            sim.fill(255);
            sim.stroke(0);

            const vx=grid[i][j][0];
            const vy=grid[i][j][1];

            if(grid[i][j][2]==="+"){

                sim.fill(255,90,90);
                ch="+";
                check=true;

            }

            if(grid[i][j][2]==="-"){

                sim.fill(90,90,255);
                ch="-";
                check=true;

            }

            if(vx===0 && vy===0 && !check){

                continue;

            }

            sim.push();

            if(!check){

                const ang = Math.atan2(vy,vx);
                const mag = Math.sqrt(vx*vx + vy*vy);
                let px = x + m;
                let py = y + m;
                if(mag > 0){
                    px += (vx / mag) * flow;
                    py += (vy / mag) * flow;

                }
                sim.translate(px,py);
                sim.rotate(ang);


                sim.fill(0);
                sim.noStroke();

                sim.rect(-m,-m*0.08,m*1.56,m*0.16);

                sim.triangle(
                    0.8*m,0,
                    0.2*m,-0.5*m,
                    0.2*m,0.5*m
                );

            }

            sim.pop();

            if(check){

                sim.circle(x+grid_size/2,y+grid_size/2,grid_size*3);

                sim.fill(0);

                if(ch==="-" ){

                    sim.textSize(28);
                    sim.text(ch,x+grid_size/4,y+grid_size/1.2);

                }else{

                    sim.textSize(24);
                    sim.text(ch,x+grid_size/6,y+grid_size/1.2);

                }

            }

        }

    }

}

sim.setup = function(){

    sim.canvas = sim.createCanvas(400,400);

    if(document.getElementById("canvas-pos_field")){

        sim.canvas.parent("canvas-pos_field");

    }

    Ini();

}

sim.mouseClicked = function(){

}
let flow = 0;
sim.draw = function(){
    flow += 0.8;
    if(flow > grid_size * 2){
        flow = 0;
    }
    sim.background(220);

    field();

    paint2();

}

}

function pos_field(sim){

let cargas = [
    {
        sinal:"-",
        x:100,
        y:201,
        carga:100
    },
    {
        sinal:"-",
        x:300,
        y:199,
        carga:100
    }
];

let vetores = [];

let time = 0;

sim.simulacaoConcluida = function(){

    return true;

}

sim.setup = function(){

    sim.canvas = sim.createCanvas(400,400);
    sim.canvas.parent("canvas-pos_field");

    add(6);

}

sim.draw = function(){

    time++;

    sim.background(220);

    drawVectors();
    drawCargas();

    if(time > 50){

        add(6);
        time = 0;

    }

    let temp = [...vetores];

    const any_anion = ifAny("-");
    const any_cation = ifAny("+");

    for(const carga of cargas){

        for(let v=temp.length-1;v>=0;v--){

            const dx = carga.x-temp[v].x;
            const dy = carga.y-temp[v].y;

            const S = Math.sqrt(dx*dx+dy*dy);

            if(S < 15 && carga.sinal === "-"){

                temp.splice(v,1);

            }

            if(S > 330 && !any_anion){

                temp.splice(v,1);

            }

        }

    }

    vetores = temp;

}

function add(n){

    const any_cation = ifAny("+");

    for(const q of cargas){

        for(let i=0;i<=n;i++){

            if(q.sinal === "+"){

                vetores.push({
                    x:q.x+15*Math.sin(i*2*Math.PI/n),
                    y:q.y+15*Math.cos(i*2*Math.PI/n),
                    trail:[]
                });

            }

            if(!any_cation){

                vetores.push({
                    x:q.x+160*Math.sin(i*2*Math.PI/n),
                    y:q.y+160*Math.cos(i*2*Math.PI/n),
                    trail:[]
                });

            }

        }

    }

}

function ifAny(sinal){

    for(const carga of cargas){

        if(carga.sinal === sinal){

            return true;

        }

    }

    return false;

}

function drawVectors(){

    for(const vector of vetores){

        const field = campo(vector.x,vector.y);

        const norma = Math.hypot(field[0],field[1]);

        if(norma === 0) continue;

        vector.trail.push([vector.x,vector.y]);

        if(vector.trail.length > 200){

            vector.trail.shift();

        }

        vector.x += field[0]/norma;
        vector.y += field[1]/norma;

        // Linha de campo

        sim.noFill();
        sim.stroke(0);

        sim.beginShape();

        for(const p of vector.trail){

            sim.vertex(p[0],p[1]);

        }

        sim.endShape();

        // Bolinha

        sim.noStroke();
        sim.fill(0);

        sim.circle(vector.x,vector.y,10);

    }

}

function drawCargas(){

    for(const q of cargas){

        let size = 0;

        if(q.sinal === "+"){

            sim.fill(255,90,90);

            size = 40;

            sim.circle(q.x,q.y,40);

            sim.fill(0);
            sim.textSize(size);

            sim.text(
                q.sinal,
                q.x-size/3.5,
                q.y+size/3
            );

        }

        if(q.sinal === "-"){

            sim.fill(90,90,255);

            size = 80;

            sim.circle(q.x,q.y,40);

            sim.fill(0);
            sim.textSize(size);

            sim.text(
                q.sinal,
                q.x-size/6,
                q.y+size/4
            );

        }

    }

}

function campo(x,y){

    let Ex = 0;
    let Ey = 0;

    for(const c of cargas){

        const dx = x-c.x;
        const dy = y-c.y;

        const dS = dx*dx+dy*dy;

        if(dS < 1) continue;

        const S = Math.sqrt(dS);

        const sinal = (c.sinal === "+") ? 1 : -1;

        const intensidade = sinal*c.carga;

        Ex += intensidade*dx/(S*S*S);
        Ey += intensidade*dy/(S*S*S);

    }

    return [Ex,Ey];

}

}

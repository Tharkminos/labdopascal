function pn_field(sim){

let trail;

let cargas = [
    {
        sinal:"+",
        x:150,
        y:149,
        carga:10
    },
    {
        sinal:"-",
        x:500-150,
        y:151,
        carga:10
    }
];

let vetores = [];
let caminho = [];
let time = 0;

sim.simulacaoConcluida = function(){

    return true;

}

sim.setup = function(){

    sim.canvas = sim.createCanvas(500,300);
    sim.canvas.parent("canvas-pn_field");

    field();
    add(6);

    trail = sim.createGraphics(sim.width,sim.height);

    drawPath();

}

sim.draw = function(){

    time++;

    sim.background(220);

    drawVectors();

    sim.image(trail,0,0);

    drawCargas();

    if(time > 50){

        add(6);
        time = 0;

    }

    let temp = [...vetores];

    const any_anion = ifAny("-");

    for(const carga of cargas){

        for(let v = temp.length-1; v >= 0; v--){

            const dx = carga.x - temp[v].x;
            const dy = carga.y - temp[v].y;

            const S = Math.hypot(dx,dy);

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

function field(){

    caminho = [];

    for(const q of cargas){

        for(let i = 0; i < 6; i++){

            let linha = [];

            let x = q.x + 10*Math.sin(i*2*Math.PI/6);
            let y = q.y + 10*Math.cos(i*2*Math.PI/6);

            for(let a = 0; a < 10000/6; a++){

                linha.push({
                    x:x,
                    y:y
                });

                for(let xz = 0; xz < 30; xz++){

                    let cp = campo(x,y);

                    let norma = Math.hypot(cp[0],cp[1]);

                    if(norma === 0){

                        break;

                    }

                    if(ifAny("+")){

                        x += cp[0]/norma;
                        y += cp[1]/norma;

                    }else{

                        x -= cp[0]/norma;
                        y -= cp[1]/norma;

                    }

                }

            }

            caminho.push(linha);

        }

    }

}

function add(n){

    const any_cation = ifAny("+");

    for(const q of cargas){

        for(let i = 0; i <= n; i++){

            if(q.sinal === "+"){

                vetores.push({

                    x:q.x + 15*Math.sin(i*2*Math.PI/n),
                    y:q.y + 15*Math.cos(i*2*Math.PI/n)

                });

            }

        }
        if(!any_cation){

            if(q === cargas[0]){

                let liner = [];

                for(let px = 0; px < caminho.length; px++){

                    for(const ponto of caminho[px]){

                        if(Math.hypot(q.x-ponto.x,q.y-ponto.y) > 175){

                            liner.push(ponto);
                            break;

                        }

                    }

                    if(liner.length >= n){

                        break;

                    }

                }

                for(const p of liner){

                    vetores.push({
                        x:p.x,
                        y:p.y
                    });

                }

            }

            if(cargas.length > 1){

                if(q === cargas[1]){

                    let liner = [];

                    for(let px = caminho.length-1; px >= 0; px--){

                        for(const ponto of caminho[px]){

                            if(Math.hypot(q.x-ponto.x,q.y-ponto.y) > 175){

                                liner.push(ponto);
                                break;

                            }

                        }

                        if(liner.length >= n){

                            break;

                        }

                    }

                    for(const p of liner){

                        vetores.push({
                            x:p.x,
                            y:p.y
                        });

                    }

                }

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

    sim.noStroke();
    sim.fill(0);

    for(const vector of vetores){

        let field = campo(vector.x,vector.y);

        let norma = Math.hypot(field[0],field[1]);

        if(norma === 0){

            continue;

        }

        vector.x += field[0]/norma;
        vector.y += field[1]/norma;
         // direção unitária
        ux = field[0]/norma
        uy = field[1]/norma
        px = -uy
        py = ux
        ponta = 8
        base  = 5
        sim.triangle(
          vector.x + ponta*ux,
          vector.y + ponta*uy,
          vector.x - ponta*ux + base*px,
          vector.y - ponta*uy + base*py,
          vector.x - ponta*ux - base*px,
          vector.y - ponta*uy - base*py)

    }

}

function drawCargas(){

    for(const q of cargas){

        let size = 0;

        if(q.sinal === "+"){

            sim.fill(255,90,90);

            size = 40;

            sim.circle(q.x,q.y,40);

            sim.textSize(size);

            sim.fill(0);

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

        if(dS < 1){

            continue;

        }

        const S = Math.sqrt(dS);

        const sinal = (c.sinal === "+") ? 1 : -1;

        const intensidade = sinal*c.carga;

        Ex += intensidade*dx/(S*S*S);
        Ey += intensidade*dy/(S*S*S);

    }

    return [Ex,Ey];

}

function drawPath(){

    trail.clear();

    trail.stroke(0);

    trail.strokeWeight(0.5);

    trail.noFill();

    for(const linha of caminho){

        trail.beginShape();

        for(const p of linha){

            trail.vertex(p.x,p.y);

        }

        trail.endShape();

    }

}

}

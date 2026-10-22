# Atividade - - - - -

**1)** Qual a diferença quando movemos uma porta com uma distância de 0,10m a uma força de 10N e a uma distância de 2m com a mesma força? O que acontece com o Momento da força atuando?

-
-
-
**2)** Temos o mesmo resultado quando mantemos a distância de 0,10m fixo, e mudamos o valor da força de 10N para 80? Justifique:

-
-
-

**3)** Como a mudança no ângulo muda o torque(momento da força)?

-
-
-

**4)** Ao aplicarmos uma mesma força em diferentes parte da porta, em qual distância conseguiremos abrir a força mais facilmente? Justifique

-
-
-

**5)** Explique agora, o que você entendeu como Momento de uma força(torque)?

-
-
-

$$$ p5js

let intensidade, distancia, direcao;
let portaAng = 0, velocidade = 0, ativo = false;


const larguraPorta = 2;
const massaPorta = 35;
const escala = 165;
const origem = {x: 225, y: 270};

let botao, reiniciar;

function setup() {
  createCanvas(760, 560);
  textFont('Arial');

  intensidade = createSlider(0, 180, 65, 1);
  distancia = createSlider(0.1, 2, 1.8, 0.05);
  direcao = createSlider(-90, 90, 0, 1);

  for (let s of [intensidade, distancia, direcao]) {
    s.style('width', '175px');
  }

  botao = createButton('Aplicar força / Pausar');
  botao.mousePressed(() => ativo = !ativo);

  reiniciar = createButton('Fechar porta');
  reiniciar.mousePressed(() => {
    ativo = false;
    portaAng = 0;
    velocidade = 0;
  });
}

function draw() {
  background(239, 242, 245);

  const F = intensidade.value();
  const r = distancia.value();
  const desvio = radians(direcao.value());

  const moduloTorque = r * F * cos(desvio);

  // Momento de inércia de uma porta uniforme
  const I = massaPorta * larguraPorta * larguraPorta / 3;

  const dt = min(deltaTime / 1000, 0.033) / 5;

  // Simulação dinâmica
  if (ativo) {
    for (let i = 0; i < 5; i++) {
      const tau = moduloTorque
        - 20 * velocidade
        - (abs(velocidade) > 0.0001
          ? 2 * Math.sign(velocidade)
          : 0);

      velocidade += tau / I * dt;
      portaAng += velocidade * dt;

      // Limites físicos da porta
      if (portaAng >= HALF_PI) {
        portaAng = HALF_PI;
        velocidade = 0;
      }

      if (portaAng <= 0) {
        portaAng = 0;
        velocidade = 0;
      }
    }
  }

  // Cabeçalho
  noStroke();
  fill(23, 42, 61);
  rect(0, 0, width, 67);

  fill(255);
  textSize(23);
  textStyle(BOLD);
  text('ABRINDO UMA PORTA PESADA', 20, 30);

  textStyle(NORMAL);
  textSize(13);
  fill(192, 211, 230);
  text(
    'Experimento: força, braço de alavanca e movimento de rotação',
    20, 51
  );

  // Parede e dobradiça
  stroke(110, 120, 130);
  strokeWeight(12);
  line(70, 270, 225, 270);

  noStroke();
  fill(220, 225, 230);
  rect(20, 350, 710, 3);

  // Porta vista de cima
  push();
  translate(origem.x, origem.y);
  rotate(-portaAng);

  stroke(108, 63, 31);
  strokeWeight(2);
  fill(174, 112, 60);
  rect(0, -13, larguraPorta * escala, 26, 4);

  // Textura da madeira
  stroke(218, 159, 99);
  strokeWeight(1);

  for (let k = 12; k < larguraPorta * escala; k += 25) {
    line(k, -9, k + 15, -9);
  }

  // Maçaneta
  noStroke();
  fill(220, 225, 235);
  circle(1.8 * escala, 0, 14);

  // Ponto de aplicação da força
  let p = r * escala;
  fill(245, 153, 34);
  circle(p, 0, 15);

  // Vetor força
  if (F > 0) {
    const a = -HALF_PI + desvio;
    const tam = map(F, 0, 180, 0, 105);

    desenharSeta(
      p, 0,
      p + tam * cos(a),
      tam * sin(a),
      color(218, 55, 56)
    );
  }

  pop();

  // Eixo de rotação
  noStroke();
  fill(75, 85, 98);
  circle(origem.x, origem.y, 25);

  fill(195, 202, 213);
  circle(origem.x, origem.y, 12);

  fill(55, 70, 85);
  textSize(13);
  text('Dobradiças', 145, 305);

  fill(30, 45, 60);
  textSize(15);
  text('Visão superior', 22, 96);

  // Painel inferior
  fill(255);
  stroke(210, 217, 224);
  strokeWeight(1);
  rect(15, 373, 730, 171, 10);

  noStroke();
  fill(28, 45, 64);
  textSize(15);
  textStyle(BOLD);
  text('Controles do experimento', 28, 397);
  textStyle(NORMAL);

  rotulo('Força', F + ' N', 28, 422);
  rotulo('Distância', r.toFixed(2) + ' m', 28, 459);
  rotulo('Desvio da perpendicular', direcao.value() + '°', 375, 422);

  // Posição dos sliders
  posicionar(intensidade, 125, 405);
  posicionar(distancia, 150, 442);
  posicionar(direcao, 548, 405);

  botao.position(28, 503);
  reiniciar.position(205, 503);

  // Resultados
  fill(22, 48, 72);
  textSize(17);
  textStyle(BOLD);

  text(
    'Torque: ' + moduloTorque.toFixed(1) + ' N·m',
    475, 493
  );

  text(
    'Abertura: ' + degrees(portaAng).toFixed(1) + '°',
    475, 520
  );

  textStyle(NORMAL);
  fill(50, 65, 78);
  textSize(12);

  text(
    'Modelo: porta uniforme de 35 kg e 2 m; força tangencial positiva abre a porta.',
    25, 360
  );

  if (portaAng >= HALF_PI - 0.0001) {
    fill(24, 129, 85);
    textSize(14);
    text('Porta totalmente aberta (90°)', 430, 105);
  }
}

function rotulo(t, v, x, y) {
  fill(45, 59, 75);
  textSize(12);
  text(t + ': ' + v, x, y);
}

function posicionar(el, x, y) {
  el.position(x, y);
}

function desenharSeta(x1, y1, x2, y2, cor) {
  stroke(cor);
  strokeWeight(4);
  line(x1, y1, x2, y2);

  push();
  translate(x2, y2);
  rotate(atan2(y2 - y1, x2 - x1));

  noStroke();
  fill(cor);
  triangle(0, 0, -13, -6, -13, 6);
  pop();
}

$$$

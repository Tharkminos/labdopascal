

// -----------------------------
// DADOS DO EXPERIMENTO
// -----------------------------
function mecExp(sim){
let massa = 2;              // kg
let gravidade = 10;         // m/s²
let alturaInicial = 20;     // m

let tempo = 0;
let velocidade = 0;
let altura = alturaInicial;

let rodando = false;
let terminou = false;

// -----------------------------
// TORRE
// -----------------------------

let xTorre = 170;
let larguraTorre = 180;

let topoTorre = 70;
let escala = 25;

// Alturas das janelas
let alturasJanelas = [20, 16, 12, 8, 4, 0];
let nomesJanelas = ["A", "B", "C", "D", "E", "F"];

// Última janela atingida
let janelaAtual = -1;


// ============================================
// SETUP
// ============================================

sim.setup = function() {

  createCanvas(750, 700);

  textFont("Arial");
}


// ============================================
// DRAW
// ============================================

sim.draw = function() {

  background(235);

  desenharTitulo();

  desenharTorre();

  atualizarFisica();

  desenharEsfera();

  desenharInformacoes();

  desenharBotoes();

  verificarJanela();
}


// ============================================
// TÍTULO
// ============================================

function desenharTitulo() {

  fill(40);
  noStroke();

  textAlign(CENTER);
  textSize(28);

  text(
    "Atividade Experimental Energia Mecânica",
    width / 2,
    35
  );
}


// ============================================
// TORRE
// ============================================

function desenharTorre() {

  // Corpo da torre
  fill(205);
  stroke(70);
  strokeWeight(2);

  rect(
    xTorre,
    topoTorre,
    larguraTorre,
    alturaInicial * escala+6
  );


  // Janelas
  for (let i = 0; i < alturasJanelas.length; i++) {

    let h = alturasJanelas[i];

    let y =
      topoTorre +
      (alturaInicial - h) * escala;


    // Janela
    fill(70);
    noStroke();

    rect(
      xTorre + larguraTorre / 2 - 18,
      y - 15,
      36,
      30
    );


    // Nome da janela
    fill(30);

    textAlign(LEFT, CENTER);
    textSize(16);

    text(
      nomesJanelas[i],
      xTorre + larguraTorre + 15,
      y
    );


    // Altura
    textAlign(RIGHT, CENTER);
    textSize(14);

    text(
      h + " m",
      xTorre - 15,
      y - 4
    );
  }


  // Chão
  stroke(60);
  strokeWeight(4);

  line(
    80,
    topoTorre + alturaInicial * escala + 5,
    650,
    topoTorre + alturaInicial * escala + 5
  );
}


// ============================================
// ESFERA
// ============================================

function desenharEsfera() {

  let x = xTorre + larguraTorre / 2;

  let y =
    topoTorre +
    (alturaInicial - altura) * escala;


  noStroke();

  fill(190, 50, 50);

  circle(
    x,
    y,
    24
  );
}


// ============================================
// FÍSICA
// ============================================

function atualizarFisica() {

  if (!rodando || terminou) {
    return;
  }


  // Intervalo de tempo
  let dt = 1 / 60;

  tempo += dt;


  // Velocidade da queda livre
  velocidade = gravidade * tempo;


  // Altura em função do tempo
  altura =
    alturaInicial -
    (gravidade * tempo * tempo) / 2;


  // Quando chega ao chão
  if (altura <= 0) {

    altura = 0;

    velocidade =
      sqrt(2 * gravidade * alturaInicial);

    rodando = false;

    terminou = true;
  }
}


// ============================================
// VERIFICAR JANELAS
// ============================================

function verificarJanela() {

  for (let i = 0; i < alturasJanelas.length; i++) {

    let h = alturasJanelas[i];

    // A esfera passou pela altura desta janela
    if (
      altura <= h + 0.05 &&
      altura >= h - 0.05
    ) {

      if (janelaAtual !== i) {

        janelaAtual = i;

      }
    }
  }
}


// ============================================
// INFORMAÇÕES
// ============================================

function desenharInformacoes() {

  let x = 430;
  let y = 110;

  fill(35);
  noStroke();

  textAlign(LEFT);

  textSize(22);

  text(
    "Dados do experimento",
    x,
    y
  );


  textSize(17);

  text(
    "Massa: " + massa.toFixed(1) + " kg",
    x,
    y + 50
  );

  text(
    "Altura: " + altura.toFixed(2) + " m",
    x,
    y + 85
  );

  text(
    "Velocidade: " + velocidade.toFixed(2) + " m/s",
    x,
    y + 120
  );

  text(
    "Tempo: " + tempo.toFixed(2) + " s",
    x,
    y + 155
  );


  text(
    "Gravidade: " + gravidade + " m/s²",
    x,
    y + 190
  );


  // Janela atual
  if (janelaAtual >= 0) {

    textSize(20);

    text(
      "Janela: " + nomesJanelas[janelaAtual],
      x,
      y + 250
    );

  } else {

    textSize(17);

    text(
      "Aguardando início...",
      x,
      y + 250
    );
  }


  // Mensagem final
  if (terminou) {

    textSize(18);

    text(
      "Objeto chegou ao chão.",
      x,
      y + 300
    );
  }
}


// ============================================
// BOTÕES
// ============================================

function desenharBotoes() {

  let y = 630;

  desenharBotao(
    150,
    y,
    120,
    40,
    "INICIAR"
  );

  desenharBotao(
    290,
    y,
    120,
    40,
    "PAUSAR"
  );

  desenharBotao(
    430,
    y,
    120,
    40,
    "REINICIAR"
  );
}


function desenharBotao(
  x,
  y,
  largura,
  altura,
  textoBotao
) {

  fill(215);
  stroke(80);
  strokeWeight(1);

  rect(
    x,
    y,
    largura,
    altura,
    6
  );


  fill(30);
  noStroke();

  textAlign(CENTER, CENTER);
  textSize(14);

  text(
    textoBotao,
    x + largura / 2,
    y + altura / 2
  );
}


// ============================================
// CLIQUES
// ============================================

function mousePressed() {

  // INICIAR
  if (
    mouseX >= 150 &&
    mouseX <= 270 &&
    mouseY >= 630 &&
    mouseY <= 670
  ) {

    if (!terminou) {

      rodando = true;
    }
  }


  // PAUSAR
  if (
    mouseX >= 290 &&
    mouseX <= 410 &&
    mouseY >= 630 &&
    mouseY <= 670
  ) {

    rodando = false;
  }


  // REINICIAR
  if (
    mouseX >= 430 &&
    mouseX <= 550 &&
    mouseY >= 630 &&
    mouseY <= 670
  ) {

    tempo = 0;

    velocidade = 0;

    altura = alturaInicial;

    rodando = false;

    terminou = false;

    janelaAtual = -1;
  }
}
}

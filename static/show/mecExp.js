// ============================================
// ATIVIDADE EXPERIMENTAL
// ENERGIA MECÂNICA
// ============================================

function mecExp(sim) {

  // -----------------------------
  // DADOS DO EXPERIMENTO
  // -----------------------------

  let massa = 2;              // kg
  let gravidade = 10;         // m/s²
  let alturaInicial = 20;     // m

  let tempo = 0;
  let velocidade = 0;
  let altura = alturaInicial;

  let rodando = false;
  let terminou = false;

  // Guarda a altura anterior
  let alturaAnterior = alturaInicial;


  // -----------------------------
  // TORRE
  // -----------------------------

  let xTorre = 170;
  let larguraTorre = 180;

  let topoTorre = 70;
  let escala = 25;


  // Alturas das janelas
  let alturasJanelas = [20, 16, 12, 8, 4, 0];

  let nomesJanelas = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
  ];


  // Última janela atingida
  let janelaAtual = -1;


  // ============================================
  // SETUP
  // ============================================

  sim.setup = function () {

    sim.createCanvas(750, 700);

    sim.textFont("Arial");
  };


  // ============================================
  // DRAW
  // ============================================

  sim.draw = function () {

    sim.background(235);

    atualizarFisica();

    verificarJanela();

    desenharTitulo();

    desenharTorre();

    desenharEsfera();

    desenharInformacoes();

    desenharBotoes();
  };


  // ============================================
  // TÍTULO
  // ============================================

  function desenharTitulo() {

    sim.fill(40);
    sim.noStroke();

    sim.textAlign(sim.CENTER);
    sim.textSize(28);

    sim.text(
      "Atividade Experimental - Energia Mecânica",
      sim.width / 2,
      35
    );
  }


  // ============================================
  // TORRE
  // ============================================

  // ============================================
// TORRE
// ============================================

function desenharTorre() {

  // Margem para que as janelas não fiquem
  // cortadas no topo ou na base
  let margem = 18;

  let topo = topoTorre + margem;

  let alturaCorpo =
    alturaInicial * escala;

  let base =
    topo + alturaCorpo;


  // -----------------------------
  // Corpo da torre
  // -----------------------------

  sim.fill(205);
  sim.stroke(70);
  sim.strokeWeight(2);

  sim.rect(
    xTorre,
    topo-30,
    larguraTorre,
    alturaCorpo+60
  );


  // -----------------------------
  // Janelas
  // -----------------------------

  for (
    let i = 0;
    i < alturasJanelas.length;
    i++
  ) {

    let h = alturasJanelas[i];


    // Posição vertical da janela
    let y =
      topo +
      (alturaInicial - h) * escala;


    // -----------------------------
    // Janela
    // -----------------------------

    sim.fill(70);
    sim.noStroke();

    sim.rect(
      xTorre + larguraTorre / 2 - 18,
      y - 15,
      36,
      30
    );


    // -----------------------------
    // Nome da janela
    // -----------------------------

    sim.fill(30);

    sim.textAlign(
      sim.LEFT,
      sim.CENTER
    );

    sim.textSize(16);

    sim.text(
      nomesJanelas[i],
      xTorre + larguraTorre + 15,
      y
    );


    // -----------------------------
    // Altura
    // -----------------------------

    sim.textAlign(
      sim.RIGHT,
      sim.CENTER
    );

    sim.textSize(14);

    sim.text(
      h + " m",
      xTorre - 15,
      y
    );
  }


  // -----------------------------
  // Chão
  // -----------------------------

  sim.stroke(60);
  sim.strokeWeight(4);

  sim.line(
    80,
    base+20,
    650,
    base+20
  );
}


  // ============================================
  // ESFERA
  // ============================================

  function desenharEsfera() {

    let x =
      xTorre +
      larguraTorre / 2;


    let y =
      topoTorre +
      (alturaInicial - altura) * escala;


    sim.noStroke();

    sim.fill(190, 50, 50);

    sim.circle(
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


    // Guarda a altura anterior
    alturaAnterior = altura;


    // Intervalo de tempo
    let dt = 1 / 60;

    tempo += dt;


    // Velocidade da queda livre
    velocidade =
      gravidade * tempo;


    // Altura em função do tempo
    altura =
      alturaInicial -
      (gravidade * tempo * tempo) / 2;


    // Quando chega ao chão
    if (altura <= 0) {

      altura = 0;


      velocidade =
        sim.sqrt(
          2 *
          gravidade *
          alturaInicial
        );


      rodando = false;

      terminou = true;
    }
  }


  // ============================================
  // VERIFICAR JANELAS
  // ============================================

  function verificarJanela() {

    for (
      let i = 0;
      i < alturasJanelas.length;
      i++
    ) {

      let h = alturasJanelas[i];


      // A esfera passou pela altura da janela
      if (
        alturaAnterior > h &&
        altura <= h
      ) {

        janelaAtual = i;
      }
    }
  }


  // ============================================
  // INFORMAÇÕES
  // ============================================

  function desenharInformacoes() {

    let x = 430;
    let y = 110;


    sim.fill(35);
    sim.noStroke();

    sim.textAlign(sim.LEFT);


    sim.textSize(22);

    sim.text(
      "Dados do experimento",
      x,
      y
    );


    sim.textSize(17);

    sim.text(
      "Massa: " +
      massa.toFixed(1) +
      " kg",
      x,
      y + 50
    );


    sim.text(
      "Altura: " +
      altura.toFixed(2) +
      " m",
      x,
      y + 85
    );


    sim.text(
      "Velocidade: " +
      velocidade.toFixed(2) +
      " m/s",
      x,
      y + 120
    );


    sim.text(
      "Tempo: " +
      tempo.toFixed(2) +
      " s",
      x,
      y + 155
    );


    sim.text(
      "Gravidade: " +
      gravidade +
      " m/s²",
      x,
      y + 190
    );


    // -----------------------------
    // JANELA ATUAL
    // -----------------------------

    if (janelaAtual >= 0) {

      sim.textSize(20);

      sim.text(
        "Janela: " +
        nomesJanelas[janelaAtual],
        x,
        y + 250
      );

    } else {

      sim.textSize(17);

      sim.text(
        "Aguardando início...",
        x,
        y + 250
      );
    }


    // -----------------------------
    // MENSAGEM FINAL
    // -----------------------------

    if (terminou) {

      sim.textSize(18);

      sim.text(
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

    sim.fill(215);
    sim.stroke(80);
    sim.strokeWeight(1);

    sim.rect(
      x,
      y,
      largura,
      altura,
      6
    );


    sim.fill(30);
    sim.noStroke();

    sim.textAlign(
      sim.CENTER,
      sim.CENTER
    );

    sim.textSize(14);

    sim.text(
      textoBotao,
      x + largura / 2,
      y + altura / 2
    );
  }


  // ============================================
  // CLIQUES
  // ============================================

  sim.mousePressed = function () {

    // -----------------------------
    // INICIAR
    // -----------------------------

    if (
      sim.mouseX >= 150 &&
      sim.mouseX <= 270 &&
      sim.mouseY >= 630 &&
      sim.mouseY <= 670
    ) {

      if (!terminou) {

        rodando = true;
      }
    }


    // -----------------------------
    // PAUSAR
    // -----------------------------

    if (
      sim.mouseX >= 290 &&
      sim.mouseX <= 410 &&
      sim.mouseY >= 630 &&
      sim.mouseY <= 670
    ) {

      rodando = false;
    }


    // -----------------------------
    // REINICIAR
    // -----------------------------

    if (
      sim.mouseX >= 430 &&
      sim.mouseX <= 550 &&
      sim.mouseY >= 630 &&
      sim.mouseY <= 670
    ) {

      tempo = 0;

      velocidade = 0;

      altura = alturaInicial;

      alturaAnterior = alturaInicial;

      rodando = false;

      terminou = false;

      janelaAtual = -1;
    }
  };
}

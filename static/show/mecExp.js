// ============================================
// ATIVIDADE EXPERIMENTAL
// ENERGIA MECÂNICA
// ============================================

function mecExp(sim) {

  // ============================================
  // DADOS DO EXPERIMENTO
  // ============================================

  let massa = 2;              // kg
  let gravidade = 10;         // m/s²
  let alturaInicial = 20;     // m

  let tempo = 0;
  let velocidade = 0;
  let altura = alturaInicial;

  let rodando = false;
  let terminou = false;

  // Altura anterior para detectar
  // quando a esfera passa pelas janelas
  let alturaAnterior = alturaInicial;


  // ============================================
  // CONFIGURAÇÃO DA TORRE
  // ============================================

  let xTorre = 170;
  let larguraTorre = 180;

  // Posição REAL do topo da torre
  let topoTorre = 85;

  // Quantidade de pixels por metro
  let escala = 25;


  // ============================================
  // JANELAS
  // ============================================

  let alturasJanelas = [
    20,
    16,
    12,
    8,
    4,
    0
  ];

  let nomesJanelas = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
  ];


  // Janela atualmente atingida
  // Começa em A porque a esfera começa em 20 m
  let janelaAtual = 0;


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

    // Atualiza a física
    atualizarFisica();

    // Verifica as janelas
    verificarJanela();

    // Desenha a interface
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

    sim.textAlign(
      sim.CENTER,
      sim.CENTER
    );

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

  function desenharTorre() {

    // --------------------------------------------
    // ALTURA TOTAL DA TORRE
    // --------------------------------------------

    let alturaTorre =
      alturaInicial * escala;

    // O final da torre corresponde exatamente
    // à altura 0 m
    let baseTorre =
      topoTorre + alturaTorre;


    // --------------------------------------------
    // CORPO DA TORRE
    // --------------------------------------------

    sim.fill(205);

    sim.stroke(70);
    sim.strokeWeight(2);

    sim.rect(
      xTorre,
      topoTorre-20,
      larguraTorre,
      alturaTorre+40
    );


    // --------------------------------------------
    // JANELAS
    // --------------------------------------------

    for (
      let i = 0;
      i < alturasJanelas.length;
      i++
    ) {

      let h = alturasJanelas[i];


      // ------------------------------------------
      // POSIÇÃO DA JANELA
      // ------------------------------------------

      let y =
        topoTorre +
        (alturaInicial - h) * escala;


      // ------------------------------------------
      // DESTAQUE DA JANELA ATUAL
      // ------------------------------------------

      if (i === janelaAtual) {

        sim.fill(190, 50, 50);

      } else {

        sim.fill(70);

      }


      sim.noStroke();


      // ------------------------------------------
      // DESENHO DA JANELA
      // ------------------------------------------

      sim.rect(
        xTorre + larguraTorre / 2 - 18,
        y - 15,
        36,
        30
      );


      // ------------------------------------------
      // NOME DA JANELA
      // ------------------------------------------

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


      // ------------------------------------------
      // ALTURA
      // ------------------------------------------

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


    // --------------------------------------------
    // CHÃO
    // --------------------------------------------

    sim.stroke(60);
    sim.strokeWeight(4);

    sim.line(
      80,
      baseTorre+10,
      650,
      baseTorre+10
    );

  }


  // ============================================
  // ESFERA
  // ============================================

  function desenharEsfera() {

    // --------------------------------------------
    // POSIÇÃO HORIZONTAL
    // --------------------------------------------

    let x =
      xTorre +
      larguraTorre / 2;


    // --------------------------------------------
    // POSIÇÃO VERTICAL
    // --------------------------------------------
    //
    // IMPORTANTE:
    // A mesma referência "topoTorre"
    // é utilizada pelas janelas.
    //
    // Assim:
    //
    // altura = 20 m -> posição A
    // altura = 16 m -> posição B
    // altura = 12 m -> posição C
    // altura = 8 m  -> posição D
    // altura = 4 m  -> posição E
    // altura = 0 m  -> posição F
    //
    // --------------------------------------------

    let y =
      topoTorre +
      (alturaInicial - altura) * escala;


    // --------------------------------------------
    // ESFERA
    // --------------------------------------------

    sim.noStroke();

    sim.fill(90, 30, 30);

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

    // Se estiver pausado ou terminado,
    // não altera os valores
    if (!rodando || terminou) {

      return;

    }


    // --------------------------------------------
    // INTERVALO DE TEMPO
    // --------------------------------------------

    let dt = 1 / 60;


    // Guarda a altura anterior
    alturaAnterior = altura;


    // Atualiza o tempo
    tempo += dt;


    // --------------------------------------------
    // VELOCIDADE
    // --------------------------------------------
    //
    // Movimento de queda livre:
    //
    // v = g * t
    //
    // --------------------------------------------

    velocidade =
      gravidade * tempo;


    // --------------------------------------------
    // ALTURA
    // --------------------------------------------
    //
    // h = h0 - (g * t²)/2
    //
    // --------------------------------------------

    altura =
      alturaInicial -
      (gravidade * tempo * tempo) / 2;


    // --------------------------------------------
    // CHEGOU AO CHÃO
    // --------------------------------------------

    if (altura <= 0) {

      altura = 0;


      // Velocidade final:
      //
      // v = sqrt(2gh)

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

    // --------------------------------------------
    // SE ESTÁ NO INÍCIO
    // --------------------------------------------

    if (tempo === 0) {

      janelaAtual = 0;

      return;

    }


    // --------------------------------------------
    // VERIFICA CADA JANELA
    // --------------------------------------------

    for (
      let i = 0;
      i < alturasJanelas.length;
      i++
    ) {

      let h =
        alturasJanelas[i];


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

    sim.textAlign(
      sim.LEFT,
      sim.TOP
    );


    // --------------------------------------------
    // TÍTULO
    // --------------------------------------------

    sim.textSize(22);

    sim.text(
      "Dados do experimento",
      x,
      y
    );


    // --------------------------------------------
    // MASSA
    // --------------------------------------------

    sim.textSize(17);

    sim.text(
      "Massa: " +
      massa.toFixed(1) +
      " kg",
      x,
      y + 50
    );


    // --------------------------------------------
    // ALTURA
    // --------------------------------------------

    sim.text(
      "Altura: " +
      altura.toFixed(2) +
      " m",
      x,
      y + 85
    );


    // --------------------------------------------
    // VELOCIDADE
    // --------------------------------------------

    sim.text(
      "Velocidade: " +
      velocidade.toFixed(2) +
      " m/s",
      x,
      y + 120
    );


    // --------------------------------------------
    // TEMPO
    // --------------------------------------------

    sim.text(
      "Tempo: " +
      tempo.toFixed(2) +
      " s",
      x,
      y + 155
    );


    // --------------------------------------------
    // GRAVIDADE
    // --------------------------------------------

    sim.text(
      "Gravidade: " +
      gravidade +
      " m/s²",
      x,
      y + 190
    );


    // --------------------------------------------
    // JANELA ATUAL
    // --------------------------------------------

    sim.textSize(20);

    sim.text(
      "Janela: " +
      nomesJanelas[janelaAtual],
      x,
      y + 250
    );


    // --------------------------------------------
    // MENSAGEM FINAL
    // --------------------------------------------

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


    // --------------------------------------------
    // INICIAR
    // --------------------------------------------

    desenharBotao(
      150,
      y,
      120,
      40,
      "INICIAR"
    );


    // --------------------------------------------
    // PAUSAR
    // --------------------------------------------

    desenharBotao(
      290,
      y,
      120,
      40,
      "PAUSAR"
    );


    // --------------------------------------------
    // REINICIAR
    // --------------------------------------------

    desenharBotao(
      430,
      y,
      120,
      40,
      "REINICIAR"
    );

  }


  // ============================================
  // DESENHAR BOTÃO
  // ============================================

  function desenharBotao(
    x,
    y,
    largura,
    altura,
    textoBotao
  ) {

    // --------------------------------------------
    // FUNDO
    // --------------------------------------------

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


    // --------------------------------------------
    // TEXTO
    // --------------------------------------------

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

    // ==========================================
    // INICIAR
    // ==========================================

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


    // ==========================================
    // PAUSAR
    // ==========================================

    if (
      sim.mouseX >= 290 &&
      sim.mouseX <= 410 &&
      sim.mouseY >= 630 &&
      sim.mouseY <= 670
    ) {

      rodando = false;

    }


    // ==========================================
    // REINICIAR
    // ==========================================

    if (
      sim.mouseX >= 430 &&
      sim.mouseX <= 550 &&
      sim.mouseY >= 630 &&
      sim.mouseY <= 670
    ) {

      // Volta ao estado inicial
      tempo = 0;

      velocidade = 0;

      altura = alturaInicial;

      alturaAnterior = alturaInicial;

      rodando = false;

      terminou = false;

      janelaAtual = 0;

    }

  };

}

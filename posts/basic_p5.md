---
results:true
---

#COMANDOS BÁSICOS

[cor=150,130,0,1]function[/cor] [cor=150,130,0,1]setup(){}[/cor]: Executa o que estiver entre {} apenas uma vez;

[cor=150,130,0,1]function[/cor] [cor=150,130,0,1]draw(){}[/cor]: Executa o que estiver entre {} em looping. O valor padrão que o computador tenta manter é de 60 vezes por segundo;

[cor=180,80,80,1]background[/cor]([cor=240,0,0,1]R[/cor],[cor=0,240,0,1]G[/cor],[cor=0,0,240,1]B[/cor]): Pinta o fundo com o sistema RGB.

[cor=180,80,80,1]fill[/cor]([cor=240,0,0,1]R[/cor],[cor=0,240,0,1]G[/cor],[cor=0,0,240,1]B[/cor])Pinta a figura abaixo utilizando a cor no sistema RGB.

[cor=180,80,80,1]circle(x,y,diametro)[/cor]:Desenha um círculo na posição horizontal x, e na posição vertical y, com o tamanho do **diâmetro** definido.

**→[cor=10,10,200,1]Exemplo da configuração do círculo, clique com o mouse para alterar a posição e utilize as setas para cima e para baixo para alterar o tamanho[/cor] ←**
←[simulacao=basic_circle]←

←[cor=180,80,80,1]rect(x,y,tamanho_x,tamanho_y)[/cor]:Desenha um retângulo na posição horizontal x, e na posição vertical y, com o tamanho definido.→

**→[cor=10,10,200,1]Exemplo da configuração do retângulo, clique com o mouse para alterar a posição e utilize as setas para cima, para baixo, para esquerda e para direita para alterar o tamanho[/cor]←**
←[simulacao=basic_rect]←

**←[cor=180,80,80,1]triangle(x1,y1,x2,y2,x3,y3)[/cor]: Desenha um triângulo escolhendo os três cantos:→**
x1,y1 é o primeiro canto
x2,y2 é o segundo canto
x3,y3 é o terceiro canto

**→[cor=10,10,200,1]Exemplo da configuração do triângulo, clique com o mouse para alterar as posições.[/cor]←**
←[simulacao=basic_triang]←

**→Abaixo, uma ferramenta para escolher a cor do elemento.←** 
[color_picker]

[etapa=Variáveis]
Variáveis, são espaços nomeados no computador, onde salvamos as informações, para podermos consultar depois. Eles são salvos de forma **temporária** enquanto o código estiver em funcionamento. Para criar uma variável que funcione tanto em **setup()** como em **draw()**, criamos ela uma primeira vez fora de [cor=220,50,50,1]function setup(){} e function draw()[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]nome_variavel[/cor] = [cor=200,150,100,1]valor_salvo[/cor] 

**Exemplo:**
[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]tempo[/cor] = [cor=200,150,100,1]0[/cor]  [cor=150,150,150,1]//Cria uma variável chamada tempo com o valor de 0 salvo.[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]nome[/cor] = [cor=100,200,100,1]"Alberto"[/cor]  [cor=150,150,150,1]// Cria uma variável chamada nome, com o valor de "Alberto" salvo[/cor]

No código, ao nos referirmos ao tempo por exemplo, em vez de mostrar a palavra tempo, ele mostrará seu valor:

**Exemplo:**

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]tempo[/cor] = [cor=200,150,100,1]50[/cor]

[cor=20,20,200,1]function[/cor] setup(){

  [cor=200,20,20,1]createCanvas(400,400);[/cor]
  
}

[cor=20,20,200,1]function[/cor] draw(){

[cor=200,20,20,1] background(220); [/cor]

  [cor=200,20,20,1]textSize(32);[/cor]
  
  [cor=200,20,20,1]text(tempo,180,200);[/cor]
  
}

$$$ p5js

let tempo  = 50

function setup(){

createCanvas(400,400);
}

function draw(){

background(220);

textSize(32);

text(tempo,180,200);

}

$$$






[etapa=Alterando valores de variáveis:]
Para alterar o valor de uma variável, podemos redefinir a variável com:

[cor=200,80,80,1] tempo [/cor] = [cor=80,200,80,1] 20 [/cor]

Ou ainda, utilizando operações matemáticas:

# Operações Matemáticas

Nas operações matemáticas, utilizamos operadores como:

[cor=200,100,100,1] tempo [/cor] [cor=100,200,100,1]-= [/cor] [cor=100,100,200,1] 1 [/cor]

[cor=100,200,100,1]-= [/cor] → Significa que  a variável da esquerda vai diminuir com o valor da direita. No caso acima, o tempo vai diminuir de 1 em 1, toda vez que a linha for chamada. 

[cor=200,100,100,1] tempo [/cor] [cor=100,200,100,1]*= [/cor] [cor=100,100,200,1] 2 [/cor]

[cor=100,200,100,1]*= [/cor] → Significa que a variável da esquerda vai multiplicar pelo valor da direita. No caso acima, o tempo vai multiplicar por 2, toda vez que a linha for chamada. 

[cor=200,100,100,1] tempo [/cor] [cor=100,200,100,1]/= [/cor] [cor=100,100,200,1] 2 [/cor]

[cor=100,200,100,1]/= [/cor] → Significa que a variável da esquerda vai dividir pelo valor da direita. No caso acima, o tempo vai dividir por 2, toda vez que a linha for chamada. 

[cor=200,100,100,1] tempo [/cor] [cor=100,200,100,1]+= [/cor] [cor=100,100,200,1] 1 [/cor]

[cor=100,200,100,1]+= [/cor] → O símbolo += aumenta o valor da variável. Se utilizarmos tempo += 1 dentro de draw(), o valor aumentará em 1 a cada repetição. Se ocorrerem 60 repetições por segundo, o valor aumentará 60 unidades por segundo. Observe o exemplo abaixo, em que a variável tempo começa com o valor 0.


[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]tempo[/cor] = [cor=200,150,100,1]0[/cor]

[cor=20,20,200,1]function[/cor] setup(){

  [cor=200,20,20,1]createCanvas(400,400);[/cor]
  
}

[cor=20,20,200,1]function[/cor] draw(){

  [cor=200,20,20,1] background(220); [/cor]

  [cor=200,20,20,1]tempo+=1;[/cor]
  
  [cor=200,20,20,1]textSize(32);[/cor]
  
  [cor=200,20,20,1]text(tempo,180,200);[/cor]
  
}

$$$ p5js

let tempo  = 0

function setup(){

createCanvas(400,400);

}

function draw(){

tempo+=1;

background(220);

textSize(32);

text(tempo,180,200);

}

$$$

[etapa=Trabalhando com Variáveis]

Para trabalhar com variáveis, no P5JS, podemos fazer isso de uma forma prática.
Vamos criar uma nuvem com movimento, e para isso criaremos 3 variáveis:

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]NuvemX[/cor] = [cor=200,150,100,1]0[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]NuvemY[/cor] = [cor=200,150,100,1]200[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]velocidade[/cor] = [cor=200,150,100,1]1[/cor]

[cor=200,100,100,1]NuvemX[/cor], refere-se a posição X(horizontal) da nuvem, [cor=200,100,100,1]NuvemY[/cor] se refere a posição Y(vertical) da nuvem e [cor=200,100,100,1]velocidade[/cor] se refere a velocidade de movimento da nuvem. Para construir a nuvem faremos o seguinte código na função [cor=100,100,200,1]draw()[/cor]:

[cor=200,100,100,1]fill(255); [/cor]      [cor=100,100,100,1]// Pinta de branco[/cor]  

[cor=200,100,100,1]NuvemX += velocidade [/cor] [cor=100,100,100,1]// A velocidade da nuvem é 1, a cada frame aumenta a variável NuvemX em 1 (ela irá para a direita) [/cor]

[cor=200,100,100,1]circle(NuvemX,NuvemY,40);[/cor] [cor=100,100,100,1]// Desenha o primeiro círculo de diâmetro 40[/cor]

[cor=200,100,100,1]circle(NuvemX+25,NuvemY,40);[/cor] [cor=100,100,100,1]// Desenha o segundo círculo afastado em 25 pixels[/cor]

[cor=200,100,100,1]circle(NuvemX+50,NuvemY,40);[/cor] [cor=100,100,100,1]// Desenha o terceiro círculo afastado em 50 pixels do primeiro[/cor]
  
[cor=200,100,100,1]text("Nuvem:" + NuvemX, 0,395);[/cor]  [cor=100,100,100,1]// Adiciona a Palavra Nuvem na tela e mostra o valor salvo em NuvemX[/cor]


$$$ p5js

function setup() {
  
  createCanvas(400, 400);
  
}

let NuvemX = 0;
let NuvemY = 200;
let velocidade = 1;

function draw() {
  
  noStroke();// Apaga o contorno
  background(117,231,255);
  fill(0,200,41);
  rect(-1,320,401);
  fill(160,80,80);
  triangle(200,200,100,320,100+200,320);
  fill(240)
  triangle(200,200,183,220,217,220);
  fill(255,255,0);
  circle(0,0,150);
  
  //Nuvem, cada círculo da nuvem é desenhado 25 pixels a frente do anterior

  NuvemX += velocidade; // A velocidade da nuvem é 1, isto é, a cada frame aumenta a posição NuvemX em 1
  
  fill(255); // Pinta de branco
  
  circle(NuvemX,NuvemY,40);
  circle(NuvemX+25,NuvemY,40);
  circle(NuvemX+50,NuvemY,40);
  
  fill(0)
  textSize(20)
  text("NuvemX = " + NuvemX,0,395)
}

$$$

[etapa=Variáveis aplicadas as cores]

Para trabalhar com variáveis, no P5JS, podemos fazer isso de uma forma prática.
Vamos criar uma nuvem com movimento, e para isso criaremos 3 variáveis:

[cor=50,50,200,1]let[/cor] [cor=220,100,100,1]Red[/cor] = [cor=200,150,100,1]0[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,220,100,1]Green[/cor] = [cor=200,150,100,1]255[/cor]

[cor=50,50,200,1]let[/cor] [cor=100,100,100,1]velocidade[/cor] = [cor=200,150,100,1]1[/cor]

[cor=220,100,100,1]Red[/cor], refere-se a cor vermelha do círculo, [cor=100,220,100,1]Green[/cor] refere-se a cor verde do círculo. [cor=200,100,100,1]velocidade[/cor] se refere a velocidade da mudança da cor nessa situação. no [cor=100,100,200,1]draw()[/cor], colocamos:

[cor=200,100,100,1]fill(Red, Green, 0); [/cor]      [cor=100,100,100,1]// Pinta o círculo[/cor]  

[cor=200,100,100,1]Red += velocidade [/cor] [cor=100,100,100,1]// A velocidade de mudança da cor vermelha é 1. [/cor]

[cor=200,100,100,1]Green -= velocidade [/cor] [cor=100,100,100,1]// A velocidade de mudança da cor verde é **-1**[/cor]


[cor=200,100,100,1]circle(200,200,200);[/cor] [cor=100,100,100,1]// Desenha o círculo de diâmetro 200[/cor]

[cor=200,100,100,1]text("Red:" + Red, 0,395);[/cor]  [cor=100,100,100,1]// Adiciona a Palavra Red na tela e mostra o valor salvo em Red[/cor]

[cor=200,100,100,1]text("Green:" + Green, 0,395);[/cor]  [cor=100,100,100,1]// Adiciona a Palavra Green na tela e mostra o valor salvo em Green[/cor]


$$$ p5js

function setup() {
  
  createCanvas(400, 400);
  frameRate(10)
}

let Red = 0;
let Green = 255;
let velocidade = 1;

function draw() {
  
  noStroke();// Apaga o contorno
  background(180); // Pinta o fundo de cinza
  
  Red += velocidade; // A velocidade da nuvem é 1, isto é, a cada frame aumenta a posição NuvemX em 1
  Green -= velocidade; // A velocidade da nuvem é 1, isto é, a cada frame aumenta a posição NuvemX em 1
  
  fill(Red,Green, 0);
  
  circle(200,200,100);

  fill(0);
  textSize(20);
  text("Red = " + Red,0,370);
  text("Green = " + Green,0,390);
}

$$$





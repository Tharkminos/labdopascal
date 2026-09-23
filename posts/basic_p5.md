---
results:true
---

#COMANDOS BÁSICOS

[cor=150,130,0,1]function[/cor] [cor=150,130,0,1]setup(){}[/cor]: Executa o que estiver entre {} apenas uma vez;

[cor=150,130,0,1]function[/cor] [cor=150,130,0,1]draw(){}[/cor]: Executa o que estiver entre {} sem parar;

[cor=180,80,80,1]background[/cor]([cor=240,0,0,1]R[/cor],[cor=0,240,0,1]G[/cor],[cor=0,0,240,1]B[/cor]): Pinta o fundo com o sistema RGB.

[cor=180,80,80,1]fill[/cor]([cor=240,0,0,1]R[/cor],[cor=0,240,0,1]G[/cor],[cor=0,0,240,1]B[/cor])Pinta a figura abaixa utilizando a cor no sistema RGB.

[cor=180,80,80,1]circle(x,y,diametro)[/cor]:Desenha um círculo na posição horizontal x, e na posição vertical y, com o tamanho do diâmetro definido.

**→[cor=10,10,200,1]Exemplo da configuração do círculo, clique com o mouse para alterar a posição[/cor]←**
←[simulacao=basic_circle]←

←[cor=180,80,80,1]rect(x,y,tamanho_x,tamanho_y)[/cor]:Desenha um retângulo na posição horizontal x, e na posição vertical y, com o tamanho definido.→

**→[cor=10,10,200,1]Exemplo da configuração do retângulo, clique com o mouse para alterar a posição e as setas para alterar o tamanho[/cor]←**
←[simulacao=basic_rect]←

←[cor=180,80,80,1]triangle(x1,y1,x2,y2,x3,y3)[/cor]:Desenha um triângulo escolhendo os três cantos: 
x1,y1 é o primeiro canto
x2,y2 é o segundo canto
x3,y3 é o terceiro canto

**→[cor=10,10,200,1]Exemplo da configuração do retângulo, clique com o mouse para alterar a posição e as setas para alterar o tamanho[/cor]←**
←[simulacao=basic_triang]←

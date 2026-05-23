        function x(pos,sz,angle){
          return pos+sz/1.5*sin(angle)
        }
        function y(pos,sz,angle){
          return pos+sz/1.5*cos(angle)
        }

        function setup() {
          frameRate(30)
          canvas = createCanvas(600, 600);
          canvas.parent("canvas-egito");

        }
        let rp = 0;
        let gp = 0;
        let bp = 0;
        let speed = 1;
        let n1 = 100; //nuvem 1
        let n2 = -200; // nuvem1

        let xn2 = -400;
        let yn2 = 200;
        let szN = 50;
        let angle = 0;
        let hour = 3.14;
        let night = 30
        function draw() {
          angle += 0.02
          hour += 0.009
          if (hour >2*3.14159265358979){
            hour = 0
          }
          mp = sin(hour/2)
          background((120+rp)*mp,(160+gp)*mp,(250+bp)*mp);
          fill(180,180,180,200)
          rect(0,441,600,60)
          fill(180,180,180,150)
          rect(0,441-59,600,60)
          fill(180,180,180,112)
          rect(0,441-119,600,60)
          fill(180,180,180,60)
          rect(0,441-119-60,600,60)
          n2 += 0.25 + 0.5*abs(sin(angle))
          xn2 += 0.125 + random(0,10)/10*abs(sin(angle))

          rp += speed/16
          gp += speed/4
          bp += speed/8
          if (gp > 30){
            speed = -1;
          } if (gp<0){
            speed = 1;
          }
          fill(255,255,255);
          noStroke() 


          //Sol Inicio
          let sunX = 300-400*sin(hour)
          let sunY = 475+400*cos(hour)
          let Sun = 100;
          let X1 = x(sunX,Sun,angle) 
          let Y1 = y(sunY,Sun,angle)
        fill(255,200+gp+rp,10-rp*10)
        quad(x(sunX,Sun,angle),y(sunY,Sun,angle),x(sunX,Sun,angle+PI/2),y(sunY,Sun,angle+PI/2),x(sunX,Sun,angle+PI),y(sunY,Sun,angle+PI),x(sunX,Sun,angle+1.5*PI),y(sunY,Sun,angle+1.5*PI))
        angle += PI/4
        fill(255,200+gp+rp,10+rp*10)
        quad(x(sunX,Sun,angle),y(sunY,Sun,angle),x(sunX,Sun,angle+PI/2),y(sunY,Sun,angle+PI/2),x(sunX,Sun,angle+PI),y(sunY,Sun,angle+PI),x(sunX,Sun,angle+1.5*PI),y(sunY,Sun,angle+1.5*PI))
        fill(255,220+gp+rp,10+rp*10)
          circle(sunX,sunY,100-rp)

          //Sol Fim

          //Nuvem1 inicio
          fill(255);
          circle(100+n2,100+n1,40)
          circle(100+n2+20,100+n1,40)
          circle(100+n2+20,100+n1-10,60)
          circle(100+n2+45,105+n1,30)
          if(n2>700){
            n1 = random(30,300)
            n2 = -200
          }
          //Nuvem2 inicio
          circle(100+xn2,100+yn2,szN)
          circle(100+xn2+20,100+yn2,szN)
          circle(100+xn2+20,100+yn2-10,szN)
          circle(100+xn2+50,100+yn2-10,szN+10)
          circle(100+xn2+45,105+yn2,szN)
          if(xn2>700){
            yn2 = random(30,300)
            szN = random(40,70)
            xn2 = -200
          }
          //Nuvens Fim
          // Chão inicio
          fill(237*0.8,201*0.8,175*0.8);
          rect(0,498,600,100);
          fill(237,201,175);
          rect(0,500,600,100);
          //Chão fim
          // Pirâmide inicio
          fill(255,200,0); 
          triangle(150+rp+0 ,500+rp,  450,500+rp  ,300,300+rp)
          fill(255,120,0);
          triangle(400+rp/10,500+rp,  450,500+rp  ,300,300+rp)
          // Pirâmide fim
          //Cactus Inicio
          fill(75,150,25)
          rect(500+random(0,1),530,6,15)
          rect(320+random(0,1),512,6,20)
          rect(200+random(0,1),512,6,32)
          rect(200+random(0,1),520,6,6)
          rect(206,518,6,6)
          rect(210,514,6,6)  
          //Cactus Fim
          //Camelo Inicio
          fill(255-30, 210-30, 150-30)
          rect(75,550,10,10)
          rect(89,535+(10-mp*10),5,20-(10-mp*10))
          circle(93,535+(10-mp*10),10)
          circle(75,550,20)
          circle(85,550,20)
          //Camelo Fim
          //Tenda inicio
          fill(230);
          triangle(400,550,450,550,425,500)
          fill(210);
          triangle(450,550,475,530,425,500)
          fill(255,180,30,30-night);
          circle(450,550,80)
          fill(255,150,30,30-night);
          circle(450,550,50)
          fill(110+(1-mp)*(50));
          triangle(415,550,440,550,425,525)
          //Tenda fim
          //Noite Inicio
          fill(0,30,60,120*(1-mp))
          rect(0,0,600,600)
          fill(255,255,200)
          circle(300-400*sin(hour+PI),600+475*cos(hour+PI),75-rp)
          fill(255,220,30,30*(1-(1.5*mp)));
          circle(430,550,50+rp*10)
          fill(255,220,30,20*(1-(1.5*mp)));
          circle(430,550,80+rp*10)
          //Noite fim

        }

let pos, vel, acc;
let dt = 0.05;
let angle = 0

function setup() {
  let canvas = createCanvas(500, 500, WEBGL);
  pos = createVector(0, -100, 0);
  vel = createVector(0, 0, 0);
  acc = createVector(0, 0, 0);
  angleMode(RADIANS);
}

function draw() {
  background(200);
  angle = angle + dt
  orbitControl();

  vel.add(p5.Vector.mult(acc, dt));
  pos.add(p5.Vector.mult(vel, dt));

  push();
  rotateX(HALF_PI);
  

  fill(150);
  plane(300, 300);
  pop();

  push();
  translate(pos.x+100*sin(angle), pos.y, pos.z+100*cos(angle));
  fill(255, 0, 0);
  s1 = sphere(20);
  pop();

  if (pos.y > 100) {
    pos.y = 100;
    vel.y *= -0.8;
  }
}


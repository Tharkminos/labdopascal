function setup() {
    let canvas = createCanvas(400, 400);
}

function draw() {
    background(0);

    fill(255);
    ellipse(width/2, frameCount % height, 30);
}

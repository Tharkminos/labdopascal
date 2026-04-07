GlowScript 3.2 VPython

scene.background = color.black

bola = sphere(
    pos = vec(0,2,0),
    radius = 0.5,
    color = color.red
)

v = 0
g = -9.8
dt = 0.02

while True:
    rate(60)

    v = v + g*dt
    bola.pos.y = bola.pos.y + v*dt

    if bola.pos.y < 0.5:
        bola.pos.y = 0.5
        v = -v*0.9

YELLOW = (245, 196, 0)
NAVY = (20, 33, 61)
TOP = (205, 220, 240)      # gradient top colour
BOTTOM = (252, 238, 205)   # gradient bottom colour
EYE = (250, 248, 240)
move = 0

def setup():
    global grad
    size(1080, 1920)
    strokeCap(ROUND)
    grad = createGraphics(width, height)
    grad.beginDraw()
    for y in range(height):
        grad.stroke(lerpColor(color(*TOP), color(*BOTTOM), y / float(height)))
        grad.line(0, y, width, y)
    grad.endDraw()

def draw():
    global move
    image(grad, 0, 0)
    for row in range(4):
        for i in range(3):
            x = (move + i * 600 + row * 200) % 1800 - 300
            y = 330 + row * 450
            t = frameCount * 0.2 + i + row
            if (i + row) % 2 == 0:
                horse(x, y, t, YELLOW)
            else:
                horse(x, y, t, NAVY)
    move += 5

def horse(x, y, t, c):
    far = (int(c[0] * 0.75), int(c[1] * 0.75), int(c[2] * 0.75))
    pushMatrix()
    translate(x, y + sin(t * 2) * 5)
    scale(1.4)
    rotate(sin(t) * 0.03)

    # far-side legs (slightly darker for depth)
    leg(45, 0, t + 2.7, far, True)
    leg(-75, -5, t + 0.5, far, False)

    # tail
    noFill()
    stroke(*c)
    swish = sin(t * 2) * 12
    for k in range(4):
        strokeWeight(7 - k)
        bezier(-118, -42, -150, -50, -175, -30 + swish, -205, -12 + swish + k * 9)

    # body, neck and head
    noStroke()
    fill(*c)
    beginShape()
    pts = [(-120, -40), (-95, -55), (-30, -48), (35, -62), (70, -95),
           (105, -128), (125, -120), (165, -75), (170, -62), (155, -55),
           (125, -80), (100, -85), (85, -55), (80, -15), (60, 10),
           (30, 15), (-30, 18), (-70, 10), (-118, -5)]
    curveVertex(*pts[-1])
    for p in pts:
        curveVertex(*p)
    curveVertex(*pts[0])
    curveVertex(*pts[1])
    endShape(CLOSE)
    ellipse(-85, -15, 75, 70)

    # ear
    triangle(104, -124, 112, -152, 121, -121)

    # mane
    stroke(*c)
    strokeWeight(5)
    for k in range(8):
        mx = lerp(40, 105, k / 7.0)
        my = lerp(-62, -128, k / 7.0)
        line(mx, my, mx - 20, my + 4 + sin(t * 3 + k) * 4)

    # eye and nostril
    noStroke()
    fill(*EYE)
    ellipse(132, -104, 7, 5)
    ellipse(162, -66, 4, 4)

    # near-side legs
    leg(55, 0, t + 2.2, c, True)
    leg(-85, -5, t, c, False)

    popMatrix()

def leg(hx, hy, t, c, front):
    a = sin(t) * 0.55
    bend = max(0, -cos(t)) * 1.2
    if front:
        b = a - bend
    else:
        b = a + bend * 0.7
    kx = hx + sin(a) * 45
    ky = hy + cos(a) * 45
    fx = kx + sin(b) * 42
    fy = ky + cos(b) * 42
    stroke(*c)
    strokeWeight(17)
    line(hx, hy, kx, ky)
    strokeWeight(9)
    line(kx, ky, fx, fy)
    strokeWeight(12)
    line(fx, fy, fx + sin(b) * 7, fy + cos(b) * 7)

def keyPressed():
    if key == 's':
        save("horses.png")

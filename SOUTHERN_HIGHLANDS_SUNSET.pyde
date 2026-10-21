SKY_TOP = (20, 33, 61)        # navy
SKY_BOTTOM = (250, 175, 90)   # warm orange at the horizon
SUN = (245, 196, 0)           # yellow
MOUNTAINS = [(130, 115, 145), (90, 85, 125), (50, 58, 98), (20, 33, 61)]

def setup():
    global sky, ridges
    size(1080, 1920)
    noStroke()

    # sky gradient
    sky = createGraphics(width, height)
    sky.beginDraw()
    for y in range(height):
        amt = min(1, y / 1300.0)
        sky.stroke(lerpColor(color(*SKY_TOP), color(*SKY_BOTTOM), amt))
        sky.line(0, y, width, y)
    sky.endDraw()

    # mountain shapes
    ridges = []
    for layer in range(4):
        base = 1150 + layer * 160
        height_amt = 450 - layer * 70
        pts = []
        for x in range(0, width + 11, 10):
            y = base - noise(x * 0.003, layer * 10) * height_amt
            pts.append((x, y))
        ridges.append(pts)

def draw():
    image(sky, 0, 0)

    # setting sun (loops)
    sun_y = 650 + (frameCount * 0.8) % 900
    for r in range(6):
        fill(SUN[0], SUN[1], SUN[2], 25)
        ellipse(540, sun_y, 280 + r * 70, 280 + r * 70)
    fill(*SUN)
    ellipse(540, sun_y, 260, 260)

    # mountains in front of the sun
    for layer in range(4):
        fill(*MOUNTAINS[layer])
        beginShape()
        vertex(0, height)
        for p in ridges[layer]:
            vertex(*p)
        vertex(width, height)
        endShape(CLOSE)

def keyPressed():
    if key == 's':
        save("sunset.png")

SKY_TOP = (185, 208, 230)
SKY_BOTTOM = (250, 215, 150) #code comment 
HILL_FAR = (150, 170, 110)
HILL_NEAR = (105, 130, 70)
VINE_ROWS = (70, 95, 45)
LEAF_COLOURS = [(110, 145, 60), (140, 165, 70), (205, 150, 50), (175, 80, 45), (125, 40, 55)]
LEAF_COUNT = 25

def setup():
    global bg, leaves
    size(1080, 1920)

    # background: sky, hills and vine rows
    bg = createGraphics(width, height)
    bg.beginDraw()
    for y in range(height):
        amt = min(1, y / 1200.0)
        bg.stroke(lerpColor(color(*SKY_TOP), color(*SKY_BOTTOM), amt))
        bg.line(0, y, width, y)
    bg.noStroke()
    bg.fill(*HILL_FAR)
    bg.beginShape()
    bg.vertex(0, height)
    for x in range(0, width + 11, 10):
        bg.vertex(x, 1050 + sin(x * 0.004) * 50)
    bg.vertex(width, height)
    bg.endShape(CLOSE)
    bg.fill(*HILL_NEAR)
    bg.beginShape()
    bg.vertex(0, height)
    for x in range(0, width + 11, 10):
        bg.vertex(x, 1250 + sin(x * 0.003 + 2) * 60)
    bg.vertex(width, height)
    bg.endShape(CLOSE)
    bg.noFill()
    bg.stroke(*VINE_ROWS)
    for r in range(1, 13):
        y0 = 1250 + r * r * 4.5
        bg.strokeWeight(2 + r * 0.8)
        bg.beginShape()
        for x in range(0, width + 11, 10):
            bg.vertex(x, y0 + sin(x * 0.003 + 2) * 60 * (1 - r / 20.0))
        bg.endShape()
    bg.endDraw()

    leaves = [new_leaf(random(width)) for i in range(LEAF_COUNT)]

def new_leaf(x):
    return {"x": x, "y": random(height), "size": random(0.8, 1.8),
            "rot": random(TWO_PI), "spin": random(-0.05, 0.05),
            "speed": random(1.5, 3.5), "phase": random(TWO_PI),
            "col": LEAF_COLOURS[int(random(len(LEAF_COLOURS)))]}

def draw():
    image(bg, 0, 0)
    wind = noise(frameCount * 0.01) * 5
    for L in leaves:
        L["x"] += L["speed"] + wind
        L["y"] += sin(frameCount * 0.04 + L["phase"]) * 2 + 0.6
        L["rot"] += L["spin"] + wind * 0.01
        if L["x"] > width + 120 or L["y"] > height + 120:
            L["x"] = -120
            L["y"] = random(-100, height * 0.8)
        draw_leaf(L["x"], L["y"], L["size"], L["rot"], L["col"])

def draw_leaf(x, y, s, rot, c):
    dark = (int(c[0] * 0.6), int(c[1] * 0.6), int(c[2] * 0.6))
    lobes = [(-1.3, 32), (-0.65, 42), (0, 50), (0.65, 42), (1.3, 32)]
    pushMatrix()
    translate(x, y)
    rotate(rot)
    scale(s)
    stroke(*dark)
    strokeWeight(3)
    line(0, 0, 0, 30)
    noStroke()
    fill(*c)
    for a, length in lobes:
        pushMatrix()
        rotate(a)
        ellipse(0, -length / 2.0, length * 0.7, length)
        popMatrix()
    stroke(*dark)
    strokeWeight(1.5)
    for a, length in lobes:
        line(0, 0, sin(a) * length * 0.85, -cos(a) * length * 0.85)
    popMatrix()

def keyPressed():
    if key == 's':
        save("vineyard.png")

SKY_TOP = (185, 208, 230) # RGB colour for the top of the sky (pale blue)
SKY_BOTTOM = (250, 215, 150) # RGB colour for the sky near the horizon (warm golden)
HILL_FAR = (150, 170, 110) # colour of the far-away hill (lighter, faded green)
HILL_NEAR = (105, 130, 70) # colour of the closer hill (deeper green)
VINE_ROWS = (70, 95, 45) # colour of the vine row lines (darkest green)
LEAF_COLOURS = [(110, 145, 60), (140, 165, 70), (205, 150, 50), (175, 80, 45), (125, 40, 55)] # list of autumn leaf colours: green, light green, gold, rust, burgundy
LEAF_COUNT = 25 # how many leaves are floating on screen

def setup():
    global bg, leaves
    size(1080, 1920) # canvas size: 1080 x 1920 px (vertical Instagram Story format)

    # background: sky, hills and vine rows
    bg = createGraphics(width, height)
    bg.beginDraw()
    for y in range(height): # loop through every pixel row, top to bottom
        amt = min(1, y / 1200.0)
        bg.stroke(lerpColor(color(*SKY_TOP), color(*SKY_BOTTOM), amt))
        bg.line(0, y, width, y)
    bg.noStroke() # no outlines on the hills
    bg.fill(*HILL_FAR) # fill colour for the far hill
    bg.beginShape() # start drawing the far hill shape
    bg.vertex(0, height) # first corner: bottom-left of the canvas
    for x in range(0, width + 11, 10):
        bg.vertex(x, 1050 + sin(x * 0.004) * 50)
    bg.vertex(width, height)
    bg.endShape(CLOSE) # close and fill the far hill
    bg.fill(*HILL_NEAR)
    bg.beginShape() # start drawing the near hill shape
    bg.vertex(0, height)
    for x in range(0, width + 11, 10):
        bg.vertex(x, 1250 + sin(x * 0.003 + 2) * 60)
    bg.vertex(width, height)
    bg.endShape(CLOSE)
    bg.noFill() # vine rows are lines only, no fill
    bg.stroke(*VINE_ROWS) # line colour for the vine rows
    for r in range(1, 13): # draw 12 vine rows (r = 1 to 12)
        y0 = 1250 + r * r * 4.5
        bg.strokeWeight(2 + r * 0.8) # closer rows are drawn thicker
        bg.beginShape()
        for x in range(0, width + 11, 10):
            bg.vertex(x, y0 + sin(x * 0.003 + 2) * 60 * (1 - r / 20.0))
        bg.endShape()
    bg.endDraw() # finish the background

    leaves = [new_leaf(random(width)) for i in range(LEAF_COUNT)] # make 25 leaves at random 

def new_leaf(x):
    return {"x": x, "y": random(height), "size": random(0.8, 1.8),
            "rot": random(TWO_PI), "spin": random(-0.05, 0.05), # starting rotation (any angle) and how fast it spins (either direction)
            "speed": random(1.5, 3.5), "phase": random(TWO_PI), # sideways drift speed, and a random offset so leaves don't bob in sync
            "col": LEAF_COLOURS[int(random(len(LEAF_COLOURS)))]} # pick a random colour from the leaf colour list

def draw(): # runs over and over (about 60 times a second)
    image(bg, 0, 0)
    wind = noise(frameCount * 0.01) * 5 # smooth, natural-feeling wind strength between 0 and 5 that changes over time
    for L in leaves: # go through every leaf
        L["x"] += L["speed"] + wind # move the leaf right by its own speed plus the wind
        L["y"] += sin(frameCount * 0.04 + L["phase"]) * 2 + 0.6
        L["rot"] += L["spin"] + wind * 0.01 # spin the leaf; stronger wind spins it a little faster
        if L["x"] > width + 120 or L["y"] > height + 120:
            L["x"] = -120
            L["y"] = random(-100, height * 0.8)
        draw_leaf(L["x"], L["y"], L["size"], L["rot"], L["col"]) # draw the leaf with its current settings

def draw_leaf(x, y, s, rot, c):
    dark = (int(c[0] * 0.6), int(c[1] * 0.6), int(c[2] * 0.6)) # a 40% darker version of the colour for the stem and veins
    lobes = [(-1.3, 32), (-0.65, 42), (0, 50), (0.65, 42), (1.3, 32)]
    pushMatrix()
    translate(x, y) # move to the leaf's position
    rotate(rot) 
    scale(s) # resize the leaf
    stroke(*dark) # stem colour
    strokeWeight(3) # stem thickness
    line(0, 0, 0, 30) # draw the stem pointing downward 30px
    noStroke()
    fill(*c)
    for a, length in lobes:
        pushMatrix()
        rotate(a)
        ellipse(0, -length / 2.0, length * 0.7, length) # draw an oval pointing outward from the centre
        popMatrix()
    stroke(*dark)
    strokeWeight(1.5) # thin veins
    for a, length in lobes:
        line(0, 0, sin(a) * length * 0.85, -cos(a) * length * 0.85)
    popMatrix()

def keyPressed(): # runs whenever a key is pressed
    if key == 's':
        save("vineyard.png") # save the current frame as vineyard.png in the sketch folder

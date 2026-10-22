SKY_TOP = (20, 33, 61) # RGB colour for the top of the sky (navy)
SKY_BOTTOM = (250, 175, 90) # RGB colour for the sky at the horizon (warm orange)
SUN = (245, 196, 0) # RGB colour for the sun (yellow)
MOUNTAINS = [(130, 115, 145), (90, 85, 125), (50, 58, 98), (20, 33, 61)] # 4 mountain colours, from the faded far-back layer to the dark navy front layer


def setup():
    global sky, ridges
    size(1080, 1920) # canvas size: 1080 x 1920 px (vertical Instagram Story format)
    noStroke() # no outlines on any shapes (sun and mountains)

    # sky gradient
    sky = createGraphics(width, height)
    sky.beginDraw()
    for y in range(height): # loop through every pixel row, top to bottom
        amt = min(1, y / 1300.0) # how far down the sky we are
        sky.stroke(lerpColor(color(*SKY_TOP), color(*SKY_BOTTOM), amt)) # blend navy into orange
        sky.line(0, y, width, y)
    sky.endDraw() # finish the sky 

    # mountain shapes
    ridges = []
    for layer in range(4): # make 4 mountain layers 
        base = 1150 + layer * 160 # the bottom line of the peaks; each layer sits 160px lower
        height_amt = 450 - layer * 70 # how tall the peaks can be; front layers are shorter
        pts = []
        for x in range(0, width + 11, 10):
            y = base - noise(x * 0.003, layer * 10) * height_amt
            pts.append((x, y))
        ridges.append(pts)

def draw(): # runs over and over (about 60 times a second)
    image(sky, 0, 0) # paint the saved sky 

    # setting sun (loops)
    sun_y = 650 + (frameCount * 0.8) % 900 # sun's height: starts at 650px, sinks 0.8px per frame, then jumps back after 900px
    for r in range(6): # draw 6 glow rings
        fill(SUN[0], SUN[1], SUN[2], 25) # sun colour but very see-through
        ellipse(540, sun_y, 280 + r * 70, 280 + r * 70)
    fill(*SUN) # solid sun colour
    ellipse(540, sun_y, 260, 260) # the sun itself

    # mountains in front of the sun
    for layer in range(4): # go through each mountain layer, back to front
        fill(*MOUNTAINS[layer])
        beginShape()
        vertex(0, height)
        for p in ridges[layer]:
            vertex(*p)
        vertex(width, height)
        endShape(CLOSE) # close and fill the mountain 

def keyPressed(): # runs whenever a key is pressed
    if key == 's':
        save("sunset.png") # save the current frame as sunset.png in the sketch folder

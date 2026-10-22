YELLOW = (245, 196, 0) # RGB values for the yellow horses
NAVY = (20, 33, 61) # RGB values for the navy horses
TOP = (205, 220, 240)      # gradient top colour
BOTTOM = (252, 238, 205)   # gradient bottom colour
EYE = (250, 248, 240) # off-white colour for the eye and nostril
move = 0 # how far the horses have travelled sideways (starts at 0)

def setup():
    global grad # lets setup() create a variable that draw() can also use
    size(1080, 1920) # canvas size: 1080 x 1920 px (vertical Instagram Story format)
    strokeCap(ROUND) # makes the ends of every line rounded instead of square
    grad = createGraphics(width, height)
    grad.beginDraw()
    for y in range(height): # loop through every pixel row, top to bottom
        grad.stroke(lerpColor(color(*TOP), color(*BOTTOM), y / float(height)))
        grad.line(0, y, width, y) # draw a 1px horizontal line across the full width in that colour
    grad.endDraw()

def draw(): # runs over and over (about 60 times a second)
    global move
    image(grad, 0, 0) # paint the saved gradient as the background (wipes the last frame)
    for row in range(4): # 4 rows of horses
        for i in range(3): # 3 horses in each row # animation timer; adding i + row stops all horses galloping in sync
            x = (move + i * 600 + row * 200) % 1800 - 300
            y = 330 + row * 450 
            t = frameCount * 0.2 + i + row
            if (i + row) % 2 == 0:
                horse(x, y, t, YELLOW) # ...draw a yellow horse
            else:
                horse(x, y, t, NAVY) # ...draw a navy horse
    move += 5

def horse(x, y, t, c):
    far = (int(c[0] * 0.75), int(c[1] * 0.75), int(c[2] * 0.75)) # a 25% darker version of the colour for the far-side legs
    pushMatrix()
    translate(x, y + sin(t * 2) * 5)
    scale(1.4) # make the horse 1.4x bigger
    rotate(sin(t) * 0.03) # rock the whole horse slightly back and forth


    # far-side legs (slightly darker for depth)
    leg(45, 0, t + 2.7, far, True) # far front leg (dark colour, timing offset by 2.7)
    leg(-75, -5, t + 0.5, far, False) # far back leg (dark colour, timing offset by 0.5)

    # tail
    noFill() # the tail is just lines, no filled shape
    stroke(*c)
    swish = sin(t * 2) * 12 # how far the tail swings up/down this frame (up to 12px)
    for k in range(4): # draw 4 strands of tail
        strokeWeight(7 - k)
        bezier(-118, -42, -150, -50, -175, -30 + swish, -205, -12 + swish + k * 9) # curved strand

    # body, neck and head
    noStroke() # no outline on the body
    fill(*c) # fill the body with the horse's colour
    beginShape()
    pts = [(-120, -40), (-95, -55), (-30, -48), (35, -62), (70, -95),
           (105, -128), (125, -120), (165, -75), (170, -62), (155, -55),
           (125, -80), (100, -85), (85, -55), (80, -15), (60, 10),
           (30, 15), (-30, 18), (-70, 10), (-118, -5)]
    curveVertex(*pts[-1])
    for p in pts: # go through every outline point
        curveVertex(*p)
    curveVertex(*pts[0])
    curveVertex(*pts[1])
    endShape(CLOSE) # finish and close the body shape
    ellipse(-85, -15, 75, 70)

    # ear
    triangle(104, -124, 112, -152, 121, -121) # small pointed triangle on top of the head

    # mane
    stroke(*c) # mane lines in the horse's colour
    strokeWeight(5)
    for k in range(8): # 8 strands of mane
        mx = lerp(40, 105, k / 7.0)
        my = lerp(-62, -128, k / 7.0)
        line(mx, my, mx - 20, my + 4 + sin(t * 3 + k) * 4) # strand flowing backwards, flicking up and down as it runs

    # eye and nostril
    noStroke() # no outline
    fill(*EYE) # off-white colour
    ellipse(132, -104, 7, 5) # the eye (small oval)
    ellipse(162, -66, 4, 4) # the nostril (tiny circle)

    # near-side legs
    leg(55, 0, t + 2.2, c, True)
    leg(-85, -5, t, c, False)

    popMatrix()

def leg(hx, hy, t, c, front): # draws one leg from hip
    a = sin(t) * 0.55 # upper leg angle: swings back and forth
    bend = max(0, -cos(t)) * 1.2
    if front:
        b = a - bend # bend the knee backwards
    else:
        b = a + bend * 0.7
    kx = hx + sin(a) * 45
    ky = hy + cos(a) * 45
    fx = kx + sin(b) * 42
    fy = ky + cos(b) * 42
    stroke(*c)
    strokeWeight(17) # thick line for the upper leg
    line(hx, hy, kx, ky)
    strokeWeight(9)
    line(kx, ky, fx, fy) # draw knee to foot
    strokeWeight(12)
    line(fx, fy, fx + sin(b) * 7, fy + cos(b) * 7)

def keyPressed(): # runs whenever a key is pressed
    if key == 's':
        save("horses.png") # save the current frame as horses.png in the sketch folder

YELLOW = (245, 196, 0) # RGB colour for the yellow stripes
NAVY   = (20, 33, 61) # RGB colour for the navy stripes (and background)

STRIPE_WIDTH = 90      # thickness of each stripe 
ANGLE        = 0       # 0 = vertical, 90 = horizontal, 45 = diagonal 
SPEED        = 2.0     # how fast the stripes slide (pixels per frame)
WAVE         = 0       # 0 = straight, try 30 for wavy
WAVE_LENGTH  = 400
WAVE_SPEED   = 0.03    # how fast the waves ripple

offset = 0 # how far the stripes have slid so far (starts at 0)
phase = 0 # where the wave ripple is up to (starts at 0)
recording = False


def setup(): # runs once when the sketch starts
    size(1080, 1920) # canvas size: 1080 x 1920 px (vertical Instagram Story format)
    frameRate(30) # run at 30 frames per second (a standard video frame rate)


def draw(): # runs over and over (30 times a second)
    global offset, phase # lets draw() change these variables
    background(*NAVY) # fill the whole canvas navy (wipes the last frame)
    draw_stripes() # draw all the stripes for this frame
    offset += SPEED # slide the stripes along a bit for the next frame
    phase += WAVE_SPEED
    if recording:
        saveFrame("frames/story-####.png")


def draw_stripes(): # draws the full set of stripes
    noStroke() # no outlines on the stripes
    diag = sqrt(width * width + height * height)
    pair = STRIPE_WIDTH * 2
    pushMatrix()
    translate(width / 2.0, height / 2.0) # move the origin to the centre of the canvas
    rotate(radians(ANGLE)) # turn the stripes to the chosen angle 
    x = -diag - pair + (offset % pair)
    i = 0
    while x < diag: # keep drawing stripes until the far edge is covered
        if i % 2 == 0:
            fill(*YELLOW) # make this stripe yellow
        else:
            fill(*NAVY) # make this stripe navy
        if WAVE == 0:
            rect(x, -diag, STRIPE_WIDTH, diag * 2)
        else:
            beginShape()
            y = -diag
            while y <= diag:
                vertex(x + WAVE * sin(TWO_PI * y / WAVE_LENGTH + phase), y)
                y += 10 # move down 10px
            y = diag # now start at the bottom
            while y >= -diag:
                vertex(x + STRIPE_WIDTH + WAVE * sin(TWO_PI * y / WAVE_LENGTH + phase), y)
                y -= 10 # move up 10px
            endShape(CLOSE) # close and fill the wavy stripe
        x += STRIPE_WIDTH # move across to where the next stripe starts
        i += 1
    popMatrix()


def keyPressed(): # runs whenever a key is pressed
    global recording
    if key in ('s', 'S'):
        save("stripes_story.png")
        println("Saved stripes_story.png")
    elif key in ('v', 'V'):
        recording = not recording
        println("Recording ON" if recording else "Recording OFF")

    

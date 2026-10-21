# Moving Yellow & Navy Stripes - Instagram Story (1080 x 1920)
# S = save a still PNG | V = start/stop recording frames for a video

YELLOW = (245, 196, 0)
NAVY   = (20, 33, 61)

STRIPE_WIDTH = 90      # thickness of each stripe
ANGLE        = 0       # 0 = vertical, 90 = horizontal, 45 = diagonal
SPEED        = 2.0     # how fast the stripes slide (pixels per frame)
WAVE         = 0       # 0 = straight, try 30 for wavy
WAVE_LENGTH  = 400
WAVE_SPEED   = 0.03    # how fast the waves ripple

offset = 0
phase = 0
recording = False


def setup():
    size(1080, 1920)
    frameRate(30)


def draw():
    global offset, phase
    background(*NAVY)
    draw_stripes()
    offset += SPEED
    phase += WAVE_SPEED
    if recording:
        saveFrame("frames/story-####.png")


def draw_stripes():
    noStroke()
    diag = sqrt(width * width + height * height)
    pair = STRIPE_WIDTH * 2
    pushMatrix()
    translate(width / 2.0, height / 2.0)
    rotate(radians(ANGLE))
    x = -diag - pair + (offset % pair)
    i = 0
    while x < diag:
        if i % 2 == 0:
            fill(*YELLOW)
        else:
            fill(*NAVY)
        if WAVE == 0:
            rect(x, -diag, STRIPE_WIDTH, diag * 2)
        else:
            beginShape()
            y = -diag
            while y <= diag:
                vertex(x + WAVE * sin(TWO_PI * y / WAVE_LENGTH + phase), y)
                y += 10
            y = diag
            while y >= -diag:
                vertex(x + STRIPE_WIDTH + WAVE * sin(TWO_PI * y / WAVE_LENGTH + phase), y)
                y -= 10
            endShape(CLOSE)
        x += STRIPE_WIDTH
        i += 1
    popMatrix()


def keyPressed():
    global recording
    if key in ('s', 'S'):
        save("stripes_story.png")
        println("Saved stripes_story.png")
    elif key in ('v', 'V'):
        recording = not recording
        println("Recording ON" if recording else "Recording OFF")

    

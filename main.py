# Trinket IO demo
# Welcome to CircuitPython :)

from touchio import *
from digitalio import *
from analogio import *
from board import *
import time
import neopixel
import random

# Capacitive touch on D1
touch = TouchIn(D1)

# NeoPixel strip (of 16 LEDs) connected on D3
NUMPIXELS = 25
neopixels = neopixel.NeoPixel(D3, NUMPIXELS, brightness=.1, auto_write=True)
DIRECTION = 1 # 1 == "up"
COLOR = 1 # 1 == "red"
MAXLITPIXELS = 10
CURLITPIXELS = 0

# COLORS
RED = (255, 0, 0)
DARKRED = (127, 0, 0)
ORANGE = (255, 165, 0)
DARKORANGE = (127, 83, 0)
WHITE = (125, 125, 125)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREEN = (0, 255, 0)
DARKGREEN = (0, 127, 0)
BLACK = (0, 0, 0)

COLORPALLET = [WHITE, RED, GREEN, RED, WHITE, RED, GREEN, GREEN, WHITE, RED, GREEN, RED, WHITE]
######################### HELPERS ##############################

# Helper to convert analog input to voltage
# def getVoltage(pin):
#     return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def flicker(idx, rgbVal):
    neopixels[idx] = rgbVal
    if idx > 2 and idx < NUMPIXELS -2:
        neopixels[idx -2] = rgbVal
        neopixels[idx -1] = rgbVal
    time.sleep(0.0125)
    neopixels[idx] = (0, 0, 0)

def rainbowPulse(i):
    for p in range(NUMPIXELS):
        idx = int ((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)

def redPulse():
    aPixel = neopixels[0]
    rCur = aPixel[0]
    gCur = aPixel[1]
    bCur = aPixel[2]

    if DIRECTION == 1:
        neopixels.fill((rCur + 10, gCur, bCur))

    if DIRECTION == 2:
        neopixels.fill((rCur - 10, gCur, bCur))

def whitePulse():
    for p in range(NUMPIXELS):
        neopixels[p] = (255, 255, 255)
    time.sleep(.0125)
    for p in range(NUMPIXELS):
        neopixels[p] = (0, 0, 0)

def chase(chaseColor):
    inverseChaseColor = chaseColor
    ## neopixels.fill((0, 0, 0))
    for p in range(NUMPIXELS):
        if inverseChaseColor == 0:
            neopixels[p] = (255, 0, 0)
            inverseChaseColor = 1
        else:
            neopixels[p] = (255, 255, 255)
            inverseChaseColor = 0
        ## print("pixel p should be", p)
        ## print("inverseChaseColor should be: ", inverseChaseColor)
        ## time.sleep(.25)

def kittPulse():
    for p in range(NUMPIXELS):
        neopixels[p] = (255,255,255)
        if p > 2:
            neopixels[p-3] = (255,0,0)
        if p > 7:
            neopixels[p-6] = (0, 0, 0)
        time.sleep(.015)

def dimmer():
    for p in range(NUMPIXELS):
        aPixel = neopixels[p]
        rCur = aPixel[0]
        gCur = aPixel[1]
        bCur = aPixel[2]
        rNew = 0
        gNew = 0
        bNew = 0
        if rCur > 25 or gCur >25 or bCur > 25:
            rNew = rCur - 20
            gNew = gCur - 20
            bNew = bCur - 20
            if (rNew < 0):
                rNew = 0
            if (gNew < 0):
                gNew = 0
            if (bNew < 0):
                bNew = 0

            # print(rNew)
            neopixels[p] = (rNew, gNew, bNew)
        else:
            neopixels[p] = (0,0,0)
    time.sleep(.0125) # make bigger to slow down

######################### MAIN LOOP ##############################

i = 0;
curLitPixels = 0
while True:
    if touch.value:
        neopixels.brightness = 1
        neopixels.fill(BLACK)
        flicker(random.randint(0, (NUMPIXELS-1)),(WHITE))
    else:
        neopixels.brightness = .1
        ## How many pixels are currently lit?
        curLitPixels = 0
        for x in range (NUMPIXELS):
            aPixel = neopixels[x]
            if aPixel[0] > 0 or aPixel[1] > 0 or aPixel[2] > 0:
                curLitPixels += 1
        CURLITPIXELS = curLitPixels

        ## Select a random pixel and fill it with a color
        if (CURLITPIXELS < MAXLITPIXELS) and (random.randint(0, 10) > 3):
            neopixels[random.randint(0, (NUMPIXELS-1))] = COLORPALLET[random.randint(0,12)]

        ## for each pixel, step it down
        dimmer()
    


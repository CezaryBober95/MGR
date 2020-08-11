#from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
import time

import busio
import board

import numpy as np
from scipy.interpolate import griddata

from colour import Color

import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)

#low range of the sensor (this will be blue on the screen)
MINTEMP = 27

#high range of the sensor (this will be red on the screen)
MAXTEMP = 33

#how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

#initialize the sensor
sensor = Adafruit_AMG88xx()
# Points grid 8x8 0,0 - 7,7
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
print(points)
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
#print("X",grid_x)
#print("Y",grid_y)

#sensor is an 8x8 grid so lets do a square
height = 540
width = 540

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
# not here

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
# not here
lcd.fill((255,0,0))

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0,0,0))
pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#let the sensor initialize
time.sleep(.1)
    
while(1):

    #read the pixels
    pixels = sensor.readPixels()
    pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    #print("Pixels",pixels,"\n")
    text=open("sample_output.txt","w")
    text.writelines(str(pixels))
    text.close()
        
    #perdorm interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    
    #draw everything
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
    pygame.display.update()
    
    
    while True:
            for row in amg.pixels:
                print(["{0:.1f}".format(temp) for temp in row])
                print("")
            print("\n")
    

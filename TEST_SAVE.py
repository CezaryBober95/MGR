"""This example is for Raspberry Pi (Linux) only!
It will not work on microcontrollers running CircuitPython!"""
import os
import math
import time
import busio
import board
import numpy as np
import pygame
from scipy.interpolate import griddata
from colour import Color
import adafruit_amg88xx
import os.path

name= "TEST_2"
#------------------------------------------------------------------------------------------
def coordinate_max(array):
    cor=np.where(array == array.max())
    array_i, array_j= cor[0], cor[1]
    array_i, array_j=int(array_i), int(array_j)
    return(array_i,array_j) # tuple

def coordinate_min(array):
    cor=np.where(array == array.min())
    array_i, array_j= cor[0], cor[1]
    array_i, array_j=int(array_i), int(array_j)
    return(array_i,array_j) # tuple

def value_check(array,row,col):
    max_temp=(array[row][col])
    return max_temp

def Raport(array,max, min,name,obs):
    animal_name = "Raport_%(name)s.txt" % {'name': name}
    if os.path.exists(animal_name) == False:
        raport = open(animal_name, "w")
    start = "\nAMG88xx pixels\n-- Pixels Test --\n\n"
    obs="Obserwacja: %s" % (obs+1)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    hour = "\n\nCzas pomiaru: %s" % current_time
    max_C = "\nMaksymalna temperatura: %s C" % str(max)
    min_C = "\nMinimalna temperatura: %s C\n\n" % str(min)
    raport=open(animal_name,"a")
    raport.write(obs)
    raport.write(start)
    raport.write(str(array))
    raport.write(hour)
    raport.write(max_C)
    raport.write(min_C)
    raport.close()

def temperature_raport(max,min,name,obs):
    animal_name = "Temp_raport_%(name)s.txt" % {'name': name}
    if os.path.exists(animal_name) == False:
        raport = open(animal_name, "w")
    obs = "Obserwacja: %s -> " % (obs+1)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    hour = "%s," % str(current_time)
    max_C = "%s," % str(max)
    min_C = "%s\n" % str(min)
    raport_temp = open(animal_name, "a")
    raport_temp.write(obs)
    raport_temp.write(hour)
    raport_temp.write(max_C)
    raport_temp.write(min_C)
    raport_temp.close()
#------------------------------------------------------------------------------------------

i2c_bus = busio.I2C(board.SCL, board.SDA)

#low range of the sensor (this will be blue on the screen)
MINTEMP = 25
#high range of the sensor (this will be red on the screen)
MAXTEMP = 28

#how many color values we can have
COLORDEPTH = 1024
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# pylint: enable=invalid-slice-index
#sensor is an 8x8 grid so lets do a square
height = 240
width = 240

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))
pygame.display.update()
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
i=0
#let the sensor initialize
time.sleep(.1)
while True:
    time.sleep(1)
    #read the pixels
    pixels = []
    for row in sensor.pixels:
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

    #perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')

    #draw everything
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                                (displayPixelHeight * ix, displayPixelWidth * jx,
                                displayPixelHeight, displayPixelWidth))

#----------------------------------------------------------------------------------------------------------------------------------------
    i2c = busio.I2C(board.SCL, board.SDA)
#    amg=adafruit_amg88xx.AMG88XX(i2c)

    Matrix=[]
    
    for row in sensor.pixels:
        Matrix.append(['{0:.2f}'.format(temp) for temp in row])

#   my_array=np.array(Matrix)
    my_array1=np.asfarray(Matrix,float)
    print(my_array1)
    Raport(my_array1,np.max(my_array1),np.min(my_array1),name,i+1)
   # cor_ij_max = coordinate_max(my_array1)
   # cor_ij_min = coordinate_min(my_array1)
   # Raport(my_array1, value_check(my_array1, cor_ij_max[0], cor_ij_max[1]), value_check(my_array1, cor_ij_min[0], cor_ij_min[1]),name,i)
   # temperature_raport(value_check(my_array1, cor_ij_max[0], cor_ij_max[1]), value_check(my_array1, cor_ij_min[0], cor_ij_min[1]),name,i)
       # time.sleep(1)
    print ("Raport %i" % (i+1))
    i=i+1
    print("\n")
    
    pygame.display.update()

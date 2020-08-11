import time
import busio
import board
import adafruit_amg88xx
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)
#for i in range(5):
while True:
	Array=[]
	#while True:
	for row in amg.pixels:
		Array.append(['{0:.1f}'.format(temp) for temp in row])
		print("")
	#print('Array')
	#print(Array)
	#print(type(Array))
	my_array=np.array(Array)
	#print('My_array')
	Matrix=np.asfarray(my_array,float)
	print(Matrix)
	print(np.max(Matrix))
	print(np.min(Matrix))
	#print(type(my_array))
	print("\n")
	time.sleep(1)

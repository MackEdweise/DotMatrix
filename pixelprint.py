"""
-------------------------------------------------------
run1.py
Main program for security system
-------------------------------------------------------
Author:  William Yang & Marcus Edwards
Version: 2015-12-20
-------------------------------------------------------
"""
import time
import RPi.GPIO as GPIO
import urllib2
import os

# Letters and Numbers
import alphanumeric

# 5x8 LED Matrix row pins
pin_r1 = 5
pin_r2 = 6
pin_r3 = 13
pin_r4 = 19
pin_r5 = 26

# 5x8 LED Matrix col pins
pin_c1 = 21
pin_c2 = 20
pin_c3 = 16
pin_c4 = 12

# Time to wait before next letter
PAUSE_INTERVAL = 300

# Time it takes to scan col
COL_SCAN = 0.0001

# Time it taks to scan row
ROW_SCAN = 0.0008

# Number of cols
NUM_COLS = 8


"""
-------------------------------------------------------
Main LED Matrix class
-------------------------------------------------------
"""
class LEDMatrixControl:

	def __init__(self):
		"""
		---------------------------------------------------------
		constructor
		---------------------------------------------------------
		"""

		self.row_ctrl = [pin_r1, pin_r2, pin_r3, pin_r4, pin_r5]
		self.col_ctrl = [pin_c1, pin_c2, pin_c3, pin_c4]

		GPIO.setmode(GPIO.BCM)

		for each in self.row_ctrl:
			GPIO.setup(each, GPIO.OUT)
		
		for each in self.col_ctrl:
			GPIO.setup(each, GPIO.OUT)

	def _decToBinPadded(self, decimal):

		"""
		---------------------------------------------------------
		private method to convert decimal to binary, then pad 0's
		---------------------------------------------------------
		"""
		
		raw = str(bin(decimal))
		part = raw[2:]
		final = part.zfill(4)
		
		a = True if final[0] == "1" else False
		b = True if final[1] == "1" else False
		c = True if final[2] == "1" else False
		d = True if final[3] == "1" else False
	
		return [a, b, c, d]

	def matrixPrint(self, user_str):
		"""
		---------------------------------------------------------
		main print function. 
		Use LEDMatrixControlObj.matrixPrint("YOUR TEXT 123.456")
		---------------------------------------------------------
		"""
		pipeline = []
		for each in user_str:
			print(each)
			pipeline.append(alphanumeric.pixelize(each))
		self._printPipeline(pipeline, True)

	def matrixPrintRepeat(self, user_str):
		"""
		---------------------------------------------------------
		main print function repeating. 
		Use LEDMatrixControlObj.matrixPrintRepeat("YOUR TEXT 123.456")
		---------------------------------------------------------
		"""
		pipeline = []
		for each in user_str:
			print(each)
			pipeline.append(alphanumeric.pixelize(each))
		self._printPipeline(pipeline, False)

	def _printPipeline(self, chars, mode):
		"""
		---------------------------------------------------------
		Internal printer pipeline
		---------------------------------------------------------
		"""
		order = 0
		count = 0
		i = 0
		repeat = True
	
		while repeat:

			current = chars[order]
			for each in self.row_ctrl:
				GPIO.output(each, True)

			j = 0		
			if(count == PAUSE_INTERVAL and order < len(chars)):
				count = 0
				order = order + 1
		
				if(order == len(chars)):
					order = 0	
					if(mode):
						repeat = False	
		
			count = count + 1	
			while(j < NUM_COLS):
		
				answer = self._decToBinPadded(j)

				for i in range(0, len(self.col_ctrl)):
					GPIO.output(self.col_ctrl[i], answer[i])
		
				for i in range(0, len(self.row_ctrl)):
					if(i in current[len(current) - j - 1]):
						GPIO.output(self.row_ctrl[i], False)
					else:
						GPIO.output(self.row_ctrl[i], True)
						
				j += 1
		
				time.sleep(COL_SCAN)
			time.sleep(ROW_SCAN)
		
			if(i == 4):
				i = 0
			else:
				i += 1

# Simple calibration test
x = LEDMatrixControl()
x.matrixPrint("123 READY")

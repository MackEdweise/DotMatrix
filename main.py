"""
-------------------------------------------------------
run1.py
Main program for security system
-------------------------------------------------------
Author:  William Yang & Marcus Edwards
Version: 2015-12-20
-------------------------------------------------------
"""

import RPi.GPIO as GPIO                    
import time                                
import os
import alphanumeric
import letters
import pixelprint

GPIO.setmode(GPIO.BCM)                      

PR = 17
MOTOR = 22
TRIG = 23                                  
ECHO = 4                                  

DIST_CONVERSION_FACTOR=17150
SETTLE_TIME=2
H_LIMIT=400
L_LIMIT=2
TRIGGER_TIME=0.00001
TOLERANCE=0.5

GPIO.setup(MOTOR,GPIO.OUT)
GPIO.setup(PR,GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)                   

def getDistance():

  GPIO.output(TRIG, False)                 
  print "Waitng For Sensor To Settle"
  
  time.sleep(SETTLE_TIME) #allow sensor to settle

  GPIO.output(TRIG, True) #trigger sensor

  time.sleep(TRIGGER_TIME)                      

  GPIO.output(TRIG, False)                 

  while GPIO.input(ECHO)==0: #find time between trigger and echo              

    pulse_start = time.time()              

  while GPIO.input(ECHO)==1:               

    pulse_end = time.time()                 

  pulse_duration = pulse_end - pulse_start 

  distance = pulse_duration * DIST_CONVERSION_FACTOR  #convert time to corresponding distance

  distance = round(distance, 2)   

  if distance > L_LIMIT and distance < H_LIMIT: #print distance or "out of range" for debugging     

    print "Distance:",distance - TOLERANCE,"cm"

  else:

    print "Out Of Range"

  return distance #return distance


obj = pixelprint.LEDMatrixControl()

obj.matrixPrint("DIAMOND")

GPIO.output(MOTOR, 0) #initiaize the motor to not spin

intitialDistance = getDistance() # find ideal distance to the diamond

while True:

  m = curl 127.0.0.1:880/SetD/mstate  # get motor state from server

  GPIO.output(MOTOR, m) #turn on or off the motor
  
  distance = getDistance() # get current distance to the diamond

  curl 127.0.0.1:880/SetD/distance

  if (GPIO.input(17) == 0) or (abs(initialDistance - distance)>2):

    print("panic!")

    os.system("speaker-test -t sine -f 600") #sound alarm

    curl 127.0.0.1:880/PROFF #tell the server that the sensor has been tripped

  else:

    curl 127.0.0.1:880/PRON #tell the server that the sensors read safe conditions

import RPi.GPIO as GPIO
import time
import datetime
##import telepot
from time import gmtime, strftime, sleep
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25,GPIO.OUT) #GPIO25 as Trig
GPIO.setup(27,GPIO.IN) #GPIO27 as Echo
GPIO.setup(26,GPIO.OUT) #set GPIO 26 as output
PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26

##telegram
def handle(msg):
    global chat_id

    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Message received from ' + str(chat_id))

    if command == '/distance':
        bot.sendMessage(chat_id, 'hi')
        

#function to get distance:
def distance():
    GPIO.output(25,1)
    time.sleep(0.00001)
    GPIO.output(25,0)
    StartTime=time.time()
    StopTime=time.time()
    while GPIO.input(27)==0:
        StartTime=time.time()    
    while GPIO.input(27)==1:
        StopTime=time.time()
    ElapsedTime=StopTime-StartTime
    Distance=(ElapsedTime*34300)/2
    return Distance

##function to move motor
def servo(a):
    PWM.start(3) #3% duty cycle
    sleep(1) #allow time for movement
    PWM.start(12) #13% duty cycle
    requests.post("https://api.thingspeak.com/update?api_key=IR47IKYOJPBRYE0G&field1=%s" %(a))
    requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update',
                    json={'api_key':'PQ99B4KN0C6CFHC8','status':'Bowl has been refilled at %s' %(getTime()) })
    sleep(1) #allow time for movement
    
def getTime ():
    return strftime("%H:%M", gmtime())


while (True):
    a = distance()
    t = getTime()

    print(a)
    print(t)

    if(a > 235 and (t == '07:06' or t == '08:12' or t=='08:11')):
        servo(a)
    

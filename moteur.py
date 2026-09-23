import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)  ##je prefere la numerotation BOARD plutot que BCM
Moteur1A=16     ##premiere sortie du premier moteur,pin16
Moteur1B=18    ##deuxieme sortie du premier moteur,pin18
Moteur1E=22     ##enable du premier moteur,pin22
GPIO.setup(Moteur1A,GPIO.OUT)## ces 3 pins du Raspberry Pi sont des sorties
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
pwm1=GPIO.PWM(Moteur1E,50)##pwm de la pin 22 a une frequence 50 hz
pwm1.start(100)##on commence avec un rapport cyclique de 100%
print"Moteur dans le sens direct,rapide"
GPIO.output(Moteur1A,GPIO.HIGH)
GPIO.output(Moteur1B,GPIO.LOW)
GPIO.output(Moteur1E,GPIO.HIGH)
sleep(5)##on laisse tourner 5 secondes avec des parametres
print"Moteur dans le sens direct,lent"
pwm1.ChangeDutyCycle(20)##modification de rapport  cyclique à 20%
sleep(5)
print"Moteur dans le sens inverse,lent"
GPIO.output(Moteur1A,GPIO.LOW)
GPIO.output(Moteur1B,GPIO.HIGH)
sleep(5)
print"arret du moteur"
GPIO.output(Moteur1E,GPIO.LOW)
pwml.stop()##interruption du pwm
GPIO.cleanup()

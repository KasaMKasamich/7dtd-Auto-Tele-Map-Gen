import sys
import telnetlib
import time
import random
import asyncio

# Author: a4blue
#This is a python script to make a player automatically explore a random gen world in 7dtd
#Requires Python 3, Allocs Server Fixes and 7dtd


#Function defs

#Returns a list with Coordinates [x,y] in spiral form
def spiral(xs,ys,it,step):
	step = int(step)
	xs = int(xs)
	ys = int(ys)
	it = int(it)
	i = 0
	state = 4
	x = xs
	y = ys
	ret = []
	while i<it:
		if i == 0:
			i = 1
		else:
			if state == 1:
				if x < xs+(-i*step):
					state = 4
					continue
				else:
					x = x-step
			elif state == 2:
				if x > xs+i*step:
					i = i+1
					state = 3
					continue
				else:
					x = x+step
			elif state == 3:
				if y > ys+i*step:
					state = 1
					continue
				else:
					y = y+step
			elif state == 4:
				if y < ys+(-i*step):
					state = 2
					continue
				else:
					y = y-step
		ret.append([x,y])
	return ret

#Removes Negative Buffs from Teleporting player
def removeBuffs(PLAYER,tn):
	cmd = "debuffplayer "+PLAYER+" "
	debuffs = ["internalBleeding","brokenLeg","splint","sprainedLeg","burningSmall","burning","hungry","hungry2","thirsty","thirsty2","freezing","hypo1","hypo2","hypo3","overheated","heat1","heat2","wet","drowning","criticalBleedout","bleeding"]
	for x in debuffs:
		s = cmd+x+"\n"
		tn.write(str.encode(s))
		
#Teleports Player
def tele(x,y,PLAYER,tn):
	s = "tele "+PLAYER+" "+str(x)+" 0 "+str(y)+"\n"
	print(s)
	tn.write(str.encode(s))
	time.sleep(1)
	return

#Main Program starts here
#TODO Error handling
#TODO more customization
#TODO define values in a file and load it if available
HOST = input('Telnet Host:')
PORT = input('Telnet Port:')
PASSWORD = input('Telnet Passwort(if set):')
tn =  telnetlib.Telnet(HOST,PORT)
if PASSWORD:
	tn.read_until(b"Please enter password:")
	tn.write(str.encode(PASSWORD+"\n"))
tn.read_until(b"Press 'help' to get a list of all commands. Press 'exit' to end session.",10)
PLAYER = input('Player(must be online):')
MODE = input('Select mode(0=Start Spiral at 0,0;1=Random then choose Coordinate Start;2=Double Spiral at Coords):')


if MODE == '0':
	LOCx = 0
	LOCy = 0
	spir = spiral(LOCx,LOCy,100,80)
	for x in spir:
		tele(x[0],x[1],PLAYER,tn)
		removeBuffs(PLAYER,tn)
elif MODE == '1':
	RandNum = input('How many random locations to visit:')
	i = 0
	while i<int(RandNum):
		tele(random.randrange(-5000,5000,1),random.randrange(-5000,5000,1),PLAYER,tn)
		i = i+1
	print("For Coordinates look on the map !")
	LOCx = input('Choose x-Coord:')
	LOCy = input('Choose y-Coord:')
	spir = spiral(LOCx,LOCy,100,80)
	for x in spir:
		tele(x[0],x[1],PLAYER,tn)
		removeBuffs(PLAYER,tn)
elif MODE == '2':
	LOCx = input('Choose x-Coord:')
	LOCy = input('Choose y-Coord:')
	BigSpir = spiral(LOCx,LOCy,100,640)
	for scord in BigSpir:
		SmallSpir = spiral(scord[0],scord[1],4,80)
		for x in SmallSpir:
			tele(x[0],x[1],PLAYER,tn)
			removeBuffs(PLAYER,tn)

tn.write(b"exit\n")

input('Enter for exit')
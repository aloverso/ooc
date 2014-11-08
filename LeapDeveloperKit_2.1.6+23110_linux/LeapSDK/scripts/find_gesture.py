import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame
import time
import serial
from pygame.locals import *
import math

SCREENWIDTH = 700
SCREENHEIGHT = 700

class Model:
    def __init__(self):

        self.topfarleft_act = (255,0,0)
        self.topmidleft_act = (0,255,0)
        self.topmidright_act = (0,0,255)
        self.topfarright_act = (255,255,0)
        self.botfarleft_act = (255,0,255)
        self.botmidleft_act = (0,255,255)
        self.botmidright_act = (255,255,255)
        self.botfarright_act = (160,32,240)

        self.topfarleft_inact = (100,0,0)
        self.topmidleft_inact = (0,100,0)
        self.topmidright_inact = (0,0,100)
        self.topfarright_inact = (100,100,0)
        self.botfarleft_inact = (100,0,100)
        self.botmidleft_inact = (0,100,100)
        self.botmidright_inact = (100,100,100)
        self.botfarright_inact = (80,16,100)

        self.topfarleft = self.topfarleft_inact #8
        self.topmidleft = self.topmidleft_inact #9
        self.topmidright = self.topmidright_inact #7
        self.topfarright = self.topfarright_inact #6
        self.botfarleft = self.botfarleft_inact #4
        self.botmidleft = self.botmidleft_inact #5
        self.botmidright = self.botmidright_inact #3
        self.botfarright = self.botfarright_inact #2
    
    def update(self,state):
        if state==0:
            self.topmidright = self.topmidright_inact #7
            self.topfarright = self.topfarright_inact #6
            self.botmidright = self.botmidright_inact #3
            self.botfarright = self.botfarright_inact #2
        if state==1:
            self.topfarleft = self.topfarleft_inact #8
            self.topmidleft = self.topmidleft_inact #9
            self.botfarleft = self.botfarleft_inact #4
            self.botmidleft = self.botmidleft_inact #5
        if state==2:
            self.botfarright = self.botfarright_act
        if state==3:
            self.botmidright = self.botmidright_act
        if state==4:
            self.botfarleft = self.botfarleft_act
        if state==5:
            self.botmidleft = self.botmidleft_act
        if state==6:
            self.topfarright = self.topfarright_act
        if state==7:
            self.topmidright = self.topmidright_act
        if state==8:
            self.topfarleft = self.topfarleft_act
        if state==9:
            self.topmidleft = self.topmidleft_act

class View:
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        # pygame.draw.circle(self.screen, pygame.Color(255,0,0), (SCREENWIDTH/2, SCREENHEIGHT/2), self.model.r1)
        # pygame.draw.circle(self.screen, pygame.Color(0,255,0), (SCREENWIDTH/2, SCREENHEIGHT/2), self.model.r2)
        pygame.draw.arc(self.screen, pygame.Color(self.model.botfarright[0],self.model.botfarright[1],self.model.botfarright[2]), pygame.Rect(SCREENWIDTH/2-150, SCREENHEIGHT/2-100, 400,400), 0, math.pi/4,100)
        pygame.draw.arc(self.screen, pygame.Color(self.model.botmidright[0],self.model.botmidright[1],self.model.botmidright[2]), pygame.Rect(SCREENWIDTH/2-150, SCREENHEIGHT/2-100, 400,400), math.pi/4, math.pi/2,100)
        pygame.draw.arc(self.screen, pygame.Color(self.model.botmidleft[0],self.model.botmidleft[1],self.model.botmidleft[2]), pygame.Rect(SCREENWIDTH/2-150, SCREENHEIGHT/2-100, 400,400), math.pi/2, 3*math.pi/4,100)
        pygame.draw.arc(self.screen, pygame.Color(self.model.botfarleft[0],self.model.botfarleft[1],self.model.botfarleft[2]), pygame.Rect(SCREENWIDTH/2-150, SCREENHEIGHT/2-100, 400,400), 3*math.pi/4, math.pi,100)
        pygame.draw.arc(self.screen, pygame.Color(self.model.topfarright[0],self.model.topfarright[1],self.model.topfarright[2]), pygame.Rect(SCREENWIDTH/2-200, SCREENHEIGHT/2-150, 500,500), 0, math.pi/4,70)
        pygame.draw.arc(self.screen, pygame.Color(self.model.topmidright[0],self.model.topmidright[1],self.model.topmidright[2]), pygame.Rect(SCREENWIDTH/2-200, SCREENHEIGHT/2-150, 500,500), math.pi/4, math.pi/2,70)
        pygame.draw.arc(self.screen, pygame.Color(self.model.topmidleft[0],self.model.topmidleft[1],self.model.topmidleft[2]), pygame.Rect(SCREENWIDTH/2-200, SCREENHEIGHT/2-150, 500,500), math.pi/2, 3*math.pi/4,70)
        pygame.draw.arc(self.screen, pygame.Color(self.model.topfarleft[0],self.model.topfarleft[1],self.model.topfarleft[2]), pygame.Rect(SCREENWIDTH/2-200, SCREENHEIGHT/2-150, 500,500), 3*math.pi/4, math.pi,70)

        pygame.display.update()

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        frame = controller.frame()

        # state=0 is fist right
        # state=1 is fist left
        # state=2 is FRONT (low) splay right down
        # state=3 is FRONT (low) splay right up
        # state=4 is FRONT (low) splay left down
        # state=5 is FRONT (low) splay left up
        # state=6 is BACK (high) splay right down
        # state=7 is BACK (high) splay right up
        # state=8 is BACK (high) splay left down
        # state=9 is BACK (high) splay left up

        for hand in frame.hands:


            #Figure out left or right hand
            handType = "Left hand" if hand.is_left else "Right hand"
            #print "  %s, id %d, position: %s" % (
                #handType, hand.id, hand.palm_position)


            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            fistOrSplayed = 1
            leftOrRight = 0
            upOrDown = 0

            #figure out high or low
            if hand.palm_position[1]>150.0:
                elevation = 1 #high 
            else:
                elevation = 0

            print "elevation",elevation

            #figure out palm up or down
            if hand.palm_normal[1]>0.0:
                upOrDown = 1
            else:
                upOrDown = 0

            print "upOrDown",upOrDown

            #fist or splayed
            for finger in hand.fingers:
                if finger.direction.angle_to(direction) > 1.8:
                    fistOrSplayed = 1 #fist
                else:  
                    fistOrSplayed = 0 #splayed

            print "fistOrSplayed",fistOrSplayed

            if handType == "Left hand":
                leftOrRight = 1 #left
            else:
                leftOrRight = 0 #right

            print "leftOrRight",leftOrRight

            if fistOrSplayed == 1: #fists
                if leftOrRight == 0: #right fist
                    state = 0
                if leftOrRight == 1: #left fist
                    state = 1

            if fistOrSplayed == 0: #splay
                if leftOrRight== 0: #right splay
                    if upOrDown == 0 and elevation == 0: #down and low
                        state = 2
                    if upOrDown == 1 and elevation == 0: #up and low
                        state = 3
                    if upOrDown == 0 and elevation == 1: #down and high
                        state = 6
                    if upOrDown == 1 and elevation == 1: #up and high
                        state = 7
            
                if leftOrRight == 1: #left splay
                    if upOrDown == 0 and elevation == 0: #down and low
                        state = 4
                    if upOrDown == 1 and elevation == 0: #up and low
                        state = 5
                    if upOrDown == 0 and elevation == 1: #down and high
                        state = 8
                    if upOrDown == 1 and elevation == 1: #up and high
                        state = 9

            print state
            # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            # ser.write(str(state)+'@')

            if state==2:
                if violin not in sounds:
                    sounds.append(violin)
                    violin.play(loops=10)
            elif state==3:
                if cello not in sounds:
                    sounds.append(cello)
                    cello.play(loops=10)
            elif state==4:
                if harp not in sounds:
                    sounds.append(harp)
                    harp.play(loops=10)        
            elif state==5:
                if drums not in sounds:
                    sounds.append(drums)
                    drums.play(loops=10)        
            elif state==6:
                if trumpet not in sounds:
                    sounds.append(trumpet)
                    trumpet.play(loops=10)        
            elif state==7:
                if trombone not in sounds:
                    sounds.append(trombone)
                    trombone.play(loops=10)
            elif state==8:
                if flute not in sounds:
                    sounds.append(flute)
                    flute.play(loops=10)
            elif state==9:
                if piano not in sounds:
                    sounds.append(piano)
                    piano.play(loops=10)
            elif state==0:
                if violin in sounds:
                    sounds.remove(violin)
                    violin.stop()
                if cello in sounds:
                    sounds.remove(cello)
                    cello.stop()
                if trumpet in sounds:
                    sounds.remove(trumpet)
                    trumpet.stop()
                if trombone in sounds:
                    sounds.remove(trombone)
                    trombone.stop()
            elif state==1:
                if harp in sounds:
                    sounds.remove(harp)
                    harp.stop()
                if drums in sounds:
                    sounds.remove(drums)
                    drums.stop()
                if flute in sounds:
                    sounds.remove(flute)
                    flute.stop()
                if piano in sounds:
                    sounds.remove(piano)
                    piano.stop()

            model.update(state)
            view.draw()


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."    
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":

    pygame.init()

    size = (SCREENWIDTH,SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    model = Model()
    view = View(model,screen)

    state = 0
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8)
    sounds = []
    violin = pygame.mixer.Sound('./instr/violin2cut.wav')
    trumpet = pygame.mixer.Sound('./instr/trumpet2cut.wav')
    cello = pygame.mixer.Sound('./instr/cello2cut.wav')
    harp = pygame.mixer.Sound('./instr/harp2cut.wav')
    trombone = pygame.mixer.Sound('./instr/trombone2cut.wav')
    piano = pygame.mixer.Sound('./instr/piano2cut.wav')
    flute = pygame.mixer.Sound('./instr/flute2cut.wav')
    drums = pygame.mixer.Sound('./instr/drums2cut.wav')

    main()

    pygame.quit()

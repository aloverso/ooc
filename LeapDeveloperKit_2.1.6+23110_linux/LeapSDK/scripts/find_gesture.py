import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame
import time

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

        hand = frame.hands[0]


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
            if finger.direction.angle_to(direction) > 1.5:
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
        #return state

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
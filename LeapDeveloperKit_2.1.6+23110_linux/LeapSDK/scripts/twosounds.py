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
        
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            #print normal
            direction = hand.direction

            splayed = True

            for finger in hand.fingers:
                if finger.direction.angle_to(direction) > 1.5:
                    splayed = False
            if splayed:
                print handType,"splayed"
            else:
                print handType,"fist"

            init_sound = sounds[:]

            if handType == "Left hand" and splayed and violin not in sounds:
                sounds.append(violin)
                violin.play()
            elif handType == "Left hand" and not splayed and violin in sounds:
                sounds.remove(violin)
                violin.stop()
            if handType == "Right hand" and splayed and trumpet not in sounds:
                sounds.append(trumpet)
                trumpet.play()
            elif handType == "Right hand" and not splayed and trumpet in sounds:
                sounds.remove(trumpet)
                trumpet.stop()

            # if not sounds == init_sound:
            #     for sound in sounds:
            #         sound.play()


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


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)
#pygame.mixer.pre_init(44100, -16, 2, 2048)
#pygame.init()
print "hey I finaly got this working!"
sounds = []
# mozart = './MidiFiles/symphony_183_1_(c)ishii.mid'
# other = './MidiFiles/symphony_38_504_1_(c)cvikl.mid'
violin = pygame.mixer.Sound('./violin.wav')
trumpet = pygame.mixer.Sound('./trumpet.wav')


# sounds.append(violin)
# sounds.append(trumpet)
# for sound in sounds:
#     sound.play()
# time.sleep(10)
main()
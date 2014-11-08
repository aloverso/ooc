import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

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


        state = 0
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
    main()
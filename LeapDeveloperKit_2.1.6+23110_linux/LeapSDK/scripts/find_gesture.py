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

        hand = frame.hands[0]

        handType = "Left hand" if hand.is_left else "Right hand"
        #print "  %s, id %d, position: %s" % (
            #handType, hand.id, hand.palm_position)

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        #print normal
        direction = hand.direction

        state = 0

        for finger in hand.fingers:
            if finger.direction.angle_to(direction) > 1.5:
                state = 1 #fist
            else:
                state = 2 #splayed = True
        if state == 1:
            print handType,"fist"

        elif state == 2:
            if hand.palm_normal[1]>0.0:
                print handType,"up and splayed"
            else:
                print handType, "down and splayed"
        else:
            state = 0



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
#!/usr/bin/env python

import mido as md
import pygame, pygame.midi
import time


def read_midi(track):
    pygame.init()
    pygame.midi.init()
    mozart = md.MidiFile('./MidiFiles/symphony_38_504_1_(c)cvikl.mid')

    print pygame.midi.get_default_output_id()
    print pygame.midi.get_device_info(0)

    #set up the output port for the mido data and the input port in pygame
    # md.get_output_names()
    # pygame_port = md.backend.pygame
    # in_port = pygame.midi.input()
    player = pygame.midi.Output(0)
    player.set_instrument(0, 1)
    print('playing')
    player.note_on(64, 277,1)
    time.sleep(1)
    player.note_off(64,277,1)
    print('played')

    # in_port.input(out_port)


    # for message in mozart.play():
    #   print(message)
    #   out_port.send(message)
    #   # out_port.send(message)

    # for i, track in enumerate(mozart.tracks):
        # print('Track {}: {}'.format(i, track.name))
        # print track.name
        # for message in track:
            # print(message)

    del player

if __name__ == '__main__':
    read_midi(1)

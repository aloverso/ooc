import mido as md
import pygame

pygame.init()
pygame.midi.init()
def read_midi(track):
	mozart = md.MidiFile('./MidiFiles/symphony_38_504_1_(c)cvikl.mid')

	#set up the output port for the mido data and the input port in pygame
	md.get_output_names()
	pygame_port = md.backend.pygame
	in_port = pygame.midi.input()
	out_port = pygame_port.open_output()
	in_port.input(out_port)


	for message in mozart.tracks[track]:
		# print(message)
		out_port.send(message)

	# for i, track in enumerate(mozart.tracks):
		# print('Track {}: {}'.format(i, track.name))
		# print track.name
		# for message in track:
			# print(message)



if __name__ == '__main__':
	read_midi(1)

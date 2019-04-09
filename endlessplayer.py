#!/usr/bin/python
# This class handles the generation of a new song given a markov chain
# containing the note transitions

from src.markov_chain import MarkovChain
import random
import numpy as np
import fluidsynth

# SPECIFICS
OVERHEAD = 10000

class EndlessPlayer:

    def __init__(self, markov_chain, main_notes, phrase_length, bpm, channels = 2, rate = 44100, channel = 0, velocity = 100):
        self.markov_chain = markov_chain
        self.fs = fluidsynth.Synth()
        self.seq = fluidsynth.Sequencer()
        self.channels = channels
        self.rate = rate
        self.synthID = self.seq.register_fluidsynth(self.fs)
        self.mySeqID = None
        self.channel = channel
        self.velocity = velocity
        self.now = 0
        self.buffer_notes = phrase_length
        self.last_note = None
        self.main_notes = main_notes
        self.note_duration = 2500
        self.bpm = bpm
        # Calculate note interval based on bpm
        self.note_interval = 60*1000 / (2 * self.bpm)

    @staticmethod
    def load(markov_chain, main_notes, phrase_length, bpm):
        assert isinstance(markov_chain, MarkovChain)
        # print ('Is markov chain:', isinstance(markov_chain, MarkovChain))
        return EndlessPlayer(markov_chain, main_notes, phrase_length, bpm)

    def schedule_next_callback(self, callbackinterval):
        # I want to be called back before the end of the next sequence
        callbackdate = int(self.seq.get_tick() + callbackinterval)
        self.seq.timer(callbackdate, dest = self.mySeqID)

    def schedule_next_sequence(self):
        # Get current sequencer tick
        self.now = self.seq.get_tick()
        # Pick from the initial notes randomly
        self.last_note = random.choice(self.main_notes)
        # Generate the notes ( to be played in now + overhead)
        for i in range(self.buffer_notes):
            # Get notes
            new_notes = self.markov_chain.get_next(self.last_note)
            # Split them into chords, or nothing
            new_note_list = new_notes.split(',')
            # Ignore sequence number
            for note in new_note_list[1:]:
                # Checkout for silences
                if note != '':
                    self.seq.note(time = int(self.now + i*self.note_interval + OVERHEAD), 
                                    absolute = True, 
                                    channel = self.channel, 
                                    key = int(note), 
                                    duration = self.note_duration, 
                                    velocity = self.velocity, 
                                    dest = self.synthID)
            # Put the seed in the next note
            self.last_note = new_notes
        # Schedule the next callback
        self.schedule_next_callback(self.buffer_notes*self.note_interval)

    def seq_callback(self, time, event, seq, data):
        self.schedule_next_sequence()

    def sequencer_starter(self, SF2):
        # This function starts the fluidsynth audio
        # Visit the help for driver/midi_driver combinations. For MAC users, coreaudio
        self.fs.start(driver= "coreaudio", midi_driver="coremidi")
        # Load the Soundfont file. Find samples of acoustic pianos online
        sfid = self.fs.sfload(SF2)
        print ('Using SoundFont File', SF2)
        self.fs.program_select(0, sfid, 0, 0)

        # Register the callback
        self.mySeqID = self.seq.register_client("mycallback", self.seq_callback)
        self.now = self.seq.get_tick()
        
        # Start the sequencer
        self.schedule_next_sequence()

    def play(self):
        # Endless player
        while True:
            pass

    def kill(self):
        # Cleanup everything
        self.seq.delete()
        self.fs.delete()

if __name__ == "__main__":
    import sys
    # Usage: python endlessplayer.py instructions/instructions.json soundfont/soundfont.sf2
    if len(sys.argv) == 3:

        SF2 = sys.argv[2]
        from src.phrase_parser import PhraseParser
        # Parse the instructions
        phraseParser = PhraseParser(sys.argv[1], False)
        # Retrieve the markov chain
        chain = phraseParser.get_chain()
        # Retrieve the initial chain
        main_notes = phraseParser.get_init_notes()
        # Retrieve phrase length and bpm
        phrase_length = phraseParser.get_length()
        bpm = phraseParser.get_bpm()

        print("Generated markov chain. Playing.")
        # Start the player object
        player = EndlessPlayer.load(chain, main_notes, phrase_length, bpm)
        player.sequencer_starter(SF2)
        # Play endlessly until there's a keyboard interrupt
        try:
            player.play()
        except KeyboardInterrupt:
            player.kill()
            raise SystemExit
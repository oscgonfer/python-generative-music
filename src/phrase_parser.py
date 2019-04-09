#!/usr/bin/python
# This class handles the parsing of a midi file and builds a markov
# chain from it.

import hashlib
import json
from src.markov_chain import MarkovChain
import numpy as np

class PhraseParser:

    def __init__(self, filename, verbose=False):
        """
        This is the constructor for a Serializer, which will serialize
        a midi given the filename. It will generate buckets for the different phrases in it
        and generate a markov chain of the different phrases in them.
        """
        self.filename = filename
        self.markov_chain = MarkovChain()
        self.initial_notes = []
        self.bpm = None
        self.song_length = None
        self.phraseLength = None
        self._parse(verbose=verbose)
        
    def _parse(self, verbose=False):
        """
        This function handles the reading of the midi and chunks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        instructions = json.load(open(self.filename, 'rb'))
        self.bpm = instructions['header']['bpm']
        self.ticks_per_beat = instructions['header']['PPQ']
        self.song_length = instructions['duration']
        self.phraseLength = instructions['phraseLength']

        print ('Parsing file:', self.filename)
        print ('Title', instructions['header']['name'])  
        print ('BPM', self.bpm)  

        EIGHTH_NOTE_INTERVAL_S = 60 / (2*self.bpm)

        # Parse the messages into buckets for each half-beat. Put them in 32-beat chunks
        chunks = []
        current_chunk = []
        index = 0
        for time in np.arange(0, self.song_length, EIGHTH_NOTE_INTERVAL_S):
            for message in instructions['tracks'][1]['notes']:
                if (message['time'] >= time and message['time'] < time + EIGHTH_NOTE_INTERVAL_S):
                    current_chunk.append(str(message['midi']))
            chunks.append(current_chunk)
            index += 1
            current_chunk = []

        # For each bucktet, create parsed messages
        phrases = []
        current_phrase = []
        current_phrase_parsed = []
        for phrase_index in range(self.phraseLength):
            current_phrase = chunks[phrase_index*self.phraseLength:(phrase_index+1)*self.phraseLength]
            index_word = 0
            for word in current_phrase:
                word_parsed = str(index_word) + ',' + ','.join(word)
                if index_word == 0:
                    self.initial_notes.append(word_parsed)
                current_phrase_parsed.append(word_parsed)
                index_word += 1
            phrases.append(current_phrase_parsed)
            current_phrase_parsed = []
            current_phrase=[]

        # Put them in the markov-chain
        for phrase in phrases:
            self._sequence(phrase)
        
        # Print out the resulting chunks
        if verbose:
            print ('Initial notes', self.initial_notes)
            print ('Matrix')
            self.markov_chain.print_as_matrix(20)
        
    def _sequence(self, phrase):
        """
        Given the current phrase of notes, this function
        runs through the each transition and sticks them into the markov chain.
        """
        for index in range(len(phrase)-1):
            self.markov_chain.add(
                phrase[index], phrase[index+1])

        # Add last as a dead-end state
        self.markov_chain.add(phrase[index+1], phrase[index+1])

    def get_chain(self):
        return self.markov_chain

    def get_init_notes(self):
        return self.initial_notes

    def get_bpm(self):
        return self.bpm

    def get_length(self):
        return self.phraseLength
#!/usr/bin/python
# This class handles the storage and manipulation of a markov chain of notes.

from collections import Counter, defaultdict, namedtuple
import random

class MarkovChain:

    def __init__(self):
        self.chain = defaultdict(Counter)
        self.sums = defaultdict(int)

    @staticmethod
    def create_from_dict(dict):
        m = MarkovChain()
        for from_note, to_notes in dict.items():
            for k, v in to_notes.items():
                m.add(from_note, k, v)
        return m

    def __str__(self):
        return str(self.get_chain())

    def add(self, from_note, to_note):
        self.chain[from_note][to_note] += 1
        self.sums[from_note] += 1

    def get_next(self, seed_note):
        if seed_note is None or str(seed_note) not in self.chain.keys():
            print ('Not in chain -> Random')
            print (self.chain.keys())
            random_chain = self.chain[random.choice(list(self.chain.keys()))]
            return random.choice(list(random_chain.keys()))
        else:
            if str(seed_note) in self.chain.keys():
                next_note_counter = random.randint(0, self.sums[seed_note])
                for note, frequency in self.chain[seed_note].items():
                    next_note_counter -= frequency
                    if next_note_counter <= 0:
                        return note

    def get_chain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def print_as_matrix(self, limit=10):
        columns = []
        for from_note, to_notes in self.chain.items():
            for note in to_notes:
                if note not in columns:
                    columns.append(note)
        _col = lambda string: '{:<8}'.format(string)
        _note = lambda note: '{}'.format(note)
        out = _col('')
        out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'
        for from_note, to_notes in self.chain.items():
            out += _col(from_note)
            for note in columns[:limit]:
                out += _col(to_notes[note])
            out += '\n'
        print(out)
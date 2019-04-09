# Python Generative Music

This code uses a set of instructions to build a markov chain in python and play it using FluidSynth Midi synthetiser. The instructions are generated from a MIDI file (.mid) and converted into json format using [ToneJS Midi](https://github.com/Tonejs/Midi). Then, they are fed into a simple [markov chain](https://en.wikipedia.org/wiki/Markov_chain) that generates midi phrases out of the ones from the original track, and playes them using [pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth).

In this example, [Aphex Twin - Aisatsana](https://www.youtube.com/watch?v=3_MRe3JwFc8) is used to generate the instructions in the markov chain. You can download the track's Midi File from the [MIDM database](http://www.midm-database.co.uk/syro.html).

## Setup

You need to have the [fluidsynth](http://www.fluidsynth.org) framework installed in order to route MIDI in your computer. In order to use this [pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth) library, you may install fluidsynth's version 1.1.x:

```
git clone https://github.com/FluidSynth/fluidsynth.git
cd fluidsynth
git checkout 1.1.x
mkdir build
cd build
cmake ..
sudo make install
```

Then, you are safe to install python bindings for it with pyfluidsynth. It is a good idea to test the different tests in [nwhitehead's pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth) and check that there is no actual error. Other more commonly used packages such as `numpy` are needed.

## Usage

The script is written in `python3`. You need to use an `SF2` file, in this case an acoustic Piano Soundfont (included in the Piano_SF) for the samples. You might need to change the midi driver in the `endlessplayer.py` file, according to your platform (in TODO-list to make it more flexible). In case of MAC:

```
self.fs.start(driver= "coreaudio", midi_driver="coremidi")
```

To start the player:

```
$ python endlessplayer.py instructions/instructions.json soundfont/SC55PianoV2.sf2
Parsing file: instructions/instructions.json
Title Aphex Twin - aisatsana
BPM 102
Generated markov chain. Playing.
Using SoundFont File Piano_SF/SC55PianoV2.sf2 
```
NB: some extra tweaks are done in the json output from the MIDI Converter. Some interesting Metadata is added, such as the duration of the phrases or `phraseLength`.

## Acknowledgment

[Alex Bainter](https://github.com/generative-music/pieces-alex-bainter), for inspiring with his work in [this post](https://medium.com/@metalex9/generating-more-of-my-favorite-aphex-twin-track-cde9b7ecda3a) and in [generative.fm](https://generative.fm/). His code is writen in JS and this repository is nothing more than a translation into Python using different libraries. All creative credits are his (except for Aphex Twin's composition, ofc).

[omgimanerd's markov-music repository](https://github.com/omgimanerd/markov-music), inspiring some of the functions for the Markov Chain creation.

[nwhitehead's pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth) implementation of python bindings for FluidSynth. The endlessplayer uses a sequencer from this library as well.
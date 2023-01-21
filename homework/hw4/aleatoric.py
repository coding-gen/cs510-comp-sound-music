#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

"""Let's make some music!"""

"""
author = Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
"""

"""
Reources:
Bart Massey's Tuner homework answer as an example of using sounddevice.
Mapping midi notes to frequencies: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
Python docs on argparse: https://docs.python.org/3/howto/argparse.html
Docs on sounddevice: https://python-sounddevice.readthedocs.io/en/0.4.4/
Sounddevice example: https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html#play-a-sine-signal
Vectorizing functions for np arrays: https://www.adamsmith.haus/python/answers/how-to-evaluate-a-function-on-every-element-of-a-numpy-array-in-python
numpy reference docs: https://numpy.org/doc/stable/reference/
Adjusted the try/except block based on: https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
"""

import wave, pyaudio, struct
import sys
import numpy as np
import math
import scipy.io.wavfile as wavfile
import argparse
import sounddevice as sd

from math import pi, sin

start_idx = 0

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def initialize():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])

    parser.add_argument("-r", "--root", 
        type=int, 
        default = 48,
        help="The MIDI key number as the root tone of the scale. (default: %(default)s)")
    parser.add_argument("-b", "--beats", 
        type=int, 
        default = 8,
        help="A time signature of beats per measure. (default: %(default)s)")
    parser.add_argument("-f", "--bpm", 
        type=float, 
        default = 90.0,
        help="The frequency of BPM beats per minute. (default: %(default)s)")
    parser.add_argument("-e", "--ramp", 
        type=float, 
        default = 0.5,
        help="The envelope's attack and release time as a fraction of the beat time. (default: %(default)s)")
    parser.add_argument("-a", "--accent", 
        type=float, 
        default = 5.0,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        help="Volume of the accent beat. (default: %(default)s)")
    parser.add_argument("-v", "--volume", 
        type=float, 
        default = 8.0,
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        help="Volume of the music. (default: %(default)s)")
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='output device (numeric ID or substring)')

    return parser.parse_args(remaining)


def makeEnvelope(ramp, frames):
    # I think the envelope needs to be applied outside of playNote
    # Or time needs to be controlled with the param time instead of the stream duration.
    rampingFrames = frames * ramp
    rampUp = np.arange(0 , 1, 1 / rampingFrames)
    rampDown = np.flip(rampUp)[:-1]
    ramped = np.ones(frames - int(2 * rampingFrames) + 1, dtype=int)
    envelope = np.append(np.append(rampUp, ramped), rampDown)
    envelope = envelope.reshape(-1, 1)

    # commenting it out for now, and moving to own method
    #t = t * envelope
    return

def sinFrames(element, f, amplitude):
    return 2 * np.pi * f * element


def playNote(args, frequency, amplitude, duration, square):

    try:
        samplerate = 48000
        def callback(outdata, frames, time, status):
            
            if status:
                print(status, file=sys.stderr)
            global start_idx
            t = (start_idx + np.arange(frames)) / samplerate
            t = t.reshape(-1, 1)
            f = frequency

            if square:
                outdata[:] = amplitude * 2 * (2*np.floor(f*t) - np.floor(2*f*t)) + 1

            else:
                sinFrames_vectorized = np.vectorize(sinFrames)
                outdata[:] = amplitude * np.sin(sinFrames_vectorized(t, frequency, amplitude))
            start_idx += frames

        with sd.OutputStream(device=args.device, channels=1, callback=callback,
                             samplerate=samplerate):
            sd.sleep(int(duration * 1000))
    except KeyboardInterrupt:
        print ('Fin.')
        sys.exit(0)
    except Exception as e:
        sys.exit(type(e).__name__ + ': ' + str(e))


def frequencyFromKey(keynumber):
    return 440 * 2**((keynumber - 69)/12)


if __name__ == "__main__":
    args = initialize()

    key_number = args.root
    # 60 is middle C
    # 69 is A above middle C
    # assuming equal tuning based on A4=a'=440 Hz

    frequency = frequencyFromKey(key_number)
    # Key 127 is    12543.85 Hz
    # Key 94 is     1864.66 Hz
    # Key 48 is     130.81 Hz
    # Key 20 is     25.96 Hz
    # Key 0 is      8.18 Hz

    # Amplitude
    """
    example:
    C[5] (key 72), square wave, A = 0.03162277660168379
    F[5] (key 77), sine wave, A = 0.251188643150958
    C[6] (key 84), sine wave, A = 0.251188643150958
    A[5] (key 81), sine wave, A = 0.251188643150958
    """
    amplitude = 10 ** (-6 * (10 - args.volume) / 20)
    rAmplitude = 10 ** (-6 * (10 - args.accent) / 20)

    # Calculate major scale
    # steps in scale: 0, +2, +2, +1, +2, +2, +2 (, +1)
    scale = [
        frequencyFromKey(key_number),
        frequencyFromKey(key_number + 2),
        frequencyFromKey(key_number + 4),
        frequencyFromKey(key_number + 5),
        frequencyFromKey(key_number + 7),
        frequencyFromKey(key_number + 9),
        frequencyFromKey(key_number + 11),
        frequencyFromKey(key_number + 12)
    ]

    # output the sound at the rate specified
    # 90 b/m = 3/2 b/s => duration in s/b = 2/3
    duration = 60 / args.bpm

    try:
        while True:
            playNote(args, frequency, rAmplitude, duration, True)
            for i in range(args.beats - 1):
                playNote(args, scale[np.random.randint(0, 7)], amplitude, duration, False)

    except KeyboardInterrupt:
        print ('Fin.')
        sys.exit(0)
    except Exception as e:
        sys.exit(type(e).__name__ + ': ' + str(e))


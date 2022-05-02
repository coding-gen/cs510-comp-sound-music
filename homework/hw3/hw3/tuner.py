#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

"""
author = Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
Homework3: Tuner
2 May 2022

Build an instrument tuner with two modes: report the frequency of a 48Ksps WAV file;
continuously report the frequency of a 48Ksps live input.
"""

"""
Sources:
I used this guide to determine the data format to use when reading and writing frames:
https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
It clued me in to needing the struct library:
https://docs.python.org/3/library/struct.html
I also used the wave library documentation: https://docs.python.org/3/library/wave.html
And examples from this pyaudio documentation: https://people.csail.mit.edu/hubert/pyaudio/

I used examples from the scipy docs: 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.triang.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fftfreq.html

How to apply the triangular window by convolving came from:
https://swharden.com/blog/2020-09-23-signal-filtering-in-python/

Read about applying a window here: 
https://download.ni.com/evaluation/pxi/Understanding%20FFTs%20and%20Windowing.pdf

Recording audio with pyaudio:
https://realpython.com/playing-and-recording-sound-python/#pyaudio_1
"""

import wave, pyaudio, struct
import sys
from math import pi, sin
from scipy.fft import fft, rfft, fftfreq
from scipy.signal.windows import triang
import numpy as np


# get magnitude of FFT, not phase, use abs() to get the magnitude of complex number
# ignore negative frequencies in the complex input fft for realtime input
# find the largest bin: numpy.argmax() 

# find max bin
# Find center frequency of the bin
# Locate function from bin number to frequency in the fft package
#   DC bin is the zero-frequency component
#   the remaining bins are equally spaced from frequency range: 0-nyquist limit (half the sampling rate)

# confirm frequency, with known value of sin wav


def get_trim(frameCount):
    # Trim the file to the first 2^17 samples (a few seconds) if it is longer than that. 
    # If it is shorter, trim to the largest possible power of 2.
    trimmedSampleCount = 2 # 2^1
    for i in range(16):
        if frameCount > trimmedSampleCount:
            trimmedSampleCount *= 2
    return trimmedSampleCount

def get_frequency(inputfile, live=False):
    data = []
    trimmedSampleCount = 0

    if not live: 
        obj = wave.open(inputfile,'rb')
        frameCount = obj.getnframes()
        CHUNK = 1024
        trimmedSampleCount = get_trim(frameCount)
        for i in range(trimmedSampleCount):
            dataChunk = obj.readframes(CHUNK)
            for datum in dataChunk:
                data.append(datum)
            # struct.unpack("<h", x)
        obj.close()
    else: 
        data = inputfile
        frameCount = 8192
        trimmedSampleCount = get_trim(frameCount)
        
    # Apply a triangular window to the samples. 
    # symmetrical: linear increase from 0 to 1 halfway, then linear decrease to 0 at the end
    # This makes the window sum half of the trimmedSampleCount
    window = triang(trimmedSampleCount, sym=True)

    # Simply multiply the window array with the signal array.
    # apply the window to the input signal with numpy
    for i in range(trimmedSampleCount):
        data[i] *= window[i]

    """
    # This is an option from swharden.com, not used currently

    # Normalize the window so the sum is 1, to preserve the amplitude of the input signal
    window = window / window.sum()
    print(f"window sum: {window.sum()}")
    """

    # Take the discrete fourier transform of the windowed samples
    # rfft for real signals
    # fft for digital signals
    if not live:
        transformed = fft(data)
    else:
        transformed = rfft(data)

    # Find the magnitude but discard the phase.
    transformedMag = [np.abs(x) for x in transformed]

    # Find the largest bin in the DFT.
    largestBin = np.argmax(transformedMag)

    # Report the center frequency of that bin.
    # a maximum precision of 1 decimal place
    freq = np.fft.fftfreq(trimmedSampleCount)
    print(f"Largest bin: {largestBin}, Center frequency: {freq}")


def get_live_frequency():
    #start taking samples from the live input. 
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 48000
    seconds = 3
    noteSamples = 8192

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
    
    frames = []
    i = 1
    while true:
        # For every 8192 samples call get_frequency()
        data = stream.read(chunk)
        frames.append(data)

        if i % noteSamples == 0:
            get_frequency(frames, True)
            frames = []
        i += 1

    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == "__main__":

    # Ignore noise
    # Account for harmonics

    if len(sys.argv) > 1: 
        inputfile = sys.argv[1]
        get_frequency(inputfile)
    else: 
        print("live")
        get_live_frequency()






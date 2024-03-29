#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3


from scipy import signal

from scipy.fft import fft, fftshift

import matplotlib.pyplot as plt
import numpy as np

window = signal.windows.triang(51)
for element in window:
    print(element)

plt.plot(window)

plt.title("Triangular window")

plt.ylabel("Amplitude")

plt.xlabel("Sample")

plt.figure()

A = fft(window, 2048) / (len(window)/2.0)

freq = np.linspace(-0.5, 0.5, len(A))

response = np.abs(fftshift(A / abs(A).max()))

response = 20 * np.log10(np.maximum(response, 1e-10))

plt.plot(freq, response)

plt.axis([-0.5, 0.5, -120, 0])

plt.title("Frequency response of the triangular window")

plt.ylabel("Normalized magnitude [dB]")

plt.xlabel("Normalized frequency [cycles per sample]")
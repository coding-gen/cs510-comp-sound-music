# Homework3: Tuner

author = Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
2 May 2022

# Purpose:
Build an instrument tuner with two modes: report the frequency of a 48Ksps WAV file;
continuously report the frequency of a 48Ksps live input.

# What I did

I did all the parts, and it runs. However, it is always wrong, saying the largest bin is 0.

# How it went

I had some difficulties determining exactly how to apply the triangle window. Some online googling was recommending doing a convolution or doing it as part of the FFT. I had a lot of type mismatches trying to apply that, before I re-read the assignment and saw it requires a simple multiplication. 

```
window type: <class 'numpy.ndarray'>
data type: <class 'numpy.ndarray'>
window type: <class 'numpy.float64'>
data type: <class 'numpy.bytes_'>
Traceback (most recent call last):
  File "/Users/gen/developer/psu/cs510-music/cs510-comp-sound-music/homework/hw3/./tuner.py", line 144, in <module>
    get_frequency(inputfile)
  File "/Users/gen/developer/psu/cs510-music/cs510-comp-sound-music/homework/hw3/./tuner.py", line 113, in get_frequency
    filtered = np.convolve(window, data, mode='valid')
  File "<__array_function__ internals>", line 5, in convolve
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/numpy/core/numeric.py", line 817, in convolve
    return multiarray.correlate(a, v[::-1], mode)
TypeError: Cannot cast array data from dtype('float64') to dtype('S32') according to the rule 'safe'


    data[i] *= window[i]
TypeError: can't multiply sequence by non-int of type 'numpy.float64''
```

# What is still to be done

It always outputs the same, wrong answer. I think maybe I need to look closer at how the FFT is binning, and line my window up with that.

```
Largest bin: 0, Center frequency: [ 0.00000000e+00  7.62939453e-06  1.52587891e-05 ... -2.28881836e-05
 -1.52587891e-05 -7.62939453e-06]

```

# Build-and-run instructions
Usage: 

python3 ./tuner.py filename.wav
python3 ./tuner.py


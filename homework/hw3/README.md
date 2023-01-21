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


I ran through all the steps, but I think there is something wrong with how I run the FFT, because the largest bin always ends up as the first one (0), whose Hz is 0. I double checked argmax behavior, and the first value of the fft result is indeed always the biggest one. I think maybe the window size is not meant to be as large as the whole sample? I have not been able to figure out how to modify the bin size in scipy fft. I think bin size needs to relate to window size.

Earlier, I had some difficulties determining exactly how to apply the triangle window. Some online googling was recommending doing a convolution or doing it as part of the FFT. I had a lot of type mismatches trying to apply that, before I re-read the assignment and saw it requires a simple multiplication. 

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

I'm also getting some input overflow when trying to run the live stream.

```
Traceback (most recent call last):
  File "/Users/gen/developer/psu/cs510-music/cs510-comp-sound-music/homework/hw3/./tuner.py", line 171, in <module>
    get_live_frequency()
  File "/Users/gen/developer/psu/cs510-music/cs510-comp-sound-music/homework/hw3/./tuner.py", line 154, in get_live_frequency
    data = stream.read(chunk)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/pyaudio.py", line 608, in read
    return pa.read_stream(self._stream, num_frames, exception_on_overflow)
OSError: [Errno -9981] Input overflowed
```
I had done some modifications to the code I got from the pyaudio docs, to not close the stream as often. Undoing those changes and modifying the block did not resolve this issue. This needs further investigation.


# Build-and-run instructions
Usage: 

python3 ./tuner.py filename.wav
python3 ./tuner.py


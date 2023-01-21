# Homework 4: Aleatoric

Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
27 May 2022

# Usage: 

```
$ ./aleatoric.py -h
usage: aleatoric.py [-h] [-l] [-r ROOT] [-b BEATS] [-f BPM] [-e RAMP] [-a {0,1,2,3,4,5,6,7,8,9,10}] [-v {0,1,2,3,4,5,6,7,8,9,10}] [-d DEVICE]

Let's make some music!

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-devices    show list of audio devices and exit
  -r ROOT, --root ROOT  The MIDI key number as the root tone of the scale. (default: 48)
  -b BEATS, --beats BEATS
                        A time signature of beats per measure. (default: 8)
  -f BPM, --bpm BPM     The frequency of BPM beats per minute. (default: 90.0)
  -e RAMP, --ramp RAMP  The envelope's attack and release time as a fraction of the beat time. (default: 0.5)
  -a {0,1,2,3,4,5,6,7,8,9,10}, --accent {0,1,2,3,4,5,6,7,8,9,10}
                        Volume of the accent beat. (default: 5.0)
  -v {0,1,2,3,4,5,6,7,8,9,10}, --volume {0,1,2,3,4,5,6,7,8,9,10}
                        Volume of the music. (default: 8.0)
  -d DEVICE, --device DEVICE
                        output device (numeric ID or substring)
```

## Select output device

```
$ ./aleatoric.py -l
> 0 MemSQL Headphones, Core Audio (1 in, 0 out)
< 1 MemSQL Headphones, Core Audio (0 in, 2 out)
  2 Built-in Microphone, Core Audio (2 in, 0 out)
  3 Built-in Output, Core Audio (0 in, 2 out)
  4 DisplayPort, Core Audio (0 in, 2 out)
  5 HDMI, Core Audio (0 in, 2 out)
  6 ZoomAudioDevice, Core Audio (2 in, 2 out)
```

# What I did

Note generation is complete. It is generating sin/square waves, at the designated beats per minute, beats per measure, in the major scale of the root, with the designated accent and volume. Additionally you can choose an output device. This was in the example code from sounddevice that I based my sound generator stream on, and I thought it was nifty so I kept it in.

# How it went

I have been learning numpy, since the example from sounddevice used it. I have had some trouble with it. For example on the envelope, I had a lot of trouble applying the envelope to the frames, since the frames are in an odd shape. In general I think I need to change how the time duration of each note is set. Currently I am setting the duration by how long the stream lasts, as per the sounddevice docs example. However there is also a 'time' param for the call back function. I think I could set it there instead, and will likely have to when I set the beats arg, and apply the envelope. I've noticed there are several frames that get executed, depending on the length of the stream. I want to be sure to apply the envelope to the entire stream, not to each frame. 

# What is still to be done

I am still working on the envelope. I haven't found how to apply it to the stream, instead of the frame. Additionally, there is a click at the start and stop of each note. This could potentially be helped with the envelop silencing the start and stop of the note. However it is likely because I have a separate stream for each note. I could re-engineer the way I send notes so they all use the same stream. I'm not sure quite how to do that, it may require switching to a blocking stream. I'll keep trying.
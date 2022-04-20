# Homework 1: Clipped

Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
6 April 2022

In this assignment, I became familiar with generating audio and playing it back. I used the recommended python libraries wave for writing and reading the soundfiles, and pyaudio for playing the audio through python itself. I also found struct useful for writing the data in the correct format for wave.

Specifically the purpose of this assignment is to demonstrate how audio clipping makes it sound louder, even though the amplitude is not actually higher. Essentially the peaks and troughs of the sine wave are cut off at half of their height. However the human ear compensates by completing the curve and interpreting the louder sound anyway. 

One change I made to this assignment is that I first play the unclipped sine wave, then play the clipped one. I found this useful for confirming the difference in amplitude myself. 

I had a bit of confusion when generating the frequency. I ended up doing some math about cycles per second and samples per second, to determine the iterator for sine. The result is slightly higher than 109 samples per cycle. Rather than rounding, I left it as a float. Additionally the frequency is not precise. Since the struct requires an int for the datapoint, I cast the float as an int. The ear is not able to tell the difference in a few rounded decimals, however it is worth noting. 

The largest issue I had was in the loop threshold. It is meant to have 48000 samples per second. However, if I set the loop to go from 0 to 48000 exactly, then it would produce no sound. I think there must be something about the sampling rate lining up poorly with the sine wave and cancelling it out. The most precise I could get and still produce a sound was 48050. This is worth more investigation. 

I confirmed the frequency is correct by ear. I found a 10 hour youtube video which plays 440 Hz and by listening, I compared it to how my tone's frequency sounds, and confirmed they sound the same. It would be worth implementing the professor's library wavfile to get a more precise confirmation.
# Homework 2: Resample

Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
20 April 2022

Usage: ./halfrate.py path/to/file.wav
expected to exist: ./hw-resample/coeffs.txt

In homework two, we learned to resample a sound file to fewer sps, specifically to half the rate of the input file. This involves filtering out the higher frequencies, then recording every other signal into a new file. 

It took me a while to parse through and understand the filter function, since sum notation was always hard for me and they didn't have descriptive variable names (a, X, n). In my code I refer to them as coefficients, signal, and len(coefficients) since that makes more sense to me. 

This generates the output file, but it does not sound right. It sounds very high and very quiet. Each file sounds different from each other and seems to have the same rhythm. So it is likely a problem with the frequency. I still need to figure out why, there must be an issue with the filter function. 

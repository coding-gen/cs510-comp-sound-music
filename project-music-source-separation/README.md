# Final Project

Genevieve LaLonde
CS510-Computers, Sound and Music
Spring term 2022
Portland State University 
Prof. Dr. Bart Massey
6 June 2022

# Informational links:

* Kong et al's paper: https://arxiv.org/pdf/2109.05418v1.pdf
* Kong et al's repo: https://github.com/bytedance/music_source_separation
* Kong et al's data MUSDB18 which they trained on: https://zenodo.org/record/1117372
* My gitlab repo: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation
* My separated musical vocals included at: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation/separated-vocals
* The audio dataset with background noise: WHAM!: http://wham.whisper.ai/
* My separated audio included at: https://gitlab.cecs.pdx.edu/music-source-separation/music-source-separation/separated_audio
* Performance evaluation: museval (Signal-to-Distortion Ratio SDR)
 * https://github.com/sigsep/sigsep-mus-eval
 * https://sigsep.github.io/sigsep-mus-eval/
 * https://museval.readthedocs.io/en/latest/

# Usage: 

To use the pretrained model, you can run Kong et al's bytesep as below:

```
$ python -m bytesep separate \
  --cpu  \
  --source_type="vocals" \
  --audio_path="../data/own/IFeelTheEarthMove.m4a" \
  --output_path="separated_results/test-output.mp3" 
Using cpu for separating ..
/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py:162: UserWarning: PySoundFile failed. Trying audioread instead.
  warnings.warn("PySoundFile failed. Trying audioread instead.")
Separate time: 746.715 s
```
As can be seen, it is necessary to use the --cpu param if your system does not have any GPU, disabling the default CUDA option. Additionally the default module PySoundFile fails, though I have not been able to find details as to why. The backup option audioread works though. 

# What I did

I set up the implementation and ran it over various types of music from my own library to determine any weaknesses. This required setting up the system a few times, since I kept hitting issues. See the end resulting setup instructions in sound_project_vm_setup.md. See my resulting separated vocals in the dirs: separated-vocals, jazz, ska, and acapella. For any particulary interesting effects, I noted the results in the commit message on the file. The separated_audio dir is empty, as I was not able to test on separating speech out from noisy backgrounds due to dataset issues, detailed below.

## Problems encountered in the setup

I will be documenting these issues below, and filing bug reports on the issues section of the original repo so future reproductions of the bytesep work can be accomplished more easily.

At first I had set up on Debian, but had better success on Ubuntu, since it is easier to install older versions of python on it manually using the dead snakes PPA as per the guide: https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/. The code repo states that newer versions of python can prevent installation of their bytesep tool. When doing the initial setup, I ran into a few issues. For example, the requirements.txt file has a typo. It was evidently copied from the setup.py file, and maintains the syntax on this line: `h5py==2.10.0',`. After that, it is recommended to download the checkpoints with bytesep itself, but there was a typo in the readme:

```
$ python -m bytesep download_checkpoints
usage: __main__.py [-h] {download-checkpoints,separate} ...
__main__.py: error: argument mode: invalid choice: 'download_checkpoints' (choose from 'download-checkpoints', 'separate')
```
Luckily upon close inspection I realized there was a dash instead of an underscore as from their own documentation and `python -m bytesep download-checkpoints` would work instead. Once it could run though, it failed on a missing system requirement for protobuf:

```
$ python -m bytesep download_checkpoints
Traceback (most recent call last):
... <redacted>
TypeError: Descriptors cannot not be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
If you cannot immediately regenerate your protos, some other possible workarounds are:
 1. Downgrade the protobuf package to 3.20.x or lower.
 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
```
After manually installing protobuf, the checkpoints were able to be downloaded. However the actual separation could not be run.

```
$ python -m bytesep separate  --cpu   --source_type="vocals"     --audio_path="../data/own/MyHero.mp3"     --output_path="separated_results/test-output.mp3" 
Using cpu for separating ..
/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py:162: UserWarning: PySoundFile failed. Trying audioread instead.
  warnings.warn("PySoundFile failed. Trying audioread instead.")
Traceback (most recent call last):
  File "/home/gen/venv/lib/python3.7/site-packages/librosa/core/audio.py", line 146, in load
    with sf.SoundFile(path) as sf_desc:
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 740, in __init__
    self._file = self._open(file, mode_int, closefd)
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 1265, in _open
    "Error opening {0!r}: ".format(self.name))
  File "/home/gen/venv/lib/python3.7/site-packages/soundfile.py", line 1455, in _error_check
    raise RuntimeError(prefix + _ffi.string(err_str).decode('utf-8', 'replace'))
RuntimeError: Error opening '../data/own/MyHero.mp3': File contains data in an unknown format.
```

While that error message in itself was not terribly helpful, it seemed to indicate some system incompatibility or missing library. I installed recommended libraries we had discussed early in class, and with some additional googling installed a few more system level things as well.

```
sudo apt-get install build-essential libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg python-dev

pip install audioread PySoundFile Wave sounddevice pyaudio

```

Pyaudio was actually very difficult to get installed. I ended up having to install it specifically outside of my python virtual environment, and it required me to first install the portaudio libraries `libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0` as it was failing on issing C header files before that, like:

```
      src/_portaudiomodule.c:28:10: fatal error: Python.h: No such file or directory
         28 | #include "Python.h"
            |          ^~~~~~~~~~
      compilation terminated.
      error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
      [end of output]

```

```
src/_portaudiomodule.c:29:10: fatal error: portaudio.h: No such file or directory
       29 | #include "portaudio.h"
          |          ^~~~~~~~~~~~~
    compilation terminated.
```

When converting some audio files, I made the mistake of uploading them from a MAC which added internal files like `'._05 Cry me a river.m4a'`. These prevented running bytesep on an entire directory, erroring on unknown format in string decoding. It took me a while to figure out the issue was caused by these internal files.

```
    raise RuntimeError(prefix + _ffi.string(err_str).decode('utf-8', 'replace'))
RuntimeError: Error opening '../data/own/jazz/._05 Cry me a river.m4a': File contains data in an unknown format.
```

It was after installing `ffmpeg` finally that the code was able to run. This had been mentioned in a github issues post as something that they tried because it was generally recommended, but had not worked for them: https://github.com/librosa/librosa/issues/1037 I tried it anyway just in case. 

I also had difficulty getting access to gitlab. I am more familiar with github and that is what is configured on my machine. Though I had set up API access tokens and SSH keys with gitlab at the start of the course, I could not clone the repository. I set up new ones, and was able to ssh with the rsa key like `git -i ~/path/to/rsa_id sgl@gitlab.cecs.pdx.edu/`. However I could not for the life of me figure out how to simply clone the repo, despite a thorough read through the GitLab SSH documentation (https://docs.gitlab.com/ee/user/ssh.html and https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html#clone-a-repository and https://docs.gitlab.com/ee/security/two_factor_authentication.html#2fa-for-git-over-ssh-operations etc.) and stackoverflow. In the end I realized I could upload files directly in the web app and did it that way instead. 


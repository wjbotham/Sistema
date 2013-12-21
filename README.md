Sistema
=======

Sistema requires pygame (http://www.pygame.org/download.shtml).  On Ubuntu, I used this guide: http://www.pygame.org/wiki/CompileUbuntu?parent=Compilation

If that has moved, these are the commands I ran:

```
#install dependencies
sudo apt-get install mercurial python3-dev python3-numpy ffmpeg \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
 
# Grab source
hg clone https://bitbucket.org/pygame/pygame
 
# Finally build and install
cd pygame
python3.2 setup.py build
sudo python3.2 setup.py install
```

To run unit tests, `python3.2 -m unittest`.

To run the dev loop, `python3.2 -m main`.

import pyglet
from goldminer import settings


if settings.music:
    song = pyglet.media.load("res/music/song1.mp3")
    looper = pyglet.media.SourceGroup(song.audio_format, None)
    looper.loop = True
    looper.queue(song)
    
    mediaplayer = pyglet.media.Player()
    mediaplayer.queue(looper)


def play():
    if settings.music:
        mediaplayer.play()
    
    
def stop():
    if settings.music:
        mediaplayer.pause()
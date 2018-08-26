import pyglet
from goldminer import assets

mediaplayer = None

def init():
    song = pyglet.media.load(assets.songs[0])
    looper = pyglet.media.SourceGroup(song.audio_format, None)
    looper.loop = True
    looper.queue(song)

    mediaplayer = pyglet.media.Player()
    mediaplayer.queue(looper)


def play():
    if not mediaplayer:
        init()

    mediaplayer.play()


def stop():
    if mediaplayer:
        mediaplayer.pause()
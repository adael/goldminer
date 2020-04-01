from random import randrange
from goldminer import assets, settings
from pygame import mixer

mixer.pre_init(44100, -16, 8, 512)
mixer.init()

# music
current_song = randrange(0, len(assets.songs) - 1)
playing = False

def play_music():
    global playing

    if not settings.music:
        return

    mixer.music.load(assets.songs[current_song])
    mixer.music.play()
    playing = True

def stop_music():
    global playing
    if not settings.music:
        return

    mixer.music.stop()
    playing = False

def next_music():
    global current_song
    if current_song + 1 < len(assets.songs):
        current_song += 1
    play_music()

# sounds
pick_axe = mixer.Sound(assets.wav_pickaxe)

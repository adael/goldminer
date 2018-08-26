import random
from goldminer import texts

class Sensible:
    def __init__(self):
        self.dead = False
        self.deaf = False
        self.mute = False
        self.blind = False
        self.confused = False

    def can_talk(self):
        return not self.mute

    def can_think(self):
        return not self.confused

    def can_ear(self):
        return not self.deaf

    def can_see(self):
        return not self.blind

    def says(self, text, probability=1.0):
        if self.can_talk():
            if random.random() <= probability:
                self.history.write_self(self, "say", text)
                self.world.actor_say(self, text)
        else:
            self.thinks(texts.im_muted)

    def thinks(self, text, probability=1.0):
        if self.can_think() and random.random() <= probability:
            self.history.write(text, self.color)

    def sees(self, text):
        if self.can_see():
            self.history.write_self(self, "see", text)

    def ears(self, text):
        if self.can_ear():
            self.history.write_self(self, "hear", text)

    def listens(self, text):
        if self.can_ear():
            self.history.write_self(self, "listen", text)

    def feels(self, feeling):
        self.history.write_self(self, "feel", feeling)

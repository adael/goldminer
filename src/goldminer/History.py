import random
from datetime import datetime


class History:
    def __init__(self):
        self.messages = []

    def insert(self, msg):
        self.messages.append((datetime.now(), msg))

    def write(self, msg, color):
        msg = random.choice(msg) if isinstance(msg, list) else msg
        txt = "[color={}]{}[/color]".format(color, msg)
        self.insert(txt)

    def write_self(self, actor, verb, msg, msg_color=None):
        if not msg_color:
            msg_color = actor.color
        self.write_ex("I", actor.color, verb, actor.color, msg, msg_color)

    def write_action(self, actor, verb, msg, msg_color="white"):
        self.write_ex(actor.name, actor.color, verb, actor.color, msg, msg_color)

    def write_ex(self, who, who_color, verb, verb_color, msg, msg_color):
        verb = random.choice(verb) if isinstance(verb, list) else verb
        msg = random.choice(msg) if isinstance(msg, list) else msg

        txt = "[color={}]{}[/color] ".format(who_color, who) + \
              "[color={}]{}[/color]: ".format(verb_color, verb) + \
              "[color={}]{}[/color]".format(msg_color, msg)

        self.insert(txt)

    def clear(self):
        self.messages.clear()

    def trim(self):
        del self.messages[:-100]

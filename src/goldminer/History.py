import random


class History:

    def __init__(self):
        self.messages = []

    def add(self, who, who_color, verb, verb_color, message, message_color):
        verb = random.choice(verb) if isinstance(verb, list) else verb
        message = random.choice(message) if isinstance(message, list) else message

        txt = "[color={}]{}[/color] ".format(who_color, who) + \
            "[color={}]{}[/color]:".format(verb_color, verb) + \
            "[color={}]{}[/color]".format(message_color, message)

        self.messages.append(txt)

    def add_self(self, actor, verb, message, message_color=None):
        if not message_color:
            message_color = actor.color
        self.add("I", actor.color, verb, actor.color, message, message_color )

    def add_action(self, actor, verb, message, message_color="white"):
        self.add(actor.name, actor.color, verb, actor.color, message, message_color)

    def clear(self):
        self.messages.clear()

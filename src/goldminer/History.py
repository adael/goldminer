import random


class History:

    def __init__(self):
        self.messages = []

    def add(self, text):
        self.messages.append(text)

    def add_action(self, who, verb, message):
        if isinstance(verb, list):
            verb = random.choice(verb)
        if isinstance(message, list):
            message = random.choice(message)
        self.add("[color={}]{} [color=green]{}[color=white]: {}".format(who.color, who.name, verb, message))

    def clear(self):
        self.messages.clear()

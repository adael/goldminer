import random

t_no_more_space = [
    "Not enough room for this",
    "I can carry nothing more",
    "No, my inventory it's full",
    "Heck, I need bigger bags"
]
t_im_thirsty = [
    "I think it's time to drink something",
    "I'm a bit dehydrated",
    "I'm gradually dying of thirst",
    "I'm gasping for a drink!",
    "Man I'm parched! Do you have any water?",
]
t_im_hungry = [
    "I am so hungry right now",
    "I've got a fast metabolism so I need to eat a lot and often!"
]


def no_more_space():
    return random.choice(t_no_more_space)


def im_thirsty():
    return random.choice(t_im_thirsty)

import pickle

filename = "goldminer.pkl"


def save_world(world):
    with open(filename, 'wb') as output:
        pickler = pickle.Pickler(output, -1)
        pickler.dump(world)


def load_world():
    with open(filename, 'r') as input:
        world = pickle.load(input)
    return world

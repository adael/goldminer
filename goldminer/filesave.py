import os
import pickle

filename = ".goldminer.pkl"


def save_world(world):
    with open(filename, 'wb') as fout:
        pickler = pickle.Pickler(fout, -1)
        pickler.dump(world)


def load_world():
    with open(filename, 'rb') as fin:
        return pickle.load(fin)


def can_load():
    return os.path.exists(filename)

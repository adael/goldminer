import os
from goldminer import game


if __name__ == "__main__":
    print("Initializing")
    print("Working directory: " + os.getcwd())
    game.start()

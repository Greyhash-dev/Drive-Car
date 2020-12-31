# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0

from menu import menu
try:
    import pygame
    import neat
    import graphviz
    import matplotlib.pyplot
    import numpy
    game = menu([720, 540], 30)
    game.entry()
except ModuleNotFoundError:
    print("Missing dependencies! Try running './install.sh'")

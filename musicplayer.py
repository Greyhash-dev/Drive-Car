# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0
import pygame
import threading
import time


def run():
    global stop_threads, playing
    while True:
        if stop_threads:
            break
        if playing == 0:
            time.sleep(0.5)
        else:
            pygame.mixer.music.stop()
            if playing == 1:
                pygame.mixer.music.load("./music/funny.mp3")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 2:
                pygame.mixer.music.load("./music/r1.mp3")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 3:
                pygame.mixer.music.load("./music/r2.mp3")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 4:
                pygame.mixer.music.load("./music/r3.mp3")
                pygame.mixer.music.play(-1, 0.0)
            playing = 0


class Player:
    def __init__(self):
        global playing, stop_threads
        stop_threads = False
        playing = 0
        pygame.init()
        self.t1 = threading.Thread(target=run, daemon=True)
        self.t1.start()

    def kill(self):
        global stop_threads
        stop_threads = True
        self.t1.join()

    def playm(self, num):
        global playing
        playing = num

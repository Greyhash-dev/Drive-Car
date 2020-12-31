# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0
import pygame
import threading
import time

# This is possibly the simplest and most hacked together Music player you have ever seen, but i just
# do not have the nerves right now to write a good music Player


# This is the thread that runs in the background
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
                pygame.mixer.music.load("./music/funny.wav")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 2:
                pygame.mixer.music.load("./music/r1.wav")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 3:
                pygame.mixer.music.load("./music/r2.wav")
                pygame.mixer.music.play(-1, 0.0)
            elif playing == 4:
                pygame.mixer.music.load("./music/r3.wav")
                pygame.mixer.music.play(-1, 0.0)
            playing = 0


# This is the class of the Player
class Player:
    def __init__(self):
        global playing, stop_threads
        pygame.mixer.pre_init(44100, 16, 2, 4096)   # Initialize the pygame music player
        stop_threads = False    # If this Value becomes True, the 'run' Thread will be terminated
        playing = 0     # If set to a value < 0 - it starts Playing (1 = Funny, 2 = russian...) if set to more than
        # there are songs, it simply stops playing
        pygame.init()   # Initialize pygame
        self.t1 = threading.Thread(target=run, daemon=True)     # Define the thread
        self.t1.start()     # Start the thread

    # This function simply kills the player
    def kill(self):
        global stop_threads
        stop_threads = True
        self.t1.join()

    # This function is used to select a music that should be played or stop the music
    def playm(self, num):
        global playing
        playing = num

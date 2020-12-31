# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0
import time
thr = 0.003


# This class calculates the speed of the Car based on the FPS, so that Lag spikes do not interfere with the
# acceleration
class gas:
    def __init__(self):
        self.lastgas = 0
        self.time = 0
        self.gas = 0
        self.time1 = 0
        self.time2 = time.time()*1000

    def call(self, gas, pos, fps):
        if gas != self.lastgas:
            self.time1 = time.time()*1000
            self.time2 = self.time
            self.lastgas = gas

        if gas == 1:
            if self.time < 1000:
                self.time = time.time()*1000 - self.time1 + self.time2
                if self.time > 1000:
                    self.time = 1000

        if gas == 0:
            if self.time > 0:
                self.time = self.time2 - (time.time()*1000 - self.time1)
                if self.time < 0:
                    self.time = 0
        if fps == 0:
            return 0
        else:
            return ((self.time/1000)**1.25*6) * (1/(fps/30))


# This Class calculates the rotation of the Cars based on the FPS, so that Lag spikes do not interfere with the
# rotation
class steering:
    def __init__(self, angle):
        self.originalangle = angle
        self.angle = angle

    def call(self, steer, fps):
        if fps == 0:
            return self.angle
        if steer != 0:
            if steer == 1:
                self.angle += 5 * (1/(fps/30))
                if self.angle == 360:
                    self.angle = 0
            elif steer == -1:
                self.angle -= 5 * (1 / (fps / 30))
                if self.angle == -1:
                    self.angle = 359
        return self.angle

    def reset(self):
        self.angle = self.originalangle

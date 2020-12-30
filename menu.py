# This File was written by Greyhash-dev (https://github.com/Greyhash-dev)
# This Program and every Files within it stand under the GNU Affero General Public License v3.0
import pygame
import os
import time
from gameenv import Game
from musicplayer import Player

pressed = False

def test():
    print("TODO")

class menuitem:
    def __init__(self, name, submenu, size, screensize, function, **kwargs):
        self.switch = kwargs.get('switch', False)
        self.switchstatus = kwargs.get('switchstatus', False)
        self.name = name
        self.font = pygame.font.SysFont("comicsansms", int(screensize[0] * 0.075 * size))
        self.color = kwargs.get('color', (0, 200, 100))
        self.object = self.font.render(self.name, True, self.color, (100, 100, 100))
        self.add = ""
        if self.switch:
            if self.switchstatus:
                self.add = " | ON"
            else:
                self.add = " | OFF"
        self.submenu = submenu
        self.function = function

    def getobject(self):
        return self.object

    def getsize(self):
        return self.object.get_size()

    def getstatus(self):
        if self.switch:
            return [True, self.switchstatus]
        else:
            return [False]

    def update(self, pos):
        global pressed
        if self.object.get_size()[1] >= pos[0] >= 0 and self.object.get_size()[0] >= pos[1] >= 0:
            self.color = (0, 200, 200)
            if pressed:
                if self.switch:
                    if self.switchstatus:
                        self.add = " | OFF"
                        self.switchstatus = False
                    else:
                        self.add = " | ON"
                        self.switchstatus = True
                else:
                    self.function()
                pressed = False
        else:
            self.color = (0, 200, 100)
        self.object = self.font.render(self.name + self.add, True, self.color, (100, 100, 100))


class menu:
    def __init__(self, screensize, actualfps):
        pygame.init()
        self.player = Player()
        self.screen = pygame.display.set_mode((screensize[0], screensize[1]))
        self.screensize = screensize
        self.actualfps = actualfps
        self.running = True
        self.clock = pygame.time.Clock()
        self.titlefont = pygame.font.Font(os.path.join("fonts", 'font.ttf'), int(screensize[0]*0.1))
        self.textfont = pygame.font.SysFont("comicsansms", int(screensize[0]*0.05))
        self.textcolor = [[0, 0, 128], 0]
        self.title = "Drive-Car!"
        self.recthight = int(self.screensize[1]/40)
        self.rectwidth = int(self.screensize[0]/(40*(screensize[0] / screensize[1])))
        self.rects = [
            [[0, 0], [self.screensize[0], self.recthight]],
            [[0, 0], [self.rectwidth, self.screensize[1]]],
            [[0, self.screensize[1]-self.recthight], [self.screensize[0], self.recthight]],
            [[self.screensize[0]-self.rectwidth, 0], [self.rectwidth, self.screensize[1]]]
        ]
        self.mainitems = [
            menuitem("Start Game without AI", 0, 1, self.screensize, lambda: self.game.spawnplayers(1, self.showlines)),
            menuitem("Start Game with AI", 0, 1, self.screensize, lambda: self.game.spawnplayerswithai(self.showlines)),
            menuitem("Settings", 0, 1, self.screensize, lambda: self.settingsscreen()),
            menuitem("Exit", 0, 1, self.screensize, lambda:self.stop())
        ]
        self.settingsitems = [
            menuitem("General Settings", 1, 1, self.screensize, lambda: self.generalsettingsscreen()),
            menuitem("AI-Settings", 1, 1, self.screensize, lambda: self.aisettingsscreen()),
            menuitem("Music", 1, 1, self.screensize, lambda:self.musicsettingsscreen()),
            menuitem("Back", 1, 1, self.screensize, lambda:self.exitsettings())
        ]
        self.gensettingsitems = [
            menuitem("Draw the 'Lasers' of the Car", 1, 1, self.screensize, test, switch=True),
            menuitem("Back", 1, 1, self.screensize, lambda: self.exitgensettings())
        ]
        self.musicitems = [
            menuitem("Funny Music", 1, 1, self.screensize, lambda:self.player.playm(1)),
            menuitem("Russian Hardbass", 1, 1, self.screensize, lambda:self.player.playm(2)),
            menuitem("More Russian Hardbass", 1, 1, self.screensize, lambda:self.player.playm(3)),
            menuitem("Even More Russian Hardbass", 1, 1, self.screensize, lambda:self.player.playm(4)),
            menuitem("OFF :(", 1, 1, self.screensize, lambda: self.player.playm(5)),
            menuitem("Back", 1, 1, self.screensize, lambda: self.exitmusicsettingsscreen())
        ]
        self.aiitems = [
            menuitem("To edit the AI Settings:", 1, 1, self.screensize, test),
            menuitem("Go to the working directory", 1, 1, self.screensize, test),
            menuitem("of this program and edit:", 1, 1, self.screensize, test),
            menuitem("'neat-config.txt'", 1, 1, self.screensize, test),
            menuitem("Back", 1, 1, self.screensize, lambda: self.exitaisettingsscreen())
        ]
        self.mousepos = pygame.mouse.get_pos()
        self.game = Game()
        self.settings = True
        self.gensettings = True
        self.musicsettings = True
        self.aisettings = True
        self.showlines = False

    def settingsscreen(self):
        global pressed
        pressed = False
        self.settings = True
        while self.settings:
            self.clock.tick(self.actualfps)
            self.redrawtitlescreen(title="Settings", rgb=(100, 0, 200))
            self.press()
            counter = 100
            for _ in self.settingsitems:
                _.update([self.mousepos[1] - counter, self.mousepos[0] - self.rectwidth])
                self.screen.blit(_.getobject(), (self.rectwidth, counter))
                counter += _.getsize()[1]
            pygame.display.flip()

    def generalsettingsscreen(self):
        global pressed
        pressed = False
        self.gensettings = True
        while self.gensettings:
            self.clock.tick(self.actualfps)
            self.redrawtitlescreen(title="Gen. Settings", rgb=(100, 0, 200))
            self.press()
            counter = 100
            for _ in self.gensettingsitems:
                _.update([self.mousepos[1] - counter, self.mousepos[0] - self.rectwidth])
                self.screen.blit(_.getobject(), (self.rectwidth, counter))
                counter += _.getsize()[1]
                if _.getstatus()[0]:
                    self.showlines = _.getstatus()
            pygame.display.flip()

    def musicsettingsscreen(self):
        global pressed
        pressed = False
        self.musicsettings = True
        while self.musicsettings:
            self.clock.tick(self.actualfps)
            self.redrawtitlescreen(title="Music", rgb=(100, 0, 200))
            self.press()
            counter = 100
            for _ in self.musicitems:
                _.update([self.mousepos[1] - counter, self.mousepos[0] - self.rectwidth])
                self.screen.blit(_.getobject(), (self.rectwidth, counter))
                counter += _.getsize()[1]
            pygame.display.flip()

    def aisettingsscreen(self):
        global pressed
        pressed = False
        self.aisettings = True
        while self.aisettings:
            self.clock.tick(self.actualfps)
            self.redrawtitlescreen(title="AI Settings", rgb=(100, 0, 200))
            self.press()
            counter = 100
            for _ in self.aiitems:
                if _ == self.aiitems[len(self.aiitems)-1]:
                    _.update([self.mousepos[1] - counter, self.mousepos[0] - self.rectwidth])
                else:
                    _.update([-10, -10])
                self.screen.blit(_.getobject(), (self.rectwidth, counter))
                counter += _.getsize()[1]
            pygame.display.flip()

    def redrawtitlescreen(self, **kwargs):
        self.screen.fill((100, 100, 100))
        title = kwargs.get('title', "Drive-Car!")
        destination = kwargs.get('destination', (self.rectwidth, self.recthight))
        rgb = kwargs.get('rgb', (0, 0, 128))
        for _ in self.rects:
            pygame.draw.rect(self.screen, pygame.Color(255, 10, 0), _)
        self.screen.blit(self.titlefont.render(title, True, rgb, (100, 100, 100)), destination)


    def entry(self, **kwargs):
        global pressed
        self.running = True
        jump = kwargs.get('jump', False)
        if not jump:
            position = 0
            tmpstr = ""
            for _ in list(self.title):
                char = self.titlefont.render(_, True, (0, 0, 128), (100, 100, 100))
                destination = (self.rectwidth+position, self.recthight)
                for x in range(0, self.screensize[0]-destination[0]-self.rectwidth-char.get_size()[0])[0::50]:
                    self.redrawtitlescreen(title=tmpstr)
                    x = (self.screensize[0]-destination[0]-self.rectwidth-char.get_size()[0]) - x
                    self.screen.blit(char, (int(destination[0]+x), int(destination[1]+(x/50)**2+10*(x/50))))
                    pygame.display.flip()
                    time.sleep(0.015)
                tmpstr += _
                position += char.get_size()[0]
                self.redrawtitlescreen(title=tmpstr)
                pygame.display.flip()
        while self.running:
            self.press()
            if self.textcolor[1] == 0:
                if self.textcolor[0][0] < 255:
                    self.textcolor[0][0] += 1
                elif self.textcolor[0][1] < 255:
                    self.textcolor[0][1] += 1
                elif self.textcolor[0][2] < 255:
                    self.textcolor[0][2] += 1
                else:
                    self.textcolor[1] = 1
            else:
                if self.textcolor[0][0] > 0:
                    self.textcolor[0][0] -= 1
                elif self.textcolor[0][1] > 0:
                    self.textcolor[0][1] -= 1
                elif self.textcolor[0][2] > 0:
                    self.textcolor[0][2] -= 1
                else:
                    self.textcolor[1] = 0
            self.clock.tick(self.actualfps)
            self.redrawtitlescreen(rgb=self.textcolor[0])
            text = self.textfont.render("By Greyhash-dev", True, (0, 0, 0), (100, 100, 100))
            self.screen.blit(text, (self.rectwidth, self.screensize[1]-self.recthight-text.get_size()[1]))
            counter = 100
            for _ in self.mainitems:
                _.update([self.mousepos[1]-counter, self.mousepos[0]-self.rectwidth])
                self.screen.blit(_.getobject(), (self.rectwidth, counter))
                counter += _.getsize()[1]
            pygame.display.flip()

    def stop(self):
        self.running = False
        self.player.kill()

    def exitsettings(self):
        self.settings = False

    def exitgensettings(self):
        self.gensettings = False

    def exitmusicsettingsscreen(self):
        self.musicsettings = False

    def exitaisettingsscreen(self):
        self.aisettings = False

    def setshowlines(self, x):
        self.showlines = x

    def press(self):
        global pressed
        for event in pygame.event.get():
            self.mousepos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  # If the little red X is pressed
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False

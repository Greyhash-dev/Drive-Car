import pygame
import math
from cars import car
import neat
import os
import _thread
import visualize


def picture(config, ge, bestplayer):
    global plot
    visualize.draw_net(config, ge[bestplayer.getid()], False)
    plot = pygame.image.load("net.png")
    t = plot.get_size()
    t = t[1] / t[0]
    plot = pygame.transform.scale(plot, (round(180 / t), 180))

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False


class Game:
    def __init__(self):
        # Some Initialize Stuff
        pygame.init()  # Initialize Pygame
        self.players = []  # In this Array will be stored all Objects once spawnplayers is executed
        logo = pygame.image.load("./graphics/logo32x32.png")  # Load in the Logo
        pygame.display.set_icon(logo)  # Set the Logo
        pygame.display.set_caption("drive car")  # Set Title
        self.screen_width = 720  # DO NOT CHANGE screen width
        self.screen_height = 540  # DO NOT CHANGE screen hight
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Set screen size
        self.screen.fill((100, 100, 100))  # Fill the screen with the rgb Value of (100, 100, 100)
        self.ai = False     # Becomes true if AI is active
        self.ge = []    # Here all the Genomes are stored
        self.nets = []  # Here all neural nets will be stored
        self.timer1 = 0
        self.timer2 = 0
        self.bestplayer = None
        self.lastbestplayer = None
        self.textfont = pygame.font.SysFont("comicsansms", 22)
        self.showlines = False
        # Displayed Things (If you Change the Fences, you MUST change the boarders!!):
        self.fences = ([0, 0, 20, 540],
                       [0, 0, 720, 20],
                       [700, 0, 20, 540],
                       [0, 520, 720, 20],
                       [80, 450, 540, 20],
                       [80, 250, 20, 200],
                       [80, 250, 200, 20],
                       [260, 170, 20, 100],
                       [260, 170, 350, 20],
                       [600, 170, 20, 300],
                       [20, 170, 160, 20],
                       [180, 70, 20, 120],
                       [180, 70, 520, 20])  # Pygame Rects
        self.boarders = [
            [[200, 90], [700, 90]],
            [[200, 90], [200, 190]],
            [[20, 190], [200, 190]],
            [[20, 190], [20, 520]],
            [[700, 520], [20, 520]],
            [[700, 520], [700, 90]],
            [[80, 470], [620, 470]],
            [[620, 170], [620, 470]],
            [[260, 170], [620, 170]],
            [[260, 170], [260, 250]],
            [[80, 250], [260, 250]],
            [[80, 250], [80, 470]]
        ]  # 2D Integer Array
        self.running = True  # Main game loop
        self.clock = pygame.time.Clock()  # Pygame clock
        self.fps = 0  # FPS of the Game
        self.actualfps = 30  # Set the FPS of the Game

    def updateScreen(self):  # Update the displayed Level
        self.screen.fill((100, 100, 100))  # Fill the screen with the rgb Value of (100, 100, 100)
        for fence in self.fences:  # Draw all Fences
            pygame.draw.rect(self.screen, pygame.Color(255, 100, 0), fence)

    def spawnplayers(self, count, showlines):
        self.players = []
        self.showlines = showlines
        for _ in range(0, count):  # Create all the Players
            self.players.append(car(_, self.boarders, self.showlines))  # Initialize the cars
        self.runGame(0, 0)  # Run the Game

    def spawnplayerswithai(self, showlines):   # This function starts the Game with AI
        self.showlines = showlines
        self.ai = True  # Set the AI Variable to True
        locale_dir = os.path.dirname(__file__)  # Read the current file Path
        config_path = os.path.join(locale_dir, "neat-config.txt")  # Where is the NEAT config file?
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)    # Just set evrything to default in neat
        p = neat.Population(config)     # Create Pupulation
        p.add_reporter(neat.StdOutReporter(True))  # Add Reporter
        stats = neat.StatisticsReporter()   # Create a config for this Reporter
        p.add_reporter(stats)   # Slap this config on the Reporter
        winner = p.run(self.runGame, 100000)     # Let's Go (Max 100000 Generations)

    def runGame(self, genomes, config):
        global plot
        if self.ai:
            ge = []     # If AI is Activated we want to create a Array witch will than house all the Genomes
            rag = 0     # Just a Counter
            self.nets = []
            for _, g in genomes:
                self.players.append(car(rag, self.boarders, self.showlines))    # Create a Car
                net = neat.nn.FeedForwardNetwork.create(g, config)  # Create a Network for this Car
                self.nets.append(net)   # Append the Neural Net to the Array
                g.fitness = 0   # Start with a Fitness of 0
                ge.append(g)    # Append the List of the Genomes
                rag += 1    # Count up
        gas = 0     # Initially Gas must be 0
        steer = 0   # Initially steer must be 0
        self.running = True     # Here we go!
        self.timer1 = 0
        if self.ai:
            for _ in self.players:  # Just doeing some Initializing of the Players (only nesercarry if AI is activated)
                _.update(0, 0, self.fps)
                self.updateScreen()
                self.screen.blit(_.getObject(), _.getOrigin())
                _.drawlines(_.getPosition(), _.getRotation(), self.screen)
            self.bestplayer = self.players[0]
            self.lastbestplayer = self.players[0]
            framecounter = 0
            visualize.draw_net(config, ge[self.bestplayer.getid()], False)
            plot = pygame.image.load("net.png")
            t = plot.get_size()
            t = t[1] / t[0]
            plot = pygame.transform.scale(plot, (round(180/t), 180))
        while self.running:
            if self.ai:
                framecounter += 1
            self.updateScreen()     # Update the Screen
            self.fps = self.clock.get_fps()  # Get current FPS
            self.clock.tick(self.actualfps)  # Set FPS
            for _ in self.players:
                if self.ai:
                    ge[_.getid()].fitness = _.getpoints()   # Set the Fitness of the Genomes
                    output = self.nets[_.getid()].activate(_.getintersections())    # Run the neural net
                    if self.ai:     # Decide what to do
                        if output[1] > 0:
                            gas = 1
                        else:
                            gas = 0
                        if output[0] > 0.5:
                            steer = 1
                        elif output[0] < -0.5:
                            steer = -1
                        else:
                            steer = 0
                _.update(gas, steer, self.fps)  # Update the Car with these movements
                self.screen.blit(_.getObject(), _.getOrigin())  # Display the Car
                _.drawlines(_.getPosition(), _.getRotation(), self.screen)  # Draw the Lines of each Car

                # -----------------------------------------------------
                # Check if car crashed into something and reset it than
                x, y = _.getPosition()
                try:
                    _.setpoints(_.getpoints() + 0.3 * (1/(self.fps/30)) * gas)
                except ZeroDivisionError:
                    print("[ERROR] The FPS was 0, this is normal during startup!")
                if self.ai:
                    if self.bestplayer.getpoints() < _.getpoints():
                        self.bestplayer = _
                x1 = round(x - 15 * math.sin((2 * math.pi * (_.getRotation()+35)) / 360))
                y1 = round(y - 15 * math.cos((2 * math.pi * (_.getRotation()+35)) / 360))
                x2 = round(x - 15 * math.sin((2 * math.pi * (_.getRotation() - 35)) / 360))
                y2 = round(y - 15 * math.cos((2 * math.pi * (_.getRotation() - 35)) / 360))
                if self.ai:
                    history = _.getgashistory()
                    elements = 0
                    if len(history) > 30:
                        for element in history:
                            elements += element
                        if (elements / len(history)) < 0.5:
                            try:
                                self.players.remove(_)
                            except ValueError:
                                print("[ERROR] Object not found that had to be deleted, this is normal if it "
                                      "happens a few times")
                for rect in self.fences:
                    if pointInRect((x1, y1), rect) or pointInRect((x2, y2), rect):
                        if self.ai:
                            try:
                                self.players.remove(_)
                            except ValueError:
                                print("[ERROR] Object not found that had to be deleted, this is normal if it "
                                      "happens a few times")
                        else:
                            _.respawn()
                # -----------------------------------------------------
            if len(self.players) == 0: # Stop the Game if everybody died
                self.running = False
            for event in pygame.event.get():  # Pygame Events
                if event.type == pygame.QUIT:   # If the little red X is pressed
                    self.running = False
                if event.type == pygame.KEYDOWN:    # If a key got Pressed
                    if not self.ai:
                        if event.key == pygame.K_w:
                            gas = 1
                        if event.key == pygame.K_d:
                            steer = -1
                        if event.key == pygame.K_a:
                            steer = 1
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.KEYUP:    # If a Key got released
                    if not self.ai:
                        if event.key == pygame.K_w:
                            gas = 0
                        if event.key == pygame.K_d:
                            if steer == -1:
                                steer = 0
                        elif event.key == pygame.K_a:
                            if steer == 1:
                                steer = 0
            if self.ai:
                try:
                    if framecounter > 3 * (1/(self.fps/30)):
                        framecounter = 0
                        if self.bestplayer != self.lastbestplayer:
                            self.lastbestplayer = self.bestplayer
                            _thread.start_new_thread(picture, (config, ge, self.bestplayer))
                except ZeroDivisionError:
                    print("[ERROR] The FPS was 0, this is normal during startup!")
                try:
                    self.screen.blit(plot, (100,270))
                except pygame.error:
                    print("[ERROR] Blit was changed when tried to display it, this is normal if it happens sometimes1")
                fps = self.textfont.render((str(round(self.fps))+"fps"), True, (0, 0, 128), (100, 100, 100))
                self.screen.blit(fps, (20, 20))
                points = self.textfont.render((str(round(self.bestplayer.getpoints())) + "Points"), True, (0, 0, 128),
                                              (100, 100, 100))
                self.screen.blit(points, (20, 20+fps.get_size()[1]))
            if not self.ai:
                points = self.textfont.render((str(round(self.players[0].getpoints())) + "Points"), True, (0, 0, 128), (100, 100, 100))
                self.screen.blit(points, (20, 20))
            pygame.display.flip()  # update the screen

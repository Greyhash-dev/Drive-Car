import pygame
import math
from cars import car
import neat
import os
import _thread
import visualize


# This function plots the best player's neural network in the middle of the screen
# config | neat.config.Config = The configuration of the network
# ge | genomes[] = All the Genomes in one Array
# bestplayer | car object = The best player, that gets plotted in the middle of the screen
def picture(config, ge, bestplayer):
    global plot
    visualize.draw_net(config, ge[bestplayer.getid()], False)
    plot = pygame.image.load("net.png")
    t = plot.get_size()
    t = t[1] / t[0]
    plot = pygame.transform.scale(plot, (round(180 / t), 180))
    plot.set_colorkey((255, 255, 255))


# This is the function that checks if a Point is in a given rect (to check if the Player hit a wall)
# point | [int, int] = [x, y] Given Point
# rect | [int, int, int, int] = [x, y, w, h] Given Rect
def pointInRect(point, rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False


def getlines(cubes):
    lines = []
    for _ in cubes:
        lines.append([[_[0], _[1]], [_[0] + _[2], _[1]]])
        lines.append([[_[0], _[1]], [_[0], _[1] + _[3]]])
        lines.append([[_[0] + _[2], _[1]], [_[0] + _[2], _[1] + _[3]]])
        lines.append([[_[0], _[1] + _[3]], [_[0] + _[2], _[1] + _[3]]])
    return lines


# The Game class
class Game:
    def __init__(self, screensize):
        # Some Initialize Stuff
        pygame.init()  # Initialize Pygame
        self.players = []  # In this Array will be stored all Objects once spawnplayers is executed
        logo = pygame.image.load("./graphics/logo32x32.png")  # Load in the Logo
        pygame.display.set_icon(logo)  # Set the Logo
        pygame.display.set_caption("drive car")  # Set Title
        self.screen_width = screensize[0]  # DO NOT CHANGE screen width
        self.screen_height = screensize[1]  # DO NOT CHANGE screen height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Set screen size
        self.screen.fill((100, 100, 100))  # Fill the screen with the rgb Value of (100, 100, 100)
        self.ai = False     # Becomes true if AI is active
        self.ge = []    # Here all the Genomes are stored
        self.nets = []  # Here all neural nets will be stored
        self.timer1 = 0     # Tis is a Variable used to check the movement of a Car in a given time and delete the ones
        # that do not move quickly
        self.timer2 = 0     # Tis is a Variable used to check the movement of a Car in a given time and delete the ones
        # that do not move quickly
        self.bestplayer = None  # In this Variable the best player gets stored (updated every Frame)
        self.lastbestplayer = None  # In this Variable the last best Player gets stored
        self.textfont = pygame.font.SysFont("comicsansms", 22)  # The Font for the Game
        self.showlines = False  # Variable if the 'Lasers' of the Cars get shown (DO NOT CHANGE THE DEFAULT HERE!)
        # Displayed Things (If you Change the Fences, you MUST change the boarders!!):
        self.fences = []
        self.boarders = []
        self.running = True  # Main game loop
        self.clock = pygame.time.Clock()  # Pygame clock
        self.fps = 0  # FPS of the Game
        self.actualfps = 30  # Set the FPS of the Game

    # This function just redraws the Map
    def updateScreen(self):  # Update the displayed Level
        self.screen.fill((100, 100, 100))  # Fill the screen with the rgb Value of (100, 100, 100)
        for fence in self.fences:  # Draw all Fences
            pygame.draw.rect(self.screen, (255, 0, 0), fence)

    # This function spawns in the Players (without AI!)
    def spawnplayers(self, count, showlines, fences):
        self.fences = fences
        self.boarders = getlines(self.fences)
        self.players = []
        self.showlines = showlines
        for _ in range(0, count):  # Create all the Players
            self.players.append(car(_, self.boarders, self.showlines))  # Initialize the cars
        self.runGame(0, 0)  # Run the Game

    # This function spawns in the Players with AI
    def spawnplayerswithai(self, showlines, fences):   # This function starts the Game with AI
        self.fences = fences
        self.boarders = getlines(self.fences)
        self.showlines = showlines  # Define if the 'Lasers' of the Cars should be displayed
        self.ai = True  # Set the AI Variable to True
        locale_dir = os.path.dirname(__file__)  # Read the current file Path
        config_path = os.path.join(locale_dir, "neat-config.txt")  # Where is the NEAT config file?
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)    # Just set everything to default in neat
        p = neat.Population(config)     # Create Population
        p.add_reporter(neat.StdOutReporter(True))  # Add Reporter
        stats = neat.StatisticsReporter()   # Set the Reporter
        p.add_reporter(stats)   # Slap this Reporter on the Population
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
        # Just setting some Variables (only necessary if ai is activated)
        if self.ai:
            for _ in self.players:
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
            plot.set_colorkey((255, 255, 255))
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
                # If ai:
                # Also check if Car is moving with a speed of 0.5 pixels per Frame, if not, kill the Car
                x, y = _.getPosition()
                try:
                    _.setpoints(_.getpoints() + 0.3 * (1/(self.fps/30)) * gas)
                except ZeroDivisionError:
                    print("[ERROR] FPS was 0, this is normal during startup!")
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
            # In this last Part of this spaghetti code, the neural net of the best Player gets drawn (if AI is active)
            # This is outsourced to another thread, because it is a quite big workload
            # Also the Net gets only updated every 0.1 second
            # Then the FPS and the points of the best players get displayed
            # Finally the screen gets updated
            if self.ai:
                try:
                    if framecounter > 3 * (1/(self.fps/30)):
                        framecounter = 0
                        if self.bestplayer != self.lastbestplayer:
                            self.lastbestplayer = self.bestplayer
                            _thread.start_new_thread(picture, (config, ge, self.bestplayer))
                except ZeroDivisionError:
                    print("[ERROR] FPS was 0, this is normal during startup!")
                try:
                    self.screen.blit(plot, (95,175))
                except pygame.error:
                    print("[ERROR] Blit was changed when tried to display it, this is normal if it happens sometimes1")
                fps = self.textfont.render((str(round(self.fps))+"fps"), True, (0, 0, 128), (100, 100, 100))
                fps.set_colorkey((100, 100, 100))
                self.screen.blit(fps, (0, 0))
                points = self.textfont.render((str(round(self.bestplayer.getpoints())) + "Points"), True, (0, 0, 128),
                                              (100, 100, 100))
                points.set_colorkey((100, 100, 100))
                self.screen.blit(points, (0, 0+fps.get_size()[1]))
            if not self.ai:
                points = self.textfont.render((str(round(self.players[0].getpoints())) + "Points"), True, (0, 0, 128),
                                              (100, 100, 100))
                points.set_colorkey((100, 100, 100))
                self.screen.blit(points, (0, 0))
            pygame.display.flip()  # update the screen

import pygame
import pickle as pkl


class editor:
    def __init__(self, screensize, actualfps):
        pygame.init()
        self.textfont = pygame.font.SysFont("comicsansms", int(screensize[0] * 0.04))
        self.screen = pygame.display.set_mode((screensize[0], screensize[1]))
        self.screensize = screensize
        self.actualfps = actualfps
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = "Drive-Car!"
        self.squaresize = 20
        self.squares = []
        self.horizontal = int(self.screensize[0] / self.squaresize)
        self.vertical = int(self.screensize[1] / self.squaresize)
        self.mousepos = pygame.mouse.get_pos()
        self.pressed = False
        self.drag = False
        self.fill = False
        self.clear = False
        self.rects = []
        self.car = pygame.image.load("./graphics/car.png")
        self.car.set_colorkey((0, 255, 0))
        try:
            with open('map.data', 'rb') as f:
                self.squares = pkl.load(f)
        except FileNotFoundError:
            for h in range(0, self.horizontal):
                x = []
                for v in range(0, self.vertical):
                    x.append([0, v * self.squaresize, h * self.squaresize])
                self.squares.append(x)
        # self.rects = self.export()

    def redraw(self):
        self.screen.fill((100, 100, 100))
        for _ in self.squares:
            for square in _:
                if square[0] == 1:
                    pygame.draw.rect(self.screen, (255, 0, 0), [square[2], square[1], self.squaresize,
                                                                self.squaresize])
        self.screen.blit(self.car, (50 - self.car.get_size()[0] / 2, 200 - self.car.get_size()[1] / 2))
        counter = 0
        if self.drag:
            text = self.textfont.render("Range Select", True, (0, 0, 0), (120, 100, 100))
            text.set_colorkey((120, 100, 100))
            self.screen.blit(text, [0, counter])
            counter += text.get_size()[1]
        if self.fill:
            text = self.textfont.render("Fill only", True, (0, 0, 0), (120, 100, 100))
            text.set_colorkey((120, 100, 100))
            self.screen.blit(text, [0, counter])
            counter += text.get_size()[1]
        if self.clear:
            text = self.textfont.render("Clear only", True, (0, 0, 0), (120, 100, 100))
            text.set_colorkey((120, 100, 100))
            self.screen.blit(text, [0, counter])
            counter += text.get_size()[1]
        for _ in range(0, self.horizontal):
            pygame.draw.line(self.screen, (255, 255, 255), (_ * self.squaresize, 0),
                             (_ * self.squaresize, self.screensize[1]))
        for _ in range(0, self.vertical):
            pygame.draw.line(self.screen, (255, 255, 255), (0, _ * self.squaresize),
                             (self.screensize[0], _ * self.squaresize))

    def run(self):
        lastpos = 0
        self.running = True
        while self.running:
            self.clock.tick(self.actualfps)
            self.press()
            if not self.pressed and not self.drag:
                lastpos = 0
            if self.pressed:
                if not self.drag:
                    pos = [int(self.mousepos[0] / self.squaresize), int(self.mousepos[1] / self.squaresize)]
                    if lastpos != pos:
                        self.manipulate(pos)
                        lastpos = pos
                if self.drag:
                    if lastpos == 0:
                        lastpos = [int(self.mousepos[0] / self.squaresize), int(self.mousepos[1] / self.squaresize)]
                    else:
                        pos = [int(self.mousepos[0] / self.squaresize), int(self.mousepos[1] / self.squaresize)]
                        if pos != lastpos:
                            self.pressed = False
                            pos = [(min(pos[0], lastpos[0]), min(pos[1], lastpos[1])),
                                   (max(pos[0], lastpos[0]), max(pos[1], lastpos[1]))]
                            lastpos = 0
                            for x in range(pos[0][0], pos[1][0]+1):
                                for y in range(pos[0][1], pos[1][1]+1):
                                    self.manipulate([x, y])

            self.redraw()
            pygame.display.flip()
        return self.rects

    def press(self):
        for event in pygame.event.get():
            self.mousepos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  # If the little red X is pressed
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
            elif event.type == pygame.KEYDOWN:  # If a key got Pressed
                if event.key == pygame.K_c:
                    self.squares = []
                    for h in range(0, self.horizontal):
                        x = []
                        for v in range(0, self.vertical):
                            x.append([0, v * self.squaresize, h * self.squaresize])
                        self.squares.append(x)
                elif event.key == pygame.K_r:
                    self.drag = not self.drag
                elif event.key == pygame.K_f:
                    self.fill = not self.fill
                    if self.fill and self.clear:
                        self.clear = 0
                elif event.key == pygame.K_d:
                    self.clear = not self.clear
                    if self.fill and self.clear:
                        self.fill = 0
                elif event.key == pygame.K_e:
                    self.rects = self.export()
                    if self.rects:
                        self.running = False
                        with open('map.data', 'wb') as f:
                            pkl.dump(self.squares, f)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    try:
                        with open('map.data', 'rb') as f:
                            self.squares = pkl.load(f)
                    except FileNotFoundError:
                        for h in range(0, self.horizontal):
                            x = []
                            for v in range(0, self.vertical):
                                x.append([0, v * self.squaresize, h * self.squaresize])
                            self.squares.append(x)

    def manipulate(self, pos):
        if self.clear:
            self.squares[pos[0]][pos[1]][0] = 0
        elif self.fill:
            self.squares[pos[0]][pos[1]][0] = 1
        else:
            self.squares[pos[0]][pos[1]][0] = not bool(self.squares[pos[0]][pos[1]][0])

    def export(self):
        horizontal = []
        for _ in self.squares:
            delete = []
            single = []
            add = []
            x = [i for i, e in enumerate([i[0] for i in _]) if e == 1]
            if len(x) != 0:
                for _ in range(0, len(x)):
                    try:
                        if x[_] == x[_-1] + 1 == x[_+1] - 1:
                            delete.append(x[_])
                        if x[_-1] + 1 != x[_] and x[_] != x[_+1] - 1:
                            single.append(x[_])
                    except IndexError:
                        if _ == 0 and len(x) != 1:
                            if x[_] != x[_+1] - 1:
                                single.append(x[_])
                        elif len(x) == 1:
                            single.append(x[_])
                        else:
                            if x[_] != x[_-1] + 1:
                                single.append(x[_])
                for _ in delete:
                    x.remove(_)
                for _ in single:
                    x.remove(_)
                counter = 0
                while 1:
                    try:
                        add.append([x[counter], x[counter+1]])
                        counter += 2
                    except IndexError:
                        break
                for _ in single:
                    add.append([_, _])
                horizontal.append(add)
            else:
                horizontal.append([])
        merge = []
        exclude = []
        for _ in range(0, len(horizontal)-1):
            for idx in range(0, len(horizontal[_])):
                if horizontal[_][idx] in horizontal[_+1] and horizontal[_][idx] != [] \
                        and [_, idx] not in exclude:
                    counter = 0
                    while 1:
                        try:
                            if not horizontal[_][idx] in horizontal[_+counter]:
                                break
                            exclude.append([_+counter, horizontal[_+counter].index(horizontal[_][idx])])
                            counter += 1
                        except IndexError:
                            break
                    merge.append([_, counter, horizontal[_][idx], idx])
        for delete in merge:
            for _ in range(0, delete[1]):
                try:
                    horizontal[delete[0]+_].remove(delete[2])
                except ValueError:
                    horizontal[delete[0]+_].remove(delete[2])
        rects = []
        for _ in range(0, len(horizontal)):
            for x in horizontal[_]:
                rects.append([_ * self.squaresize, x[0] * self.squaresize, 1 * self.squaresize,
                              (x[1] - x[0]+1) * self.squaresize])
        for _ in merge:
            rects.append([_[0] * self.squaresize, _[2][0] * self.squaresize, _[1] * self.squaresize,
                          (_[2][1] - _[2][0]+1) * self.squaresize])
        return rects

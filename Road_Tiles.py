import pygame

colors = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255), 'GREEN': (0, 255, 0), 'RED': (255, 0, 0),
          'GREY': (116, 111, 110), 'ORANGE': (231, 95, 67), 'YELLOW': (255, 247, 0)}


class Block_Wall:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        return


class Straight_Horizontally:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        pygame.draw.rect(screen,
                         colors['GREY'],
                         [self.position[1],
                          self.position[0] + 0.15 * self.tile_len,
                          self.tile_len,
                          self.tile_len * 0.7])
        pygame.draw.line(screen, colors['RED'], (self.position[1], self.position[0] + 0.5 * self.tile_len),
                         (self.position[1] + self.tile_len, self.position[0] + 0.5 * self.tile_len))


class Straight_Vertically:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        pygame.draw.rect(screen,
                         colors['GREY'],
                         [self.position[1] + 0.15 * self.tile_len,
                          self.position[0],
                          self.tile_len * 0.7,
                          self.tile_len])
        pygame.draw.line(screen, colors['RED'], (self.position[1] + 0.5 * self.tile_len, self.position[0]),
                         (self.position[1] + self.tile_len * 0.5, self.position[0] + self.tile_len))


# ------------------------------------------------------------------------------------------------------------------------
class Turn_Right_Down:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []
        points.append((self.position[1] + 0.35 * self.tile_len, self.position[0] + 0.15 * self.tile_len))
        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0] + 0.35 * self.tile_len))

        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0] + self.tile_len))
        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0] + self.tile_len))

        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.85))
        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.15))

        pygame.draw.polygon(screen, colors['GREY'], points)


class Turn_Left_Down:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []

        points.append((self.position[1], self.position[0] + self.tile_len * 0.15))
        points.append((self.position[1], self.position[0] + self.tile_len * 0.85))

        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0] + self.tile_len))
        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0] + self.tile_len))

        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0] + 0.35 * self.tile_len))
        points.append((self.position[1] + 0.65 * self.tile_len, self.position[0] + 0.15 * self.tile_len))

        pygame.draw.polygon(screen, colors['GREY'], points)


class Turn_Right_Up:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []

        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0]))
        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0]))

        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.15))
        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.85))

        points.append((self.position[1] + 0.35 * self.tile_len, self.position[0] + 0.85 * self.tile_len))
        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0] + 0.65 * self.tile_len))

        pygame.draw.polygon(screen, colors['GREY'], points)


class Turn_Left_Up:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []

        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0]))
        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0]))

        points.append((self.position[1], self.position[0] + self.tile_len * 0.15))
        points.append((self.position[1], self.position[0] + self.tile_len * 0.85))

        points.append((self.position[1] + 0.65 * self.tile_len, self.position[0] + 0.85 * self.tile_len))
        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0] + 0.65 * self.tile_len))

        pygame.draw.polygon(screen, colors['GREY'], points)


# ------------------------------------------------------------------------------------------------------------------------

class T_down:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []
        points.append((self.position[1], self.position[0] + 0.15 * self.tile_len))
        points.append((self.position[1], self.position[0] + 0.85 * self.tile_len))

        points.append((self.position[1] + 0.15 * self.tile_len, self.position[0] + self.tile_len))
        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0] + self.tile_len))

        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.85))
        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.15))

        pygame.draw.polygon(screen, colors['GREY'], points)


class T_up:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []
        points.append((self.position[1], self.position[0] + 0.15 * self.tile_len))
        points.append((self.position[1], self.position[0] + 0.85 * self.tile_len))

        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.85))
        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.15))

        points.append((self.position[1] + 0.85 * self.tile_len, self.position[0]))
        points.append((self.position[1] + 0.12 * self.tile_len, self.position[0]))

        pygame.draw.polygon(screen, colors['GREY'], points)


# ------------------------------------------------------------------------------------------------------------------------
class X_crossroads:
    def __init__(self, position, tile_len):
        self.position = position
        self.tile_len = tile_len

    def draw(self, screen):
        points = []
        points.append((self.position[1], self.position[0] + 0.25 * self.tile_len))
        points.append((self.position[1], self.position[0] + 0.75 * self.tile_len))

        points.append((self.position[1] + 0.25 * self.tile_len, self.position[0] + self.tile_len))
        points.append((self.position[1] + 0.75 * self.tile_len, self.position[0] + self.tile_len))

        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.75))
        points.append((self.position[1] + self.tile_len, self.position[0] + self.tile_len * 0.25))

        points.append((self.position[1] + self.tile_len * 0.75, self.position[0]))
        points.append((self.position[1] + self.tile_len * 0.25, self.position[0]))

        pygame.draw.polygon(screen, colors['GREY'], points)

# ------------------------------------------------------------------------------------------------------------------------

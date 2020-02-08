import pygame
import numpy as np
from car import *


class Animation:

    def __init__(self, map, window_scale, objects):
        pygame.init()
        self.objects = objects
        self.map = map
        self.window_scale = window_scale
        self.window_size = [window_scale * self.map.width, window_scale * self.map.height]
        self.screen = pygame.display.set_mode(self.window_size)

        pygame.display.set_caption("TMP NAME")

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.colors = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255), 'GREEN': (0, 255, 0), 'RED': (255, 0, 0),
                       'GREY': (116, 111, 110), 'ORANGE': (231, 95, 67), 'YELLOW': (255, 247, 0)}

    def end(self):
        pygame.quit()

    def draw_map(self):
        for row in range(1, self.map.height + 1):
            for column in range(1, self.map.height + 1):
                color = self.map.map[row][column].get_color()
                pygame.draw.rect(self.screen,
                                 color,
                                 [(self.window_scale) * (column - 1),
                                  (self.window_scale) * (row - 1),
                                  self.window_scale,
                                  self.window_scale])

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end()
                    return False
                elif event.key == pygame.K_DOWN:
                    self.objects[0].go_down()
                elif event.key == pygame.K_UP:
                    self.objects[0].go_up()
                elif event.key == pygame.K_RIGHT:
                    self.objects[0].go_right()
                elif event.key == pygame.K_LEFT:
                    self.objects[0].go_left()

            elif event.type == pygame.QUIT:
                self.end()
                return False

        self.draw_map()
        pygame.display.flip()
        return True

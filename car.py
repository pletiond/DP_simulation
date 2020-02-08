from map import *
import numpy as np


class Car:

    def __init__(self, start_location, map):
        self.x = start_location[1]
        self.y = start_location[0]
        self.map = map
        self.map.map[self.y][self.x] = self
        self.current_task = None
        # self.id = int(np.nanmax(self.map.map)) + 1
        self.id = 8

    def go_up(self):
        if self.map.map[self.y - 1][self.x].is_empty(self):
            self.map.map[self.y - 1][self.x] = self
            self.map.map[self.y][self.x] = Route()
            self.y -= 1
            return True
        return False

    def go_down(self):
        if self.map.map[self.y + 1][self.x].is_empty(self):
            self.map.map[self.y + 1][self.x] = self
            self.map.map[self.y][self.x] = Route()
            self.y += 1
            return True
        return False

    def go_right(self):
        if self.map.map[self.y][self.x + 1].is_empty(self):
            self.map.map[self.y][self.x + 1] = self
            self.map.map[self.y][self.x] = Route()
            self.x += 1
            return True
        return False

    def go_left(self):
        if self.map.map[self.y][self.x - 1].is_empty(self):
            self.map.map[self.y][self.x - 1] = self
            self.map.map[self.y][self.x] = Route()
            self.x -= 1
            return True
        return False

    def get_color(self):
        if self.current_task is None:
            return (255, 247, 0)  # YELLOW
        else:
            return (0, 188, 255)  # ORANGE

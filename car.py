from map import *
import numpy as np


class Car:

    def __init__(self, start_location, map):
        self.x = start_location[1]
        self.y = start_location[0]
        self.map = map
        self.map.map[self.y][self.x] = self
        self.possible_task = None
        self.current_task = None
        self.id = self.map.car_id_max
        self.map.car_id_max += 1


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

    def is_empty(self, car=None):
        return False

    def is_agent(self):
        return True

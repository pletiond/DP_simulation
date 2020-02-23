import numpy as np


class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []
        self.task_id_max = 1
        self.car_id_max = 10
        for i in range(height + 2):
            self.map.append([])
            for j in range(width + 2):
                self.map[i].append(None)
                if i == 0 or j == 0 or i == height + 1 or j == width + 1:
                    self.map[i][j] = None
                else:
                    self.map[i][j] = Wall()

    def add_route(self, start, end):
        if start[0] == end[0]:
            start_point = start[1]
            end_point = end[1]
            level = start[0]

            for i in range(min(start_point, end_point), max(start_point, end_point) + 1):
                if self.map[level][i] is None:
                    continue
                self.map[level][i] = Route()

        elif start[1] == end[1]:
            start_point = start[0]
            end_point = end[0]
            level = start[1]

            for i in range(min(start_point, end_point), max(start_point, end_point) + 1):
                if self.map[i][level] is None:
                    continue
                self.map[i][level] = Route()

    def print(self):
        print(self.map)

    def to_bitman(self):
        out = np.ones((self.height + 2, self.width + 2))
        for i in range(self.height + 1):
            for j in range(self.width + 2):
                if not self.map[i][j] is None and self.map[i][j].is_empty():
                    out[i][j] = 0
        return out

    def to_bitman_objects(self):
        out = np.ones((self.height + 2, self.width + 2), dtype=np.int32)
        for i in range(self.height + 1):
            for j in range(self.width + 2):
                if not self.map[i][j] is None and (self.map[i][j].is_empty() or self.map[i][j].is_agent()):
                    out[i][j] = 0
        return out

    def print_map(self, map):
        for i in range(len(map)):
            if i == 0 or i == len(map) - 1:
                continue
            for j in range(len(map[i])):
                if j == 0 or i == len(map[i]) - 1:
                    continue
                if map[i][j] == 0:
                    print('--', end=' ')
                elif map[i][j] == 1:
                    print('XX', end=' ')
                else:
                    print("{:02d}".format(map[i][j]), end=' ')

            print('\n')

class Wall:
    def __str__(self):
        return '-'

    def get_color(self):
        return (116, 111, 110)  # Grey

    def is_empty(self, car=None):
        return False

    def is_agent(self):
        return False


class Route:

    def get_color(self):
        return (255, 255, 255)  # write

    def is_empty(self, car=None):
        return True

    def is_agent(self):
        return False

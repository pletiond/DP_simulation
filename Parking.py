import numpy as np


class Dummy_Parking:

    def __init__(self, car_points):
        self.car_points = car_points

    def where_to_park(self, loc):
        min_len = None
        best_loc = None
        for cp in self.car_points:
            # print(f'CP: {cp.location} has score: {cp.score}')
            if best_loc is None or self.heuristic(loc, cp.location) < min_len:
                min_len = self.heuristic(loc, cp.location)
                best_loc = cp.location
        return best_loc

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def add_location(self, loc):
        for i, cp in enumerate(self.car_points):
            len = int(self.heuristic(loc, cp.location))
            diff = len ** (-1)
            self.car_points[i].score += diff


class Probabilistic_Parking:

    def __init__(self, car_points):
        self.car_points = car_points
        self.records = 0

    def where_to_park(self, loc):
        print('\n----')
        print(f'In LOC: {loc}')
        min_len = None
        best_loc = None
        for cp in self.car_points:
            # print(f'CP: {cp.location} has score: {cp.score}')
            if best_loc is None or self.heuristic(loc, cp.location) < min_len:
                min_len = self.heuristic(loc, cp.location)
                best_loc = cp.location
                if min_len == 0:
                    return cp.location

        best_loc2 = None
        best_score = None
        print(f'Best1: {best_loc}')
        for cp in self.car_points:
            print(f'CP: {cp.location} has score: {cp.score}')
            score = (cp.score * 2) / self.heuristic(loc, cp.location)
            print(score)
            if best_loc2 is None or best_score < score:
                best_score = score
                best_loc2 = cp.location

        if self.records < 20:
            return best_loc

        if best_loc == best_loc2:
            print('Same')
            # input('...')
            return best_loc
        else:
            print(best_loc)
            print(best_loc2)
            print(best_score)
            # input('ok?')
            return best_loc2

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def add_location(self, loc):
        self.records += 1
        for i, cp in enumerate(self.car_points):
            len = int(self.heuristic(loc, cp.location))
            diff = (len ** (-2)) * 100
            self.car_points[i].score += diff

import random
import csv

class Task:

    def __init__(self, start, end, map):
        self.map = map
        self.task_id = self.map.task_id_max
        self.map.task_id_max += 1
        self.start = start
        self.end = end
        self.state = 'NEW'
        self.car = None
        # self.map.map[self.start[0]][self.start[1]] = Task_Point()
        # self.map.map[self.end[0]][self.end[1]] = Task_Point()

    def activate(self):
        # self.map.map[self.start[0]][self.start[1]] = Task_Start(self.task_id, self)
        # self.map.map[self.end[0]][self.end[1]] = Task_End(self.task_id, self)
        self.state = 'ACTIVATED'
        self.car = None

    def assign(self, car):
        self.state = 'ASSIGNED'
        self.car = car

    def complete(self):
        self.state = 'COMPLETED'

    def __str__(self):
        return f'TID: {self.task_id} From: {self.start} To: {self.end}'

    def __repr__(self):
        return self.__str__()


class Task_Start:
    def __init__(self, task_id, parent):
        self.task_id = task_id
        self.parent = parent

    def get_color(self):
        return (0, 255, 0)  # green

    def is_empty(self, car=None):
        if car is None:
            return True
        if car.current_task is None:
            print("ASSIGN--------")
            car.current_task = self.parent
            self.parent.assign(car)
            car.turn_round()
            return True
        else:
            return False

    def is_agent(self):
        return False


class Task_End:
    def __init__(self, task_id, parent):
        self.task_id = task_id
        self.parent = parent

    def get_color(self):
        return (255, 0, 0)  # red

    def is_empty(self, car=None):
        if car is None:
            return True
        if car.current_task.task_id == self.task_id:
            car.current_task = None
            car.possible_task = None
            car.turn_round()
            self.parent.complete()
            return True
        else:
            return False

    def is_agent(self):
        return False


class Task_Point:
    def get_color(self):
        return (211, 211, 211)

    def is_empty(self, car=None):
        return True

    def is_agent(self):
        return False


class Spawn_Points:

    def __init__(self, tasks, map, cars, max_cars):
        self.tasks = tasks
        self.map = map
        self.cars = cars
        self.points = []
        self.max_cars = max_cars
        bitmap = map.to_bitman()
        for row in range(len(bitmap)):
            for col in range(len(bitmap[row])):
                if bitmap[row][col] == 0 and not self.is_on_crossroads(bitmap, (row, col)):
                    self.add_spawn_point((row, col), 1, '')
        print(f'Total spawn points: {len(self.points)}')

    def add_spawn_point(self, location, spawn_rate, orientation):
        self.points.append((location, spawn_rate, orientation))
        # self.map.map[location[0]][location[1]] = Task_Point()

    def create_task(self, time):
        start, end = self.get_random_free_points()
        if start == False:
            return
        with open(f'tests/tasks01_a{self.max_cars}_t{self.max_cars}_central.csv', 'a') as fp:
            fp.write(f'{start};{end};{int(time)}\n')
        new_task = Task(start, end, self.map)
        new_task.activate()
        self.tasks.append(new_task)

    def get_random_free_points(self):
        free = []
        for point in self.points:
            skip = False
            for t in self.tasks:
                if t.start == point[0] or t.end == point[0]:
                    skip = True
                    break

            if skip:
                continue
            free.append(point)
        if len(free) < 2:
            return False, False

        start = random.choice(free)
        free.remove(start)
        end = random.choice(free)

        return start[0], end[0]

    def refresh_spawn_points(self):
        for point in self.points:
            point_loc = point[0]
            if self.map.map[point_loc[0]][point_loc[1]].__class__.__name__ == 'Route':
                self.map.map[point_loc[0]][point_loc[1]] = Task_Point()


    def is_on_crossroads(self, bitman, node_position):
        count = 0
        if node_position[0] > 0 and bitman[node_position[0] - 1][node_position[1]] == 0:
            count += 1
        if node_position[1] > 0 and bitman[node_position[0]][node_position[1] - 1] == 0:
            count += 1
        if node_position[0] < len(bitman) and bitman[node_position[0] + 1][node_position[1]] == 0:
            count += 1
        if node_position[1] < len(bitman[0]) and bitman[node_position[0]][node_position[1] + 1] == 0:
            count += 1
        if count > 2:
            return True
        else:
            return False

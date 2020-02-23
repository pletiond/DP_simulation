import heapq
import numpy as np


class SingleCarController():

    def __init__(self, car, map, tasks):
        self.map = map
        self.car = car
        self.tasks = tasks
        self.route = None

    def plan_route(self):
        # self.route = self.astar(start, end)[1:]
        if self.car.current_task is None:
            self.get_next_task()
        elif self.car.current_task.state == 'ASSIGNED':
            self.plan_delivery()

    def get_next_task(self):
        maze = self.map.to_bitman()

        next_task = None
        shortest_dis = None
        new_route = None
        for i in range(len(self.tasks)):

            if not self.tasks[i].state == 'ACTIVATED':
                continue
            route = self.astar(maze, (self.car.y, self.car.x), self.tasks[i].start)[::-1]
            distance = len(route)

            if next_task is None or shortest_dis > distance:
                next_task = self.tasks[i]
                shortest_dis = distance
                new_route = route

        print(f'Shortest task: {next_task.task_id}')
        self.route = new_route

    def plan_delivery(self):
        maze = self.map.to_bitman()
        route = self.astar(maze, (self.car.y, self.car.x), self.car.current_task.end)[::-1]
        self.route = route
        return

    def do_step(self):
        if self.route is None:
            self.plan_route()
        if len(self.route) == 0:
            self.route = None
            return
        next = self.route.pop(0)
        if self.car.x == next[1]:
            if self.car.y == next[0] + 1:
                self.car.go_up()
            elif self.car.y == next[0] - 1:
                self.car.go_down()
        elif self.car.y == next[0]:
            if self.car.x == next[1] + 1:
                self.car.go_left()
            elif self.car.x == next[1] - 1:
                self.car.go_right()

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, array, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # , (1, 1), (1, -1), (-1, 1), (-1, -1)

        close_set = set()

        came_from = {}

        gscore = {start: 0}

        fscore = {start: self.heuristic(start, goal)}

        oheap = []

        heapq.heappush(oheap, (fscore[start], start))

        while oheap:

            current = heapq.heappop(oheap)[1]

            if current == goal:

                data = []

                while current in came_from:
                    data.append(current)

                    current = came_from[current]

                return data

            close_set.add(current)

            for i, j in neighbors:

                neighbor = current[0] + i, current[1] + j

                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)

                if 0 <= neighbor[0] < array.shape[0]:

                    if 0 <= neighbor[1] < array.shape[1]:

                        if array[neighbor[0]][neighbor[1]] == 1:
                            continue

                    else:

                        # array bound y walls

                        continue

                else:

                    # array bound x walls

                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current

                    gscore[neighbor] = tentative_g_score

                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

        return False


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

import heapq
import numpy as np


class TokenPassing:

    def __init__(self, cars, map, tasks):
        self.map = map
        self.cars = cars
        self.tasks = tasks
        self.bitmap = self.map.to_bitman_objects()
        self.time_plans = []
        for i in range(1000):
            self.time_plans.append(self.bitmap.tolist())
        self.current_time = 0

        for car in cars:
            self.time_plans[0][car.y][car.x] = car.id

        # self.map.print_map(self.time_plans[0])
        # print('----------')

    def do_step(self):
        print(f'\n\nTime: {self.current_time}')
        for i in range(len(self.cars)):
            if self.cars[i].possible_task is None:
                self.plan_route_to_start_task(self.cars[i])
            elif (not self.cars[i].current_task is None) and self.cars[i].current_task.start[1] == self.cars[i].x and \
                    self.cars[i].current_task.start[0] == self.cars[i].y:
                self.plan_route_to_end_task(self.cars[i])

        # self.map.print_map(self.time_plans[self.current_time])
        # print('----')
        # self.map.print_map(self.time_plans[self.current_time + 1])

        self.move_cars()
        self.current_time += 1

    def plan_route_to_start_task(self, car):
        if len(self.tasks) == 0:
            return

        next_task = None
        shortest_dis = None
        new_route = None
        for i in range(len(self.tasks)):
            if not self.check_possible_task(self.tasks[i]):
                continue

            if not self.tasks[i].state == 'ACTIVATED':
                continue
            route = self.astar((car.y, car.x), self.tasks[i].start)
            if route == False:
                continue
            route = route[::-1]
            distance = len(route)

            if next_task is None or shortest_dis > distance:
                next_task = self.tasks[i]
                shortest_dis = distance
                new_route = route
        if next_task is None:
            return
        print(f'Shortest task: {next_task.task_id}')
        car.possible_task = next_task
        self.reserve_route(car, new_route)

    def plan_route_to_end_task(self, car):
        route = self.astar((car.y, car.x), car.current_task.end)
        if route == False:
            return
        route = route[::-1]

        self.reserve_route(car, route)
        print(route)
        # self.map.print_map(self.time_plans[self.current_time])
        print('----')
        # self.map.print_map(self.time_plans[self.current_time + 1])

    def reserve_route(self, car, new_route):
        # self.map.print_map(self.time_plans[self.current_time])
        for i in range(len(new_route)):
            # print(f'Time: {self.current_time + 1 + i}  {new_route[i]}')

            self.time_plans[self.current_time + 1 + i][new_route[i][0]][new_route[i][1]] = car.id
            # self.map.print_map(self.time_plans[self.current_time + 1 + i])
            # print('======')

    def move_cars(self):
        next_state = self.time_plans[self.current_time + 1]
        curr_state = self.time_plans[self.current_time]

        for i in range(len(self.cars)):
            car = self.cars[i]

            if next_state[car.y][car.x] == curr_state[car.y][car.x]:
                print('WAIT')
                self.time_plans[self.current_time + 1][car.y][car.x] = car.id

                ...  # Wait

            elif next_state[car.y][car.x + 1] == curr_state[car.y][car.x]:
                car.go_right()
                print('RIGHT')
            elif next_state[car.y][car.x - 1] == curr_state[car.y][car.x]:
                car.go_left()
                print('LEFTG')
            elif next_state[car.y + 1][car.x] == curr_state[car.y][car.x]:
                car.go_down()
                print('DOWN')
            elif next_state[car.y - 1][car.x] == curr_state[car.y][car.x]:
                car.go_up()
                print('UP')
            else:
                print('ERROR')
                # exit()

    def check_possible_task(self, task):
        for car in self.cars:
            if car.possible_task is None:
                continue
            if car.possible_task.task_id == task.task_id:
                return False
        return True

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        close_set = set()

        came_from = {}

        gscore = {start: 0}

        fscore = {start: self.heuristic(start, goal)}

        oheap = []

        heapq.heappush(oheap, (fscore[start], start, self.current_time + 1))

        while oheap:

            heap_item = heapq.heappop(oheap)
            # print(heap_item)
            current = heap_item[1]
            time = heap_item[2]

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

                if 0 <= neighbor[0] < self.bitmap.shape[0]:

                    if 0 <= neighbor[1] < self.bitmap.shape[1]:

                        if not self.time_plans[time][neighbor[0]][neighbor[1]] == 0:
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

                    heapq.heappush(oheap, (fscore[neighbor], neighbor, time + 1))

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

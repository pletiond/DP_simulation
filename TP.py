from map import *
import copy
from Car import *


class TP:

    def __init__(self, cars, map, tasks, car_points):
        self.map = map
        self.cars = cars
        self.tasks = tasks
        self.bitmap = self.map.to_bitman_objects()
        self.objects_map = self.bitmap.tolist()
        for i in range(len(self.bitmap)):
            for j in range(len(self.bitmap[i])):
                self.objects_map[i][j] = []
        self.time_plans = []
        for i in range(10000):
            self.time_plans.append(copy.deepcopy(self.objects_map))
        self.current_time = 0
        self.car_points = car_points
        for cp in car_points:
            l = cp.location
            self.bitmap[l[0]][l[1]] = 0

        for car in cars:
            self.time_plans[0][car.y][car.x].append((car.id, car.orientation))

    def do_step(self):
        print(f'\n\nTime: {self.current_time}')
        for a in self.cars:
            for b in self.cars:
                if a == b:
                    continue
                if a.x == b.x and a.y == b.y and a.orientation == b.orientation:
                    print('LOCATION ERROR')
                    print(a)
                    print(b)
                    input('.......')

        self.park_cars()

        for i in range(len(self.cars)):
            if self.cars[i].possible_task is None:
                self.plan_route_for_car(self.cars[i])
        self.try_to_add_car()

        self.move_cars()
        self.check_tasks()
        self.current_time += 1

    def try_to_add_car(self):

        for cp in range(len(self.car_points)):
            if self.car_points[cp].cars_available == 0:
                continue

            loc = self.car_points[cp].location
            if self.bitmap[loc[0] - 1][loc[1]] == 0:
                orientation = 'UP'
            elif self.bitmap[loc[0] + 1][loc[1]] == 0:
                orientation = 'DOWN'
            elif self.bitmap[loc[0]][loc[1] - 1] == 0:
                orientation = 'LEFT'
            elif self.bitmap[loc[0]][loc[1] + 1] == 0:
                orientation = 'RIGHT'
            else:
                continue
            empty = True
            for car in self.cars:
                l = (car.y, car.x)
                if self.car_points[cp].location == l and car.orientation == orientations[orientation]:
                    empty = False
                    break
            if not empty:
                continue
            new_car = Car(loc, self.map, self.car_points[cp].tile_len, orientation, self.car_points[cp].speed)
            self.cars.append(new_car)

            res = self.plan_route_for_car(new_car)
            if not res:
                self.cars.remove(new_car)
                continue
            self.car_points[cp].cars_available -= 1

    def check_tasks(self):
        to_remove = []
        for t in range(len(self.tasks)):
            task = self.tasks[t]
            for c in range(len(self.cars)):
                car = self.cars[c]
                car_pos = (car.y, car.x)
                if car_pos == task.start and car.possible_task == task and car.current_task is None:
                    car.current_task = task
                    car.possible_task = task
                    task.assign(car)
                    self.map.map[car.y][car.x] = Task_Point()
                elif car_pos == task.end and car.current_task == task:
                    car.current_task = None
                    car.possible_task = None
                    task.complete()
                    to_remove.append(t)

                    self.map.map[car.y][car.x] = Task_Point()
        for t in to_remove[::-1]:
            r = self.tasks.pop(t)

    def plan_route_for_car(self, car):
        print(f'Planning route to start for car  {car.id}')

        next_task = None
        shortest_dis = None
        new_route = None
        new_orientations = None
        for i in range(len(self.tasks)):
            if not self.check_possible_task(self.tasks[i]):
                continue

            route, all_orientations = self.astar(car.id, (car.y, car.x), self.tasks[i].start, car.orientation)

            if route == False:
                continue
            route2, all_orientations2 = self.astar(car.id, self.tasks[i].start, self.tasks[i].end, all_orientations[-1],
                                                   offset=len(route) - 1)
            if route2 == False:
                continue

            best_loc = None
            min_len = None
            loc = self.tasks[i].end
            for cp in self.car_points:
                if best_loc is None or self.heuristic(loc, cp.location) < min_len:
                    min_len = self.heuristic(loc, cp.location)
                    best_loc = cp.location

            route3, all_orientations3 = self.astar(car.id, self.tasks[i].end, best_loc, all_orientations2[-1],
                                                   offset=len(route) + len(route2) - 2)
            if route3 == False:
                continue
            route = route[0:-1] + route2[0:-1] + route3
            all_orientations = all_orientations[0:-1] + all_orientations2[0:-1] + all_orientations3
            distance = len(route)

            if next_task is None or shortest_dis > distance:
                next_task = self.tasks[i]
                shortest_dis = distance
                new_route = route
                new_orientations = all_orientations
        if next_task is None:
            return False
        print(next_task)
        print('Route:')
        print(new_route)
        print('-')
        car.possible_task = next_task
        if (car.y, car.x) == next_task.start:
            car.current_task = next_task
            next_task.assign(car)
            self.map.map[car.y][car.x] = Task_Point()
        self.delete_future_plans(car)
        self.reserve_route(car, new_route, new_orientations)

        return True

    def delete_future_plans(self, car):
        found = True
        time = 0
        while found:
            found = False
            for i in range(len(self.time_plans[self.current_time + time])):
                for j in range(len(self.time_plans[self.current_time + time][i])):
                    tile = self.time_plans[self.current_time + time][i][j]
                    for c in range(len(tile)):
                        if tile[c][0] == car.id:
                            found = True
                            tile.pop(c)
                            break
            time += 1

    def reserve_route(self, car, new_route, new_orientations):
        for i in range(len(new_route)):
            self.time_plans[self.current_time + i][new_route[i][0]][new_route[i][1]].append(
                (car.id, new_orientations[i]))

    def move_cars(self):
        next_state = self.time_plans[self.current_time + 1]

        for i in range(len(self.cars)):
            car = self.cars[i]
            print(car)
            res = None

            if car.id in [x[0] for x in next_state[car.y][car.x]]:
                print(f'Car {car.id} WAIT')
                car.wait()

            elif car.id in [x[0] for x in next_state[car.y][car.x + 1]]:
                res = car.go_right()
                print(f'Car {car.id} RIGHT')
            elif car.id in [x[0] for x in next_state[car.y][car.x - 1]]:
                res = car.go_left()
                print(f'Car {car.id} LEFT')
            elif car.id in [x[0] for x in next_state[car.y + 1][car.x]]:
                res = car.go_down()
                print(f'Car {car.id} DOWN')
            elif car.id in [x[0] for x in next_state[car.y - 1][car.x]]:
                res = car.go_up()
                print(f'Car {car.id} UP')
            else:
                print('MOVE CARS ERRORR!!!')
                print(car)
                input('...')
                car.wait()
            if res == False:
                print('ERROR CANT MOVE!!!---')

    def check_possible_task(self, task):
        for car in self.cars:
            if car.possible_task is None:
                continue
            if car.possible_task.task_id == task.task_id:
                return False
        return True

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, agent_id, start, end, orientation, offset=0):
        start_node = ANode(None, start)
        start_node.g = start_node.h = start_node.f = 0
        start_node.orientation = orientation
        end_node = ANode(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = open_list[index]
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                all_orientations = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    all_orientations.append(current.orientation)
                    current = current.parent
                if not all_orientations[::-1][0] == start_node.orientation:
                    input('---')
                return path[::-1], all_orientations[::-1]  # Return reversed path

            # Generate children
            children = []
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for new_position in directions + [(0, 0)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                if new_position == directions[(current_node.orientation + 2) % 4]:
                    continue

                # Make sure within range
                if node_position[0] > (len(self.bitmap) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.bitmap[len(self.bitmap) - 1]) - 1) or node_position[1] < 0:
                    continue

                new_orientation = None
                if new_position == (0, 0) or new_position == directions[current_node.orientation]:
                    new_orientation = current_node.orientation
                elif new_position == directions[(current_node.orientation - 1) % 4]:
                    new_orientation = (current_node.orientation - 1) % 4
                elif new_position == directions[(current_node.orientation + 1) % 4]:
                    new_orientation = (current_node.orientation + 1) % 4

                if self.bitmap[node_position[0]][node_position[1]] != 0 or not self.check_constrain(agent_id,
                                                                                                    current_node.g + 1 + offset,
                                                                                                    (
                                                                                                            node_position[
                                                                                                                0],
                                                                                                            node_position[
                                                                                                                1]), (
                                                                                                            current_node.position[
                                                                                                                0],
                                                                                                            current_node.position[
                                                                                                                1]),
                                                                                                    new_orientation):
                    continue

                # Create new node

                new_node = ANode(current_node, node_position, new_orientation)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
                # Child is on the closed list
                skip = False
                for closed_child in closed_list:
                    if child == closed_child and closed_child.f == child.f and child.orientation == closed_child.orientation:
                        skip = True
                        break
                if skip:
                    continue

                # Child is already in the open list
                skip = False
                for open_node in open_list:
                    if child == open_node and child.f >= open_node.f and child.orientation == open_node.orientation:
                        skip = True
                        break

                if skip:
                    continue

                # Add the child to the open list
                open_list.append(child)

        return False, False

    def check_constrain(self, agent_id, time, position, from_, orientation):
        tile = self.time_plans[self.current_time + time][position[0]][position[1]]
        if len(tile) == 0:
            return True
        elif len(tile) == 1 and not self.is_on_crossroads(position) and not tile[0][1] == orientation:
            return True
        return False

    def is_on_crossroads(self, node_position):
        count = 0
        if node_position[0] > 0 and self.bitmap[node_position[0] - 1][node_position[1]] == 0:
            count += 1
        if node_position[1] > 0 and self.bitmap[node_position[0]][node_position[1] - 1] == 0:
            count += 1
        if node_position[0] < len(self.bitmap) and self.bitmap[node_position[0] + 1][node_position[1]] == 0:
            count += 1
        if node_position[1] < len(self.bitmap[0]) and self.bitmap[node_position[0]][node_position[1] + 1] == 0:
            count += 1
        if count > 2:
            return True
        else:
            return False

    @staticmethod
    def heuristic(a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def park_cars(self):
        to_remove = []
        for i in range(len(self.cars)):
            if self.cars[i].possible_task is not None:
                continue
            car_loc = (self.cars[i].y, self.cars[i].x)
            for cp in range(len(self.car_points)):
                if self.car_points[cp].location == car_loc:
                    to_remove.append(i)
                    self.car_points[cp].cars_available += 1

        for j in to_remove[::-1]:
            self.cars.pop(j)


class ANode():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, orientation=None):
        self.parent = parent
        self.position = position
        self.orientation = orientation

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

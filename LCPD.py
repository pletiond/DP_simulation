from Car import *
import copy
from Parking import *
from Task import *


class ANode():
    def __init__(self, parent=None, position=None, orientation=None, waiting=False):
        self.parent = parent
        self.position = position
        self.orientation = orientation
        self.waiting = waiting

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return f'Pos: {self.position}, Ori: {self.orientation},  G H F: {self.g} {self.h} {self.f}'

    def __repr__(self):
        return self.__str__()


class LCPD:

    def __init__(self, cars, map, tasks, car_points):
        self.map = map
        self.cars = cars
        self.tasks = tasks
        self.bitmap = self.map.to_bitman_objects()
        self.car_points = car_points
        self.current_time = 0
        self.moved = 0
        # self.parking = Probabilistic_Parking(car_points)
        self.parking = Dummy_Parking(car_points)
        self.number_of_astar = 0
        self.routes = {}
        for cp in car_points:
            l = cp.location
            self.bitmap[l[0]][l[1]] = 0

        self.do_replan = True
        self.tasks_time = []

    def do_step(self):
        print(f'\nStep {self.current_time}')
        for a in self.cars:
            for b in self.cars:
                if a == b:
                    continue
                if a.x == b.x and a.y == b.y and a.orientation == b.orientation:
                    print('LOCATION ERROR')
                    print(a)
                    print(b)
                    input('.......')

        for t in self.tasks:
            print(t)
        print()
        test_set = set()
        for c in self.cars:
            print(c)
            if c.current_task is not None:
                test_set.add(c.current_task)
        self.park_cars(only_in=True)
        self.unpark_cars()

        if self.do_replan:
            self.replan()

        self.park_cars()
        self.move_cars()
        self.check_tasks()
        self.current_time += 1

    def check_tasks(self):
        to_remove = []
        for t in range(len(self.tasks)):
            task = self.tasks[t]
            for c in range(len(self.cars)):
                car = self.cars[c]
                car_pos = (car.y, car.x)
                if car_pos == task.start and car.current_task is None and task.car is None:
                    car.current_task = task
                    car.possible_task = task
                    task.assign(car, self.current_time)
                    self.map.map[car.y][car.x] = Task_Point()
                    self.do_replan = True
                    self.parking.add_location(task.start)
                elif car_pos == task.end and car.current_task is not None and car.current_task.task_id == task.task_id:
                    car.current_task = None
                    car.possible_task = None
                    self.tasks[t].complete(self.current_time)
                    to_remove.append(t)
                    time = self.tasks[t].assign_time - self.tasks[t].in_time
                    self.tasks_time.append(time)

                    self.map.map[car.y][car.x] = Task_Point()
                    self.do_replan = True
        for t in to_remove[::-1]:
            self.tasks.pop(t)

    def replan(self):
        self.assign_free_agents()

        free_agents_plans = []

        for a in self.cars:

            if a.possible_task is None:
                next = self.parking.where_to_park((a.y, a.x))
                new_plan = {'id': a.id, 'orientation': a.orientation, 'start': (a.y, a.x), 'end': None,
                            'task_end': next, 'VIP': False}
                free_agents_plans.append(new_plan)
                continue
            # print(f'Car {a.y} - {a.x}   Task {a.possible_task.start} -> {a.possible_task.end}  Current: {a.current_task is not None}')
            if a.current_task is None:
                # print(f'Car {a.id}       {a.possible_task.task_id} -')
                new_plan = {'id': a.id, 'orientation': a.orientation, 'start': (a.y, a.x), 'end': None,
                            'task_end': a.possible_task.start, 'VIP': a.possible_task.is_VIP}
                free_agents_plans.append(new_plan)
            elif a.current_task is not None:
                # print(f'Car {a.id}        {a.possible_task.task_id} {a.current_task.task_id}')
                new_plan = {'id': a.id, 'orientation': a.orientation, 'start': (a.y, a.x), 'end': None,
                            'task_end': a.current_task.end, 'VIP': a.possible_task.is_VIP}
                free_agents_plans.append(new_plan)

        # print(free_agents_plans)
        cbs = CBS(self.bitmap, free_agents_plans)
        self.routes, num_astar = cbs.solve()
        self.number_of_astar += num_astar
        if self.routes is None:
            self.routes = cbs.solve(ignore_VIP=True)

        for a in self.cars:
            if a.id in self.routes.keys():
                continue
            print('AGENT IS NOT IN ROUTES PLANNING------------------------')
        self.do_replan = False

    def assign_free_agents(self):
        free_agents = self.get_free_agents()
        free_tasks = self.get_free_tasks()

        self.assign_VIP(free_agents, free_tasks)

        metrics = {}

        for t in free_tasks:
            metrics[t] = []
            for a in free_agents:
                route_len = CBS.heuristic((a.y, a.x), t.start)
                score = route_len - (self.current_time - t.in_time)
                metrics[t].append((a, score))

            metrics[t].sort(key=lambda tup: tup[1])

        assignned = {}

        while True:

            if len(assignned.keys()) == len(free_agents) or len(metrics) == 0:
                break
            for a in free_agents:
                if a in assignned.keys():
                    continue
                best_task = None
                t_len = None
                for t, arr in metrics.items():
                    if len(arr) == 0 or not arr[0][0].id == a.id:
                        continue

                    if best_task is None or t_len > arr[0][1]:
                        best_task = t
                        t_len = arr[0][1]
                if best_task is None:
                    continue
                del metrics[best_task]
                assignned[a] = best_task
                for task in metrics.keys():
                    for i in range(len(metrics[task])):
                        if metrics[task][i][0].id == a.id:
                            metrics[task].pop(i)
                            break

        for key, value in assignned.items():
            for a in range(len(free_agents)):
                for t in range(len(free_tasks)):
                    if free_agents[a] == key and value == free_tasks[t]:
                        # print(f'Car {key.id} - Task {value.task_id}')
                        key.possible_task = value
                        if (key.y, key.x) == value.start:
                            key.current_task = value
                            value.assign(key, self.current_time)

    def assign_VIP(self, free_agents, free_tasks):
        to_remove = []
        for t, task in enumerate(copy.deepcopy(free_tasks), start=0):

            if not task.is_VIP:
                continue
            nearest_car_index = None
            shortest_dist = None
            for c, car in enumerate(free_agents.copy(), start=0):
                route_len = CBS.heuristic((car.y, car.x), task.start)
                if shortest_dist is None or route_len < shortest_dist:
                    shortest_dist = route_len
                    nearest_car_index = c
            if nearest_car_index is None:
                continue
            free_agents[nearest_car_index].possible_task = task
            if shortest_dist == 0:
                free_agents[nearest_car_index].current_task = free_tasks[t]
                free_tasks[t].assign(free_agents[nearest_car_index], self.current_time)
            print(f'VIP Task {task} has {free_agents[nearest_car_index]}')

            to_remove.append(t)
            free_agents.remove(free_agents[nearest_car_index])
        for t in to_remove[::-1]:
            free_tasks.pop(t)

    def get_free_agents(self):
        free_agents = []
        for a in range(len(self.cars)):
            if self.cars[a].current_task is None:
                self.cars[a].possible_task = None
                free_agents.append(self.cars[a])

        return free_agents

    def get_free_tasks(self):
        free_tasks = []
        for t in range(len(self.tasks)):
            if self.tasks[t].car is None:
                free_tasks.append(self.tasks[t])

        return free_tasks

    def move_cars(self):

        for i in range(len(self.cars)):
            self.moved += 1
            route = self.routes[self.cars[i].id]
            if len(route) == 1:
                self.cars[i].wait()
                route.pop(0)
                continue
            curr_pos = route[0]
            next_pos = route[1]
            diff = tuple(x - y for x, y in zip(next_pos, curr_pos))

            car = self.cars[i]
            res = None

            if diff == (0, 1):
                res = car.go_right()
                # print(f'Car {car.id} RIGHT')
            elif diff == (0, -1):
                res = car.go_left()
                # print(f'Car {car.id} LEFT')
            elif diff == (1, 0):
                res = car.go_down()
                # print(f'Car {car.id} DOWN')
            elif diff == (-1, 0):
                res = car.go_up()
                # print(f'Car {car.id} UP')
            elif diff == (0, 0):
                # print(f'Car {car.id} ERROR---------!!!!')
                car.wait()
            else:
                print('DIFF error')
                exit(1)

            if res == False:
                print('ERROR CANT MOVE!!!---')
            route.pop(0)

    def park_cars(self, only_in=False):
        for cp in range(len(self.car_points)):
            self.car_points[cp].park_cars(self.current_time, only_in)

    def unpark_cars(self):
        for cp in range(len(self.car_points)):
            if not self.car_points[cp].is_car_available():
                continue

            self.car_points[cp].unpark_car()
            self.do_replan = True
            self.car_points[cp].cars_available -= 1


class CBS:

    def __init__(self, map, agents):
        self.map = map
        self.agents = agents
        self.number_of_astar = 0
        self.current_time = 0
        self.curr_node = None

    def solve(self, ignore_VIP=False):
        # print('CBS solve')
        self.OPEN = []
        root = Node()
        self.curr_node = root
        self.get_init_solutions()
        root.compute_cost()
        self.OPEN.append(root)

        while len(self.OPEN) > 0:
            self.curr_node = self.get_best_node()  # lowest solution cost
            conflicts, edge_conflicts = self.validate_solution()
            if not ignore_VIP:
                self.validate_VIP(conflicts, edge_conflicts)

            if len(conflicts) == 0 and len(edge_conflicts) == 0:
                for a, sol in self.curr_node.solution.items():
                    if sol is None:
                        input('empty sol!!!!')
                return self.curr_node.solution, self.number_of_astar  # goal
            # Node conflict
            if len(conflicts) > 0:
                first_conflict = conflicts[0]
                # print(first_conflict)

                # print('\n')
                for a in first_conflict['agents']:
                    # print(a)
                    new_node = Node()
                    new_node.constraints = self.curr_node.constraints.copy()
                    new_node.edge_constraints = self.curr_node.edge_constraints.copy()
                    new_node.add_constraint(a, first_conflict['position'], first_conflict['time'])
                    new_node.solution = self.curr_node.solution.copy()
                    new_node.orientations = self.curr_node.orientations.copy()
                    # Update solutions
                    self.update_solution(new_node, a)
                    new_node.compute_cost()

                    # print(new_node)
                    if not new_node.cost is None:
                        self.OPEN.append(new_node)
                        # print('ADDED')

            # Edge conflict
            else:
                first_conflict = edge_conflicts[0]
                # print(first_conflict)

                for a in first_conflict['agents']:
                    new_node = Node()
                    new_node.constraints = self.curr_node.constraints.copy()
                    new_node.edge_constraints = self.curr_node.edge_constraints.copy()
                    new_node.add_edge_constraint(a, first_conflict['from'], first_conflict['to'],
                                                 first_conflict['time'])
                    new_node.solution = self.curr_node.solution.copy()
                    new_node.orientations = self.curr_node.orientations.copy()
                    # Update solutions
                    self.update_solution(new_node, a)
                    new_node.compute_cost()

                    if not new_node.cost is None:
                        self.OPEN.append(new_node)

    def get_init_solutions(self):
        for agent in self.agents:
            id = agent['id']
            orientation = agent['orientation']
            start = agent['start']
            end = agent['end']
            task_end = agent['task_end']
            if end is None:
                route_to_end, all_orientations = self.astar(self.curr_node, id, orientation, start, task_end)
                self.curr_node.solution[id] = route_to_end
                self.curr_node.orientations[id] = all_orientations
                continue

            route_to_task, all_orientations1 = self.astar(self.curr_node, id, orientation, start, end)

            orientation = all_orientations1[-1]
            route_to_end, all_orientations2 = self.astar(self.curr_node, id, orientation, end, task_end)

            merged_routes = route_to_task[0:-1] + route_to_end
            merged_orientations = all_orientations1[0:-1] + all_orientations2

            self.curr_node.solution[id] = merged_routes
            self.curr_node.orientations[id] = merged_orientations

    def update_solution(self, node, agent_id):
        agent = None
        for a in self.agents:
            if a['id'] == agent_id:
                agent = a.copy()
                break
        id = agent['id']
        orientation = agent['orientation']
        start = agent['start']
        end = agent['end']
        task_end = agent['task_end']

        if end is None:
            route_to_end, all_orientations = self.astar(node, id, orientation, start, task_end)
            if not route_to_end:
                node.solution[id] = None
                return
            node.solution[id] = route_to_end
            node.orientations[id] = all_orientations
            return

        route_to_task, all_orientations1 = self.astar(node, id, orientation, start, end)
        if not route_to_task:
            node.solution[id] = None
            return
        route_to_end, all_orientations2 = self.astar(node, id, all_orientations1[-1], end, task_end,
                                                     offset=len(route_to_task) - 1)
        if not route_to_end:
            node.solution[id] = None
            return
        merged_routes = route_to_task[0:-1] + route_to_end
        merged_orientations = all_orientations1[0:-1] + all_orientations2

        node.solution[id] = merged_routes
        node.orientations[id] = merged_orientations

    def get_best_node(self):
        best_node = None
        for node in self.OPEN:
            if node.cost is None:
                continue

            if best_node is None:
                best_node = node
            elif node.cost < best_node.cost:
                best_node = node

        self.OPEN.remove(best_node)
        return best_node

    def validate_solution(self):
        conflicts = []
        edge_conflicts = []
        max_len = 0
        for sol in self.curr_node.solution.values():
            if max_len < len(sol):
                max_len = len(sol)

        all_orientations = self.curr_node.orientations
        for i in range(max_len):
            occupied = {}
            for agent, sol in self.curr_node.solution.items():
                if i >= len(sol):
                    continue
                if not sol[i] in occupied:
                    occupied[sol[i]] = [agent]
                else:
                    occupied[sol[i]].append(agent)

                # edge check
                for agent2, sol2 in self.curr_node.solution.items():
                    if agent2 == agent or len(sol2) - 1 <= i or len(sol) - 1 <= i:
                        continue
                    if sol[i] == sol2[i] and sol[i + 1] == sol2[i + 1]:
                        edge_conflict = {'agents': [agent, agent2], 'from': sol[i], 'to': sol[i + 1], 'time': i}
                        edge_conflicts.append(edge_conflict)

            for key, value in occupied.items():
                if len(value) < 2:
                    continue
                for a1 in value:
                    for a2 in value:
                        if a1 == a2:
                            continue

                        conflict = {'agents': [a1, a2], 'position': key, 'time': i}
                        if len(value) == 2 and not self.is_on_crossroads(key) and not all_orientations[a1][i] == \
                                                                                      all_orientations[a2][i]:
                            continue

                        conflicts.append(conflict)
                        return conflicts, edge_conflicts

        return conflicts, edge_conflicts

    def validate_VIP(self, conflicts, edge_conflicts):
        if len(conflicts) > 0:
            agents_id = conflicts[0]['agents']
            agent1 = None
            agent2 = None
            for a in self.agents:
                if a['id'] == agents_id[0]:
                    agent1 = a['VIP']
                if a['id'] == agents_id[1]:
                    agent2 = a['VIP']
            if agent1 and not agent2:
                print(agents_id)
                conflicts[0]['agents'].pop(0)
                print(conflicts)

            elif not agent1 and agent2:
                print(agents_id)
                conflicts[0]['agents'].pop(1)
                print(conflicts)

        elif len(edge_conflicts) > 0:
            ...

    @staticmethod
    def heuristic(a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def check_constrain(self, node, agent_id, time, position, from_):
        for c in node.constraints:
            if c[0] == agent_id and c[1] == position and c[2] == time:
                return False

        for e in node.edge_constraints:
            if e[0] == agent_id and e[3] == time - 1 and (
                    (e[1] == position and e[2] == from_) or (e[2] == position and e[1] == from_)):
                return False

        return True

    def astar(self, node, agent_id, orientation, start, end, offset=0):

        self.number_of_astar += 1
        start_node = ANode(None, start)
        start_node.g = start_node.h = start_node.f = 0
        start_node.orientation = orientation
        end_node = ANode(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            open_list.sort(key=lambda x: x.f)
            best_score = open_list[0].f
            best_not_waiting_score = 0
            for index, item in enumerate(open_list):
                if item.f > best_score:
                    break
                current = open_list[index]
                not_waiting_score = 0
                while current is not None:
                    if current.waiting:
                        break
                    not_waiting_score += 1
                    current = current.parent

                if best_not_waiting_score < not_waiting_score:
                    current_node = open_list[index]
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                all_orientations = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    all_orientations.append(current.orientation)
                    current = current.parent
                return path[::-1], all_orientations[::-1]

            children = []
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for new_position in directions + [(0, 0)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                if new_position == directions[(current_node.orientation + 2) % 4]:
                    continue

                if node_position[0] > (len(self.map) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.map[len(self.map) - 1]) - 1) or node_position[1] < 0:
                    continue

                if self.map[node_position[0]][node_position[1]] != 0 or not self.check_constrain(node, agent_id,
                                                                                                 current_node.g + 1 + offset,
                                                                                                 (
                                                                                                         node_position[
                                                                                                             0],
                                                                                                         node_position[
                                                                                                             1]), (
                                                                                                         current_node.position[
                                                                                                             0],
                                                                                                         current_node.position[
                                                                                                             1])):
                    continue

                new_orientation = None
                if new_position == (0, 0) or new_position == directions[current_node.orientation]:
                    new_orientation = current_node.orientation
                elif new_position == directions[(current_node.orientation - 1) % 4]:
                    new_orientation = (current_node.orientation - 1) % 4
                elif new_position == directions[(current_node.orientation + 1) % 4]:
                    new_orientation = (current_node.orientation + 1) % 4
                new_node = ANode(current_node, node_position, new_orientation, new_position == (0, 0))

                children.append(new_node)

            for child in children:

                child.g = current_node.g + 1
                if child.g > 500:
                    continue
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                skip = False
                for closed_child in closed_list:
                    if child == closed_child and closed_child.f == child.f and child.orientation == closed_child.orientation:
                        skip = True
                        break
                if skip:
                    continue

                skip = False
                for open_node in open_list:
                    if child == open_node and child.f >= open_node.f and child.orientation == open_node.orientation:
                        skip = True
                        break

                if skip:
                    continue

                open_list.append(child)

        return False, False

    def is_on_crossroads(self, node_position):
        count = 0
        if node_position[0] > 0 and self.map[node_position[0] - 1][node_position[1]] == 0:
            count += 1
        if node_position[1] > 0 and self.map[node_position[0]][node_position[1] - 1] == 0:
            count += 1
        if node_position[0] < len(self.map) and self.map[node_position[0] + 1][node_position[1]] == 0:
            count += 1
        if node_position[1] < len(self.map[0]) and self.map[node_position[0]][node_position[1] + 1] == 0:
            count += 1
        if count > 2:
            return True
        else:
            return False


class Node:

    def __init__(self):
        self.solution = {}
        self.orientations = {}
        self.constraints = []
        self.edge_constraints = []
        self.cost = None

    def set_solution(self):
        ...

    def add_constraint(self, agent, position, time):
        self.constraints.append((agent, position, time))

    def add_edge_constraint(self, agent, v1, v2, time):
        self.edge_constraints.append((agent, v1, v2, time))

    def compute_cost(self):
        cost = 0
        for sol in self.solution.values():
            if sol is None:
                self.cost = None
                return

            cost += len(sol)
        self.cost = cost

    def __str__(self):
        return f'Solutions: {self.solution}\nConstraints: {self.constraints}\nEdge_constraints: {self.edge_constraints}\nCost: {self.cost}\n'


if __name__ == '__main__':
    map = [
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0]
    ]

    agents = [{'id': 1, 'start': (0, 1), 'end': (4, 1)},
              {'id': 2, 'start': (4, 1), 'end': (0, 1)}]

    cbs = CBS(map=map, agents=agents)

    final_sol = cbs.solve()
    print('==================')
    print(final_sol)

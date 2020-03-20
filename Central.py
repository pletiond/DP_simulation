import numpy as np
from map import Map
from task import *


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


class Central:

    def __init__(self, cars, map, tasks):
        self.map = map
        self.cars = cars
        self.tasks = tasks
        self.bitmap = self.map.to_bitman_objects()
        self.time_plans = []
        self.current_time = 0
        for i in range(100):
            self.time_plans.append(self.bitmap.tolist())
        # self.current_time = 0

        for car in cars:
            self.time_plans[0][car.y][car.x] = car.id

    def do_step(self):
        self.check_tasks()

        if self.check_change():
            # print('Replan')
            self.replan()

        self.move_cars()
        self.current_time += 1

    def check_tasks(self):
        for t in range(len(self.tasks)):
            task = self.tasks[t]
            for c in range(len(self.cars)):
                car = self.cars[c]
                car_pos = (car.y, car.x)
                if car_pos == task.start and car.current_task is None and task.car is None:
                    car.current_task = task
                    car.possible_task = task
                    task.assign(car)
                    self.map.map[car.y][car.x] = Task_Point()
                elif car_pos == task.end and car.current_task is not None and car.current_task.task_id == task.task_id:
                    car.current_task = None
                    car.possible_task = None
                    task.complete()
                    self.map.map[car.y][car.x] = Task_Point()

    def replan(self):
        for i in range(self.current_time + 1, len(self.time_plans)):
            self.time_plans[i] = self.bitmap.tolist()

        self.assign_free_agents()

        free_agents_plans = []

        for a in self.cars:
            print('======')

            if a.possible_task is None:
                print(f'Car {a.id}      - -')
                continue
            # print(f'Car {a.y} - {a.x}   Task {a.possible_task.start} -> {a.possible_task.end}  Current: {a.current_task is not None}')
            if a.current_task is None:
                print(f'Car {a.id}       {a.possible_task.task_id} -')
                new_plan = {'id': a.id, 'orientation': a.orientation, 'start': (a.y, a.x), 'end': a.possible_task.start,
                            'task_end': a.possible_task.end}
                free_agents_plans.append(new_plan)
            elif a.current_task is not None:
                print(f'Car {a.id}        {a.possible_task.task_id} {a.current_task.task_id}')
                new_plan = {'id': a.id, 'orientation': a.orientation, 'start': (a.y, a.x), 'end': None,
                            'task_end': a.possible_task.end}
                free_agents_plans.append(new_plan)

        cbs = CBS(self.map.to_bitman_objects(), free_agents_plans)
        routes = cbs.solve()

        # print(routes)

        for id, route in routes.items():
            for i in range(len(route)):
                if self.current_time + i >= len(self.time_plans):
                    self.time_plans.append(self.bitmap.tolist())
                step = route[i]
                self.time_plans[self.current_time + i][step[0]][step[1]] = id
        for a in self.cars:
            if a.id in routes.keys():
                continue
            self.time_plans[self.current_time + 1][a.y][a.x] = a.id

    def assign_free_agents(self):
        free_agents = self.get_free_agents()
        free_tasks = self.get_free_tasks()

        metrics = {}

        for t in free_tasks:
            metrics[t] = []
            for a in free_agents:
                route_len = CBS.heuristic((a.y, a.x), t.start)
                metrics[t].append((a, route_len))

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
                for t, arr in metrics.items():
                    if len(arr) > 0 and arr[0][0].id == a.id:
                        metrics[t].pop(0)

        for key, value in assignned.items():
            for a in range(len(free_agents)):
                for t in range(len(free_tasks)):
                    if free_agents[a] == key and value == free_tasks[t]:
                        # print(f'Car {key.id} - Task {value.task_id}')
                        key.possible_task = value

    def get_free_agents(self):
        free_agents = []
        for a in range(len(self.cars)):
            if self.cars[a].current_task is None and self.cars[a].possible_task is None:
                free_agents.append(self.cars[a])

        return free_agents

    def get_free_tasks(self):
        free_tasks = []
        for t in range(len(self.tasks)):
            free = True
            for a in range(len(self.cars)):
                if self.cars[a].possible_task is None:
                    continue
                if self.cars[a].possible_task.task_id == self.tasks[t].task_id:
                    free = False
                    break

            if free:
                free_tasks.append(self.tasks[t])

        return free_tasks

    def check_change(self):
        return True
        assingged_agents = 0
        for a in self.cars:
            if a.possible_task is not None:
                assingged_agents += 1
        if assingged_agents == len(self.cars):
            return False
        elif assingged_agents == len(self.tasks):
            return False
        return True

    def move_cars(self):
        # print('\nMove cars')
        next_state = self.time_plans[self.current_time + 1]
        curr_state = self.time_plans[self.current_time]

        for i in range(len(self.cars)):
            car = self.cars[i]
            res = None
            # if next_state[car.y][car.x] == curr_state[car.y][car.x]:
            #    # print(f'Car {car.id} WAIT')
            #    self.time_plans[self.current_time + 1][car.y][car.x] = car.id

            if next_state[car.y][car.x + 1] == curr_state[car.y][car.x]:
                res = car.go_right()
                # print(f'Car {car.id} RIGHT')
            elif next_state[car.y][car.x - 1] == curr_state[car.y][car.x]:
                res = car.go_left()
                # print(f'Car {car.id} LEFTG')
            elif next_state[car.y + 1][car.x] == curr_state[car.y][car.x]:
                res = car.go_down()
                # print(f'Car {car.id} DOWN')
            elif next_state[car.y - 1][car.x] == curr_state[car.y][car.x]:
                res = car.go_up()
                # print(f'Car {car.id} UP')
            else:
                # print(f'Car {car.id} ERROR---------!!!!')
                self.time_plans[self.current_time + 1][car.y][car.x] = car.id
                # exit()
            if res == False:
                print('ERROR CANT MOVE!!!---')


class CBS:

    def __init__(self, map, agents):
        self.map = map
        self.agents = agents

        self.current_time = 0
        self.curr_node = None

    def solve(self):
        # print('CBS solve')
        self.OPEN = []
        root = Node()
        self.curr_node = root
        # print('.')
        self.get_init_solutions()
        # print('..')
        root.compute_cost()
        # print('...')
        self.OPEN.append(root)

        while len(self.OPEN) > 0:
            self.curr_node = self.get_best_node()  # lowest solution cost
            conflicts, edge_conflicts = self.validate_solution()

            if len(conflicts) == 0 and len(edge_conflicts) == 0:
                return self.curr_node.solution  # goal
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
                    # Update solutions
                    self.update_solution(new_node, a)
                    new_node.compute_cost()

                    # print(new_node)
                    if not new_node.cost is None:
                        self.OPEN.append(new_node)
                        # print('ADDED')
                    # print('-------')
            # Edge conflict
            else:
                first_conflict = edge_conflicts[0]
                # print(first_conflict)

                # print('\n')
                for a in first_conflict['agents']:
                    # print(a)
                    new_node = Node()
                    new_node.constraints = self.curr_node.constraints.copy()
                    new_node.edge_constraints = self.curr_node.edge_constraints.copy()
                    new_node.add_edge_constraint(a, first_conflict['from'], first_conflict['to'],
                                                 first_conflict['time'])
                    new_node.solution = self.curr_node.solution.copy()
                    # Update solutions
                    self.update_solution(new_node, a)
                    new_node.compute_cost()

                    # print(new_node)
                    if not new_node.cost is None:
                        self.OPEN.append(new_node)
                        # print('ADDED')
                    # print('-------')

            # tmp = input('Ready?')
            # print('----------------------------------------------------------------------')

    def get_init_solutions(self):
        # Map.print_map(None,self.map)
        # print('Init----')
        for agent in self.agents:
            id = agent['id']
            orientation = agent['orientation']
            # print(f'Agent {id}:')
            start = agent['start']
            end = agent['end']
            task_end = agent['task_end']
            if end is None:
                route_to_end, orientation = self.astar(self.curr_node, id, orientation, start, task_end)
                if not route_to_end:
                    # print('skip')
                    continue
                self.curr_node.solution[id] = route_to_end
                continue

            # print(f'{start} -> {end} -> {task_end}')

            route_to_task, orientation = self.astar(self.curr_node, id, orientation, start, end)
            # print(route_to_task)

            if not route_to_task:
                # print('skip')
                continue
            route_to_end, orientation = self.astar(self.curr_node, id, orientation, end, task_end)
            if not route_to_end:
                # print('skip')
                continue
            # print(route_to_end)
            merged_routes = route_to_task[0:-1] + route_to_end

            self.curr_node.solution[id] = merged_routes

    def update_solution(self, node, agent_id):
        # print('Update----')
        agent = None
        for a in self.agents:
            if a['id'] == agent_id:
                agent = a.copy()
                break
        id = agent['id']
        orientation = agent['orientation']
        # print(f'Agent {id}:')
        start = agent['start']
        end = agent['end']
        task_end = agent['task_end']

        if end is None:
            route_to_end, orientation = self.astar(node, id, orientation, start, task_end)
            if not route_to_end:
                node.solution[id] = None
                return
            node.solution[id] = route_to_end
            return

        route_to_task, orientation = self.astar(node, id, orientation, start, end)
        route_to_end, orientation = self.astar(node, id, orientation, end, task_end, offset=len(route_to_task) - 1)
        if not route_to_task or not route_to_end:
            node.solution[id] = None
            return
        merged_routes = route_to_task[0:-1] + route_to_end
        # print(merged_routes)
        node.solution[id] = merged_routes
        # tmp = input('Ready?')

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
        # print(max_len)

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
                        # print('EDGE CONFLICT!!!!!')
                        edge_conflict = {'agents': [agent, agent2], 'from': sol[i], 'to': sol[i + 1], 'time': i}
                        edge_conflicts.append(edge_conflict)

            for key, value in occupied.items():
                if len(value) < 2:
                    continue
                conflict = {'agents': value, 'position': key, 'time': i}
                # conflicts.append(conflict)

        # print(conflicts)
        return conflicts, edge_conflicts

    @staticmethod
    def heuristic(a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def check_constrain(self, node, agent_id, time, position, from_):

        for c in node.constraints:
            if c[0] == agent_id and c[1] == position and c[2] == time:
                # print('--------------------- SKIP')
                return False
        if len(node.edge_constraints) == 0:
            return True

        # print(node.edge_constraints)
        # print(f'Agent: {agent_id} Time: {time} From: {from_} To: {position}' )

        for e in node.edge_constraints:
            if e[0] == agent_id and e[3] == time - 1 and (
                    (e[1] == position and e[2] == from_) or (e[2] == position and e[1] == from_)):
                # print('FALSE')
                # tmp = input('Ready?')
                return False

        # print('TRUE')

        return True

    def astar(self, node, agent_id, orientation, start, end, offset=0):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        # print('a star')
        start_node = ANode(None, start)
        start_node.g = start_node.h = start_node.f = 0
        start_node.orientation = orientation
        end_node = ANode(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
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
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1], current_node.orientation  # Return reversed path

            # Generate children
            children = []
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for new_position in directions + [(0, 0)]:
                if new_position == directions[(current_node.orientation + 2) % 4]:
                    continue
                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.map) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.map[len(self.map) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
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

                # Create new node
                new_orientation = None
                if new_position == (0, 0) or new_position == directions[current_node.orientation]:
                    new_orientation = current_node.orientation
                elif new_position == directions[(current_node.orientation - 1) % 4]:
                    new_orientation = (current_node.orientation - 1) % 4
                elif new_position == directions[(current_node.orientation + 1) % 4]:
                    new_orientation = (current_node.orientation + 1) % 4
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

        return False


class Node:

    def __init__(self):
        self.solution = {}
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
            if cost < len(sol):
                cost = len(sol)
        self.cost = cost

    def find_solutions(self):
        ...

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

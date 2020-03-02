import numpy as np


class ANode():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Central:

    def __init__(self):
        ...


class CBS:

    def __init__(self, map, agents):
        self.map = map
        self.agents = agents

        self.current_time = 0
        self.curr_node = None

    def solve(self):
        self.OPEN = []
        root = Node()
        self.curr_node = root
        self.get_init_solutions()
        root.compute_cost()
        self.OPEN.append(root)

        while len(self.OPEN) > 0:
            self.curr_node = self.get_best_node()  # lowest solution cost
            res = self.validate_solution()

            if len(res) == 0:
                return self.curr_node.solution  # goal

            first_conflict = res[0]
            print(first_conflict)
            # MA-CSB optional
            print('\n')
            for a in first_conflict['agents']:
                print(a)
                new_node = Node()
                new_node.constraints = self.curr_node.constraints.copy()
                new_node.add_constraint(a, first_conflict['position'], first_conflict['time'])
                new_node.solution = self.curr_node.solution.copy()
                # Update solutions
                self.update_solution(new_node, a)
                new_node.compute_cost()

                print(new_node)
                if not new_node.cost is None:
                    self.OPEN.append(new_node)
                    print('ADDED')
                print('-------')
            tmp = input('Ready?')
            print('----------------------------------------------------------------------')

    def get_init_solutions(self):
        for agent in self.agents:
            id = agent['id']
            print(f'Agent {id}:')
            start = agent['start']
            end = agent['end']
            route = self.astar(self.curr_node, id, start, end)
            if route == False:
                continue
            # route = route[::-1]
            print(route)
            self.curr_node.solution[id] = route

    def update_solution(self, node, agent_id):
        agent = None
        for a in self.agents:
            if a['id'] == agent_id:
                agent = a.copy()
                break
        id = agent['id']
        # print(f'Agent {id}:')
        start = agent['start']
        end = agent['end']
        # print(node.constraints)
        route = self.astar(node, id, start, end)
        if route == False:
            node.solution[id] = None
            return
        # route = route[::-1]
        # print(route)
        node.solution[id] = route

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

            for key, value in occupied.items():
                if len(value) < 2:
                    continue
                conflict = {'agents': value, 'position': key, 'time': i}
                conflicts.append(conflict)

        # print(conflicts)
        return conflicts

    def heuristic(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def check_constrain(self, node, agent_id, position, time):
        for c in node.constraints:
            if c[0] == agent_id and c[1] == position and c[2] == time:
                # print('--------------------- SKIP')
                return False

        return True

    def astar(self, node, agent_id, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = ANode(None, start)
        start_node.g = start_node.h = start_node.f = 0
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
                    current_node = item
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
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0),
                                 (0, 0)]:  # Adjacent squares , (-1, -1), (-1, 1), (1, -1), (1, 1)

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.map) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.map[len(self.map) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.map[node_position[0]][node_position[1]] != 0 or not self.check_constrain(node, agent_id, (
                node_position[0], node_position[1]), current_node.g + 1):
                    continue

                # Create new node
                new_node = ANode(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child and not current_node.position == new_node.position:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


class Node:

    def __init__(self):
        self.solution = {}
        self.constraints = []
        self.cost = None

    def set_solution(self):
        ...

    def add_constraint(self, agent, position, time):
        self.constraints.append((agent, position, time))

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
        return f'Solutions: {self.solution}\nConstrains: {self.constraints}\nCost: {self.cost}\n'


map = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

agents = [{'id': 1, 'start': (0, 1), 'end': (3, 2)},
          {'id': 2, 'start': (1, 0), 'end': (2, 3)}]

cbs = CBS(map=map, agents=agents)

final_sol = cbs.solve()
print('==================')
print(final_sol)

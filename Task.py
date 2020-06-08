import random
from ast import literal_eval as make_tuple

class Task:

    def __init__(self, start, end, map, time, out_file, is_VIP=False):
        self.map = map
        self.out_file = out_file
        self.task_id = self.map.task_id_max
        self.map.task_id_max += 1
        self.start = start
        self.end = end
        self.state = 'NEW'
        self.car = None
        self.in_time = time
        self.assign_time = None
        self.complete_time = None
        self.is_VIP = is_VIP

    def assign(self, car, time):
        self.state = 'ASSIGNED'
        self.car = car
        self.assign_time = time

    def complete(self, time):
        self.state = 'COMPLETED'
        self.complete_time = time
        with open(f'{self.out_file}.csv', 'a') as fp:
            fp.write(
                f'{self.task_id};{self.start};{self.end};{int(self.in_time)};{int(self.assign_time)};{int(self.complete_time)};{self.car.id};{self.is_VIP}\n')

    def __str__(self):
        return f'TID: {self.task_id} From: {self.start} To: {self.end} VIP: {self.is_VIP}'

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
            # print("ASSIGN--------")
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

    def __init__(self, tasks, map, cars, max_tasks, out_file):
        self.tasks = tasks
        self.map = map
        self.cars = cars
        self.points = []
        self.max_tasks = max_tasks
        self.out_file = out_file
        bitmap = map.to_bitman()
        for row in range(len(bitmap)):
            for col in range(len(bitmap[row])):
                if bitmap[row][col] == 0 and not self.is_on_crossroads(bitmap, (row, col)):
                    self.add_spawn_point((row, col), 1, '')

        # print(f'Total spawn points: {len(self.points)}')

        with open(f'{self.out_file}.csv', 'a') as fp:
            fp.write(f'task_id;start;end;in_time;assign_time;complete_time;car_id;is_VIP\n')

    def add_spawn_point(self, location, spawn_rate, orientation):
        self.points.append((location, spawn_rate, orientation))
        # self.map.map[location[0]][location[1]] = Task_Point()

    def do_step(self, time):
        # if len(self.tasks):
        #    print(f'Longest: {time - self.tasks[0].in_time}')
        #    if time - self.tasks[0].in_time >= 50:
        #        print(time)
        #        print('END')
        #        exit(0)

        # if time % 5 == 0:
        #    for _ in range(time//100 +1):
        #        self.create_task(time)
        # print(f'Tasks: {len(self.tasks)}')

        while len(self.tasks) < self.max_tasks:
            self.create_task(time)

    def create_task(self, time):
        start, end = self.get_random_free_points()
        if start == False:
            return
        # if time > 5 and time % 5 == 0:
        #    new_task = Task(start, end, self.map, time, self.out_file, is_VIP= True)
        # else:
        #    new_task = Task(start, end, self.map, time, self.out_file)
        new_task = Task(start, end, self.map, time, self.out_file)
        self.tasks.append(new_task)

    def get_random_free_points(self):
        free_starts = []
        free_ends = []
        for point in self.points:

            free_ends.append(point)
            for i in range(point[1]):
                free_starts.append(point)
        if len(free_ends) < 2:
            return False, False

        start = random.choice(free_starts)
        end = random.choice(free_ends)
        while start == end:
            free_ends.remove(start)
            end = random.choice(free_ends)
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


class Static_Points:
    def __init__(self, tasks, map, cars, in_file, out_file):
        self.tasks = tasks
        self.map = map
        self.cars = cars
        self.future_tasks = []
        self.in_file = in_file
        self.out_file = out_file

        self.load_tasks()
        with open(f'{self.out_file}.csv', 'a') as fp:
            fp.write(f'task_id;start;end;in_time;assign_time;complete_time;car_id;is_VIP\n')

    def do_step(self, time):
        print(f'Tasks: {len(self.tasks)}')
        if len(self.tasks):
            print(f'Longest: {time - self.tasks[0].in_time}')
            if time - self.tasks[0].in_time >= 50:
                print(time)
                print('END')
                exit(0)

        while len(self.future_tasks) and self.future_tasks[0][0] == time:
            t = self.future_tasks.pop(0)
            new_task = Task(t[1], t[2], self.map, time, self.out_file)
            self.tasks.append(new_task)
        if len(self.future_tasks) == 0 and len(self.tasks) == 0:
            exit(0)

    def load_tasks(self):
        file1 = open(self.in_file, 'r')
        lines = file1.readlines()

        for line in lines[1:]:
            items = line.split(';')
            start = make_tuple(items[1])
            end = make_tuple(items[2])
            time = int(items[3])
            self.future_tasks.append((time, start, end))
        self.future_tasks.sort(key=lambda x: x[0])

class Task:

    def __init__(self, start, end, map):
        self.map = map
        self.task_id = self.map.task_id_max
        self.map.task_id_max += 1
        self.start = start
        self.end = end
        self.state = 'NEW'
        self.car_id = None

    def activate(self):
        self.map.map[self.start[0]][self.start[1]] = Task_Start(self.task_id, self)
        self.map.map[self.end[0]][self.end[1]] = Task_End(self.task_id, self)
        self.state = 'ACTIVATED'

    def assign(self, car_id):
        self.state = 'ASSIGNED'
        self.car_id = car_id

    def complete(self):
        self.state = 'COMPLETED'

class Task_Start:
    def __init__(self, task_id, parent):
        self.task_id = task_id
        self.parent = parent

    def get_color(self):
        return (0, 255, 0)  # green

    def is_empty(self, car):
        if car.current_task is None:
            car.current_task = self.task_id
            self.parent.assign(car.id)
            return True
        else:
            return False


class Task_End:
    def __init__(self, task_id, parent):
        self.task_id = task_id
        self.parent = parent

    def get_color(self):
        return (255, 0, 0)  # red

    def is_empty(self, car):
        if car.current_task == self.task_id:
            car.current_task = None
            self.parent.complete()
            return True
        else:
            return False

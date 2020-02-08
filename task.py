class Task:

    def __init__(self, start, end, map):
        self.map = map
        self.task_id = self.map.task_id_max
        self.map.task_id_max += 1

        self.map.map[start[0]][start[1]] = Task_Start(self.task_id)
        self.map.map[end[0]][end[1]] = Task_End(self.task_id)


class Task_Start:
    def __init__(self, task_id):
        self.task_id = task_id

    def get_color(self):
        return (0, 255, 0)  # green

    def is_empty(self, car):
        car.current_task = self.task_id
        return True


class Task_End:
    def __init__(self, task_id):
        self.task_id = task_id

    def get_color(self):
        return (255, 0, 0)  # red

    def is_empty(self, car):
        car.current_task = None
        return True

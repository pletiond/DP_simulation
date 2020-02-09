from map import *
from car import *
from task import *
from animation import *

map = Map(width=50, height=50)

map.add_route((2, 2), (2, 49))
map.add_route((10, 2), (10, 49))
map.add_route((20, 2), (20, 49))
map.add_route((30, 2), (30, 49))
map.add_route((40, 2), (40, 49))
map.add_route((49, 2), (49, 49))

map.add_route((2, 2), (49, 2))
map.add_route((2, 25), (49, 25))
map.add_route((2, 49), (49, 49))

car1 = Car((2, 2), map)
# car2 = Car((2, 3), map)

task1 = Task((5, 3), (35, 3), map)
task2 = Task((3, 8), (3, 35), map)
task3 = Task((35, 24), (5, 48), map)
task4 = Task((31, 10), (1, 25), map)
task5 = Task((48, 45), (19, 10), map)
task6 = Task((21, 42), (48, 10), map)

completed_tasks = []
tasks = [task1, task2, task3, task4, task5, task6]
cars = [car1]
ACTIVATED_TASKS = 6

for t in range(ACTIVATED_TASKS):
    tasks[t].activate()

animation = Animation(map, window_scale=12, objects=cars, tasks=tasks)


while True:
    if len(tasks) > 0 and tasks[0].state == 'COMPLETED':
        done = tasks.pop(0)
        completed_tasks.append(done)
        if len(tasks) > 0:
            tasks[0].activate()

    if not animation.update():
        break

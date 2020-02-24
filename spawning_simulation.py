from car import *
from task import *
from SingleCarController import *
from TokenPassing import *
from animation import *
from defined_maps import *

# map, tasks, cars = get_case_1()
map, tasks, cars, spawn_points = get_spawn_case1()

SPAWN_RATE = 10
WINDOW_SCALE = 15

completed_tasks = []
animation = Animation(map, window_scale=WINDOW_SCALE, objects=cars, tasks=tasks)

# single_car_controller = SingleCarController(cars[0], map, tasks)

TP = TokenPassing(cars, map, tasks)

while True:
    print(f'Tasks: {len(tasks)}')

    if TP.current_time % SPAWN_RATE == 0:
        spawn_points.create_task()

    if not animation.update():
        break

    animation.clock.tick(5)
    # i = input('Continue...')
    TP.do_step()
    spawn_points.refresh_spawn_points()
    while True:
        found = False
        for i in range(len(tasks)):
            if tasks[i].state == 'COMPLETED':
                tasks.pop(i)
                found = True
                break

        if not found:
            break

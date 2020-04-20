from Car import *
from task import *
from SingleCarController import *
from TP import *
from animation import *
from defined_maps import *

# map, tasks, cars = get_case_1()
map, tasks, cars = get_small_test_case1()  #

WINDOW_SCALE = 15

completed_tasks = []
animation = Animation(map, window_scale=WINDOW_SCALE, objects=cars, tasks=tasks)

# single_car_controller = SingleCarController(cars[0], map, tasks)

TP = TP(cars, map, tasks)

while True:
    #print(f'Tasks: {len(tasks)}')

    if not animation.update():
        break

    animation.clock.tick(5)
    #i = input('Continue...')
    TP.do_step()

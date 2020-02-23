from car import *
from task import *
from SingleCarController import *
from TokenPassing import *
from animation import *
from defined_maps import *

map, tasks, cars = get_case_1()


completed_tasks = []
ACTIVATED_TASKS = 6

for t in range(ACTIVATED_TASKS):
    tasks[t].activate()

animation = Animation(map, window_scale=13, objects=cars, tasks=tasks)

# single_car_controller = SingleCarController(cars[0], map, tasks)

TP = TokenPassing(cars, map, tasks)



while True:
    # if len(tasks) > 0 and tasks[0].state == 'COMPLETED':
    #    done = tasks.pop(0)
    #    completed_tasks.append(done)
    #    if len(tasks) > 0:
    #        tasks[0].activate()

    # if len(completed_tasks) >= ACTIVATED_TASKS - 2:
    #    reactivated_task = completed_tasks.pop(0)
    #    reactivated_task.activate()

    # if len(single_car_controller.tasks) > 0:
    # single_car_controller.do_step()
    #    TP.do_step()
    #    ...

    if not animation.update():
        break

    animation.clock.tick(5)

    TP.do_step()
    #i = input('Continue...')

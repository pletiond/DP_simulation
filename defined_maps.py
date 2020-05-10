from Central import *
from TP import *
from TPTS import *


def get_large_map1(tile_len, speed):
    width = 13
    height = 10
    map = Map(width=width, height=height)

    for i in range(1, width + 1, 4):
        map.add_route((1, i), (height + 1, i))
    for i in range(1, height + 2, 3):
        map.add_route((i, 0), (i, width + 1))

    cars = [Car((4, 3), map, tile_len, 'RIGHT', speed),
            Car((4, 4), map, tile_len, 'RIGHT', speed),
            Car((4, 5), map, tile_len, 'RIGHT', speed),
            Car((4, 6), map, tile_len, 'LEFT', speed),
            Car((7, 9), map, tile_len, 'UP', speed),
            Car((7, 9), map, tile_len, 'DOWN', speed),
            Car((7, 10), map, tile_len, 'LEFT', speed),
            Car((7, 11), map, tile_len, 'LEFT', speed),
            Car((9, 5), map, tile_len, 'UP', speed),
            Car((8, 5), map, tile_len, 'UP', speed), ]
    cars = []
    tasks = []
    max_cars = 0

    cars_points = [Car_Point(map, cars, (2, 3), tile_len, 8, speed),
                   Car_Point(map, cars, (2, 11), tile_len, 8, speed),
                   Car_Point(map, cars, (8, 3), tile_len, 8, speed),
                   Car_Point(map, cars, (8, 11), tile_len, 8, speed)
                   ]

    for c in cars_points:
        max_cars += c.cars_available

    central = Central(cars, map, tasks, cars_points)
    tp = TP(cars, map, tasks, cars_points)
    tpts = TPTS(cars, map, tasks, cars_points)

    solver = tp
    max_tasks = max_cars // 2

    spawn_points = Spawn_Points(tasks, map, [], max_tasks=max_tasks,
                                out_file=f'tests/05/{str(solver.__class__.__name__)}_a{max_cars}_t{max_tasks}')
    # static_points = Static_Points(tasks, map, [], in_file='inputs/Central_a8_t8.csv', out_file=f'tests/02/tmp_static_{str(solver.__class__.__name__)}_a{max_cars}_t{max_cars}')

    points = spawn_points

    return map, tasks, cars, points, cars_points, solver


def get_large_map2(tile_len, speed):
    width = 13
    height = 16
    map = Map(width=width, height=height)

    for i in range(1, width + 1, 4):
        map.add_route((1, i), (height + 1, i))
    for i in range(1, height + 2, 3):
        map.add_route((i, 0), (i, width + 1))

    cars = []
    tasks = []
    max_cars = 0

    cars_points = [Car_Point(map, cars, (2, 3), tile_len, 2, speed),
                   Car_Point(map, cars, (2, 11), tile_len, 2, speed),
                   Car_Point(map, cars, (8, 3), tile_len, 2, speed),
                   Car_Point(map, cars, (8, 11), tile_len, 2, speed),
                   Car_Point(map, cars, (14, 3), tile_len, 1, speed),
                   Car_Point(map, cars, (14, 11), tile_len, 1, speed)
                   ]

    for c in cars_points:
        max_cars += c.cars_available

    central = Central(cars, map, tasks, cars_points)
    tp = TP(cars, map, tasks, cars_points)
    tpts = TPTS(cars, map, tasks, cars_points)

    solver = central
    max_tasks = max_cars

    spawn_points = Spawn_Points(tasks, map, [], max_tasks=max_tasks,
                                out_file=f'tests/astar/{str(solver.__class__.__name__)}_c{max_cars}_t{max_tasks}')
    # static_points = Static_Points(tasks, map, [], in_file='tests/07/in2_Central.csv', out_file=f'tests/07/in_Central2_out2_VIP_{str(solver.__class__.__name__)}')

    points = spawn_points

    return map, tasks, cars, points, cars_points, solver

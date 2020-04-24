from Car import *
from task import *
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

    cars = []
    tasks = []
    max_cars = 0

    cars_points = [Car_Point(map, cars, (2, 3), tile_len, 2, speed),
                   Car_Point(map, cars, (2, 11), tile_len, 2, speed),
                   Car_Point(map, cars, (8, 3), tile_len, 2, speed),
                   Car_Point(map, cars, (8, 11), tile_len, 2, speed)
                   ]
    for c in cars_points:
        max_cars += c.cars_available

    central = Central(cars, map, tasks, cars_points)
    tp = TP(cars, map, tasks, cars_points)
    tpts = TPTS(cars, map, tasks, cars_points)

    solver = central

    # spawn_points = Spawn_Points(tasks, map, [], max_tasks=max_cars, out_file=f'tests/02/{str(solver.__class__.__name__)}_a{max_cars}_t{max_cars}')
    static_points = Static_Points(tasks, map, [], in_file='inputs/Central_a8_t8.csv',
                                  out_file=f'tests/02/static_{str(solver.__class__.__name__)}_a{max_cars}_t{max_cars}')

    points = static_points

    return map, tasks, cars, points, cars_points, solver

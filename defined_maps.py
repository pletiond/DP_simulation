from LCPD import *
from TP import *
from TPTS import *


def get_scenario1(tile_len, speed):
    # Map-------------
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

    # Cars-------------
    cars_points = [Car_Point(map, cars, (2, 3), tile_len, 4, speed),
                   Car_Point(map, cars, (2, 11), tile_len, 4, speed),
                   Car_Point(map, cars, (8, 3), tile_len, 4, speed),
                   Car_Point(map, cars, (8, 11), tile_len, 4, speed),
                   Car_Point(map, cars, (14, 3), tile_len, 4, speed),
                   Car_Point(map, cars, (14, 11), tile_len, 4, speed)
                   ]

    for c in cars_points:
        max_cars += c.cars_available

    # Algorithm-------------
    lcpd = LCPD(cars, map, tasks, cars_points)
    tp = TP(cars, map, tasks, cars_points)
    tpts = TPTS(cars, map, tasks, cars_points)

    solver = lcpd
    max_tasks = max_cars

    # Tasks-------------
    points = Spawn_Points(tasks, map, [], max_tasks=max_tasks,
                          out_file=f'results/tmp/{str(solver.__class__.__name__)}_c{max_cars}')
    # points = Static_Points(tasks, map, [], in_file='results/09/big.csv', out_file=f'results/09/{str(solver.__class__.__name__)}_c{max_cars}_static_big')

    return map, tasks, cars, points, cars_points, solver

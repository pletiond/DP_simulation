from Car import *
from task import *

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

    cars_points = [Car_Point(map, (2, 3), tile_len, 2, speed),
                   Car_Point(map, (2, 11), tile_len, 2, speed),
                   Car_Point(map, (8, 3), tile_len, 2, speed),
                   Car_Point(map, (8, 11), tile_len, 2, speed)
                   ]
    for c in cars_points:
        max_cars += c.cars_available
    spawn_points = Spawn_Points(tasks, map, [], max_cars)

    return map, tasks, cars, spawn_points, cars_points

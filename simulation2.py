from Visualization import *
from defined_maps import *
from Central import *
from TP import *

tile_len = 50
speed = 50
ticks = 50

map, tasks, cars, spawn_points, cars_points = get_large_map1(tile_len, speed)

central = Central(cars, map, tasks, cars_points)
tp = TokenPassing(cars, map, tasks, cars_points)
vis = Visualization(map.to_bitman_objects(), tile_len, cars=cars, ticks=ticks, spawn_points=spawn_points,
                    cars_points=cars_points,
                    solver=tp)

vis.run()

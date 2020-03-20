from Visualization import *
from defined_maps import *
from Central import *

tile_len = 60
speed = 50
ticks = 50

map, tasks, cars, spawn_points = get_large_map1(tile_len, speed)

central = Central(cars, map, tasks)
vis = Visualization(map.to_bitman_objects(), tile_len, cars=cars, ticks=ticks, spawn_points=spawn_points,
                    solver=central)

vis.run()

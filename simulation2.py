from Visualization import *
from defined_maps import *

tile_len = 50
speed = 10
ticks = 10

map, tasks, cars, spawn_points, cars_points, solver = get_large_map2(tile_len, speed)

vis = Visualization(map.to_bitman_objects(), tile_len, cars=cars, ticks=ticks, spawn_points=spawn_points,
                    cars_points=cars_points,
                    solver=solver)

vis.run()

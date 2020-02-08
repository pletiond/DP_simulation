from map import *
from car import *
from task import *
from animation import *

map = Map(width=50, height=50)

map.add_route((2, 2), (2, 49))
map.add_route((10, 2), (10, 49))
map.add_route((20, 2), (20, 49))
map.add_route((30, 2), (30, 49))
map.add_route((40, 2), (40, 49))
map.add_route((49, 2), (49, 49))

map.add_route((2, 2), (49, 2))
map.add_route((2, 25), (49, 25))
map.add_route((2, 49), (49, 49))

car1 = Car((2, 2), map)

task1 = Task((5, 3), (35, 3), map)

animation = Animation(map, window_scale=12, objects=[car1])

while True:
    if not animation.update():
        break

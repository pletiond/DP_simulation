from car import *
from task import *


def get_small_test_case1():
    map = Map(width=5, height=5)
    map.add_route((2, 3), (4, 3))

    map.add_route((2, 2), (2, 4))
    map.add_route((4, 2), (4, 4))

    car1 = Car((2, 3), map)
    car2 = Car((4, 3), map)

    task1 = Task((2, 2), (4, 2), map)
    task1.activate()
    task2 = Task((4, 4), (2, 4), map)
    task2.activate()

    tasks = [task1, task2]
    cars = [car1, car2]

    return map, tasks, cars


def get_case_1():
    map = Map(width=75, height=50)

    map.add_route((2, 2), (2, 74))
    map.add_route((10, 2), (10, 74))
    map.add_route((20, 2), (20, 74))
    map.add_route((30, 2), (30, 74))
    map.add_route((40, 2), (40, 74))
    map.add_route((49, 2), (49, 74))

    map.add_route((2, 2), (49, 2))
    map.add_route((2, 25), (49, 25))
    map.add_route((2, 49), (49, 49))
    map.add_route((2, 74), (49, 74))

    car1 = Car((2, 2), map)
    car2 = Car((2, 3), map)

    task1 = Task((5, 3), (35, 3), map)
    task2 = Task((3, 8), (3, 35), map)
    task3 = Task((35, 24), (5, 48), map)
    task4 = Task((31, 10), (1, 25), map)
    task5 = Task((48, 45), (19, 10), map)
    task6 = Task((21, 42), (48, 10), map)

    tasks = [task1, task2, task3, task4, task5, task6]
    cars = [car1, car2]

    return map, tasks, cars


def get_spawn_case1():
    map = Map(width=75, height=50)

    map.add_route((2, 2), (2, 74))
    map.add_route((10, 2), (10, 74))
    map.add_route((20, 2), (20, 74))
    map.add_route((30, 2), (30, 74))
    map.add_route((40, 2), (40, 74))
    map.add_route((49, 2), (49, 74))

    map.add_route((2, 2), (49, 2))
    map.add_route((2, 25), (49, 25))
    map.add_route((2, 49), (49, 49))
    map.add_route((2, 74), (49, 74))

    car1 = Car((2, 1), map)
    car2 = Car((2, 75), map)
    car3 = Car((49, 75), map)
    car4 = Car((49, 1), map)
    car5 = Car((1, 25), map)
    car6 = Car((1, 49), map)
    car7 = Car((50, 25), map)
    car8 = Car((50, 49), map)
    cars = [car1, car2, car3, car4, car5, car6, car7, car8]

    tasks = []

    spawn_points = Spawn_Points(tasks, map, cars)
    spawn_points.add_spawn_point((3, 10), 1)
    spawn_points.add_spawn_point((3, 18), 1)
    spawn_points.add_spawn_point((11, 10), 1)
    spawn_points.add_spawn_point((11, 18), 1)
    spawn_points.add_spawn_point((21, 10), 1)
    spawn_points.add_spawn_point((21, 18), 1)
    spawn_points.add_spawn_point((31, 10), 1)
    spawn_points.add_spawn_point((31, 18), 1)
    spawn_points.add_spawn_point((41, 10), 1)
    spawn_points.add_spawn_point((41, 18), 1)

    spawn_points.add_spawn_point((3, 33), 1)
    spawn_points.add_spawn_point((3, 41), 1)
    spawn_points.add_spawn_point((11, 33), 1)
    spawn_points.add_spawn_point((11, 41), 1)
    spawn_points.add_spawn_point((21, 33), 1)
    spawn_points.add_spawn_point((21, 41), 1)
    spawn_points.add_spawn_point((31, 33), 1)
    spawn_points.add_spawn_point((31, 41), 1)
    spawn_points.add_spawn_point((41, 33), 1)
    spawn_points.add_spawn_point((41, 41), 1)

    spawn_points.add_spawn_point((3, 57), 1)
    spawn_points.add_spawn_point((3, 65), 1)
    spawn_points.add_spawn_point((11, 57), 1)
    spawn_points.add_spawn_point((11, 65), 1)
    spawn_points.add_spawn_point((21, 57), 1)
    spawn_points.add_spawn_point((21, 65), 1)
    spawn_points.add_spawn_point((31, 57), 1)
    spawn_points.add_spawn_point((31, 65), 1)
    spawn_points.add_spawn_point((41, 57), 1)
    spawn_points.add_spawn_point((41, 65), 1)

    spawn_points.add_spawn_point((2, 1), 1)
    spawn_points.add_spawn_point((2, 75), 1)
    spawn_points.add_spawn_point((49, 75), 1)
    spawn_points.add_spawn_point((49, 1), 1)
    spawn_points.add_spawn_point((1, 25), 1)
    spawn_points.add_spawn_point((1, 49), 1)
    spawn_points.add_spawn_point((50, 25), 1)
    spawn_points.add_spawn_point((50, 49), 1)

    return map, tasks, cars, spawn_points


def get_small_spawn_case1():
    map = Map(width=7, height=7)
    map.add_route((2, 2), (6, 2))
    map.add_route((2, 4), (6, 4))
    map.add_route((2, 6), (6, 6))

    map.add_route((2, 2), (2, 6))
    map.add_route((6, 2), (6, 6))

    car1 = Car((1, 2), map)
    car2 = Car((7, 6), map)
    cars = [car1, car2]

    tasks = []
    spawn_points = Spawn_Points(tasks, map, cars)
    spawn_points.add_spawn_point((2, 1), 1)
    spawn_points.add_spawn_point((6, 7), 1)
    spawn_points.add_spawn_point((2, 7), 1)
    spawn_points.add_spawn_point((6, 1), 1)
    spawn_points.add_spawn_point((1, 4), 1)
    spawn_points.add_spawn_point((7, 4), 1)
    spawn_points.add_spawn_point((1, 2), 1)
    spawn_points.add_spawn_point((7, 6), 1)

    return map, tasks, cars, spawn_points

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
    task2 = Task((4, 4), (2, 4), map)

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

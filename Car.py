from map import *
import numpy as np
import math
import pygame

orientations = ['LEFT', 'UP', 'RIGHT', 'DOWN']


class Car:

    def __init__(self, start_location, map, tile_len, orientation, speed):
        self.x = start_location[1]
        self.y = start_location[0]
        self.map = map
        # self.map.map[self.y][self.x] = self
        self.possible_task = None
        self.current_task = None
        self.id = self.map.car_id_max
        self.map.car_id_max += 1

        size = (tile_len * 0.7, tile_len * 0.3)
        self.tile_len = tile_len
        self.image = pygame.Surface(size)
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, tile_len * 0.7, tile_len * 0.3))
        pygame.draw.line(self.image, (255, 255, 0), (size[0] * 0.9, 0), (size[0] * 0.9, size[1]), 5)
        self.image.set_colorkey(0)
        self.speed = speed
        self.buffer = []
        self.orientation = orientations.index(orientation)

        if orientation == 'RIGHT':
            self.pos = [(self.x - 1) * tile_len + 0.2 * tile_len, (self.y - 1) * tile_len + tile_len * 0.68]
            self.angle = 0
        elif orientation == 'LEFT':
            self.pos = [(self.x - 1) * tile_len + 0.8 * tile_len, (self.y - 1) * tile_len + tile_len * 0.33]
            self.angle = 180
        elif orientation == 'UP':
            self.pos = [(self.x - 1) * tile_len + 0.68 * tile_len, (self.y - 1) * tile_len + tile_len * 0.8]
            self.angle = 90
        elif orientation == 'DOWN':
            self.pos = [(self.x - 1) * tile_len + 0.33 * tile_len, (self.y - 1) * tile_len + tile_len * 0.2]
            self.angle = 270

        self.w, self.h = self.image.get_size()
        self.steps_to_goal = []

    def go_up(self):
        self.y -= 1
        # turn_round = self.map.check_point(self)
        if self.orientation == 0:
            self.go_right_vis()
        elif self.orientation == 1:
            self.go_step_straight_vis()
        elif self.orientation == 2:
            self.go_left_vis()
        else:
            print('ERROR!------------')


    def go_down(self):
        self.y += 1
        # turn_round = self.map.check_point(self)
        if self.orientation == 0:
            self.go_left_vis()
        elif self.orientation == 1:
            print('ERROR!------------')
        elif self.orientation == 2:
            self.go_right_vis()
        else:
            self.go_step_straight_vis()


    def go_right(self):
        self.x += 1
        # turn_round = self.map.check_point(self)
        if self.orientation == 0:
            print('ERROR!------------')
        elif self.orientation == 1:
            self.go_right_vis()
        elif self.orientation == 2:
            self.go_step_straight_vis()
        else:
            self.go_left_vis()


    def go_left(self):
        self.x -= 1
        # turn_round = self.map.check_point(self)
        if self.orientation == 0:
            self.go_step_straight_vis()
        elif self.orientation == 1:
            self.go_left_vis()
        elif self.orientation == 2:
            print('ERROR!------------')
        else:
            self.go_right_vis()


    def get_color(self):
        if self.current_task is None:
            return (255, 247, 0)  # YELLOW
        else:
            return (0, 188, 255)  # ORANGE

    def is_empty(self, car=None):
        return False

    def is_agent(self):
        return True

    def move(self, distance=1):
        x = int(math.cos(math.radians(self.angle)) * 100)
        y = int(math.sin(math.radians(self.angle)) * 100)

        self.pos[0] += (x / 100) * distance
        self.pos[1] += (-y / 100) * distance

    def turn(self, angle):
        self.angle += angle
        self.angle %= 360

    def draw(self, screen):
        self.blitRotate(screen, self.image.copy(), self.pos, (self.w // 2, self.h // 2), self.angle)

    def blitRotate(self, surf, image, pos, originPos, angle):
        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
            pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        # rotate and blit the image
        surf.blit(rotated_image, origin)

    def do_step(self):
        if len(self.steps_to_goal) == 0 and len(self.buffer) == 0:
            return

        if len(self.steps_to_goal) == 0:
            self.correct_position()
            next = self.buffer.pop(0)

            if next == 'LEFT':
                self.go_left_vis()
            elif next == 'STRAIGHT':
                self.go_step_straight_vis()
            elif next == 'RIGHT':
                self.go_right_vis()
            elif next == 'TURN_ROUND':
                self.turn_round()
                self.do_step()
                return

        step = self.steps_to_goal.pop(0)
        self.angle += step[1]
        self.move(step[0])

    def go_step_straight_vis(self):

        if len(self.steps_to_goal) > 0:
            self.buffer.append('STRAIGHT')
            return

        for i in range(self.speed):
            self.steps_to_goal.append((self.tile_len / self.speed, 0))

    def go_left_vis(self):
        if len(self.steps_to_goal) > 0:
            self.buffer.append('LEFT')
            return
        self.orientation = (self.orientation - 1) % 4
        self.steps_to_goal.append((self.tile_len / self.speed, 40))
        for i in range(self.speed // 2):
            # if i == steps:
            #    self.steps_to_goal.append((0, 90))

            self.steps_to_goal.append((self.tile_len * 0.6 / (self.speed // 2), 0))

        self.steps_to_goal.append((0, 50))
        remain = self.speed - 1 - self.speed // 2
        for i in range(remain):
            self.steps_to_goal.append((self.tile_len * 0.52 / remain, 0))

    def go_right_vis(self):
        if len(self.steps_to_goal) > 0:
            self.buffer.append('RIGHT')
            return
        self.orientation = (self.orientation + 1) % 4
        self.steps_to_goal.append((self.tile_len / self.speed, -50))
        for i in range(self.speed // 2):
            self.steps_to_goal.append((self.tile_len * 0.19 / (self.speed // 2), 0))

        self.steps_to_goal.append((0, -40))
        remain = self.speed - 1 - self.speed // 2
        for i in range(remain):
            self.steps_to_goal.append((self.tile_len * 0.38 / remain, 0))

    def correct_position(self):
        x = int(self.pos[0] // self.tile_len)
        y = int(self.pos[1] // self.tile_len)

        if self.orientation == 0:
            x_plus = 0.8
            y_plus = 0.33
        elif self.orientation == 1:
            x_plus = 0.68
            y_plus = 0.8
        elif self.orientation == 2:
            x_plus = 0.2
            y_plus = 0.68
        else:
            x_plus = 0.33
            y_plus = 0.2
        self.pos = [x * self.tile_len + x_plus * self.tile_len, y * self.tile_len + y_plus * self.tile_len]

    def turn_round(self):
        print('TURN ROUND')
        self.angle += 180
        self.angle %= 360
        self.orientation += 2
        self.orientation %= 4
        self.correct_position()

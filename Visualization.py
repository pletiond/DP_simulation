from Road_Tiles import *
import math

decode_dict = {
    '1010': Straight_Horizontally,
    '0101': Straight_Vertically,
    '1001': Turn_Right_Down,
    '1100': Turn_Left_Down,
    '0011': Turn_Right_Up,
    '0110': Turn_Left_Up,
    '1000': T_down,
    '0000': X_crossroads,
    '0010': T_up
}
orientations = ['LEFT', 'UP', 'RIGHT', 'DOWN']


class Vis_Car:
    def __init__(self, position, tile_len, orientation, speed):
        size = (tile_len * 0.7, tile_len * 0.3)
        self.tile_len = tile_len
        self.image = pygame.Surface(size)
        pygame.draw.rect(self.image, (0, 255, 255), (0, 0, tile_len * 0.7, tile_len * 0.3))
        pygame.draw.line(self.image, (255, 0, 0), (size[0] * 0.9, 0), (size[0] * 0.9, size[1]), 5)
        self.image.set_colorkey(0)
        self.speed = speed
        self.buffer = []
        self.orientation = orientations.index(orientation)

        if orientation == 'RIGHT':
            self.pos = [position[1] * tile_len + 0.2 * tile_len, position[0] * tile_len + tile_len * 0.68]
            self.angle = 0
        elif orientation == 'LEFT':
            self.pos = [position[1] * tile_len + 0.8 * tile_len, position[0] * tile_len + tile_len * 0.33]
            self.angle = 180
        elif orientation == 'UP':
            self.pos = [position[1] * tile_len + 0.68 * tile_len, position[0] * tile_len + tile_len * 0.8]
            self.angle = 90
        elif orientation == 'DOWN':
            self.pos = [position[1] * tile_len + 0.68 * tile_len, position[0] * tile_len + tile_len * 0.2]
            self.angle = 270

        self.w, self.h = self.image.get_size()
        self.steps_to_goal = []

    def move(self, distance=1):
        x = int(math.cos(math.radians(self.angle)) * 100)
        y = int(math.sin(math.radians(self.angle)) * 100)

        self.pos[0] += (x / 100) * distance
        self.pos[1] += (-y / 100) * distance

    def turn(self, angle):
        self.angle += angle
        self.angle %= 360

        x = int(math.cos(math.radians(self.angle)) * 100)
        y = int(math.sin(math.radians(self.angle)) * 100)
        # print(f'{self.angle} - {int(x)}  {int(y)}')

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
            print(next)
            if next == 'LEFT':
                self.go_left()
            elif next == 'STRAIGHT':
                self.go_step_straight()
            elif next == 'RIGHT':
                self.go_right()

        # print(self.pos)

        step = self.steps_to_goal.pop(0)
        self.angle += step[1]
        self.move(step[0])

    def go_step_straight(self):

        if len(self.steps_to_goal) > 0:
            self.buffer.append('STRAIGHT')
            return
        print(orientations[self.orientation])
        for i in range(self.speed):
            self.steps_to_goal.append((self.tile_len / self.speed, 0))

    def go_left(self):
        if len(self.steps_to_goal) > 0:
            self.buffer.append('LEFT')
            return
        self.orientation = (self.orientation - 1) % 4
        print(orientations[self.orientation])
        self.steps_to_goal.append((self.tile_len / self.speed, 40))
        for i in range(self.speed // 2):
            # if i == steps:
            #    self.steps_to_goal.append((0, 90))

            self.steps_to_goal.append((self.tile_len * 0.6 / (self.speed // 2), 0))

        self.steps_to_goal.append((0, 50))
        remain = self.speed - 1 - self.speed // 2
        for i in range(remain):
            self.steps_to_goal.append((self.tile_len * 0.52 / remain, 0))

    def go_right(self):
        if len(self.steps_to_goal) > 0:
            self.buffer.append('RIGHT')
            return
        self.orientation = (self.orientation + 1) % 4
        print(orientations[self.orientation])
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
        print(f'{x}  {y}')
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
        self.pos = [x * self.tile_len + x_plus * tile_len, y * self.tile_len + y_plus * tile_len]


class Visualization:

    def __init__(self, map, tile_len, cars):
        self.map = map
        self.cars = cars
        self.tile_len = tile_len
        self.vis_map = []
        self.width = len(self.map[0]) * tile_len
        self.height = len(self.map) * tile_len

        self.map_to_graphics()

        pygame.init()
        pygame.display.set_caption("Simulation")
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()

    def map_to_graphics(self):
        for row in range(len(self.map)):
            vis_row = []
            for column in range(len(self.map[row])):
                if self.map[row][column] == 1:
                    vis_row.append(
                        Block_Wall((row * self.tile_len, column * self.tile_len), self.tile_len))  # APPEND WALL
                    continue
                code = self.encode_tile(row, column)
                tile = self.decode_tile(code)((row * self.tile_len, column * self.tile_len), self.tile_len)
                vis_row.append(tile)
                print(code)

            self.vis_map.append(vis_row)

    def encode_tile(self, row, column):
        code = ''
        # TOP
        if row == 0:
            code += '1'
        else:
            code += str(self.map[row - 1][column])
        # RIGHT
        if column + 1 == len(self.map[row]):
            code += '1'
        else:
            code += str(self.map[row][column + 1])
        # DOWN
        if row + 1 == len(self.map):
            code += '1'
        else:
            code += str(self.map[row + 1][column])
        # LEFT
        if column == 0:
            code += '1'
        else:
            code += str(self.map[row][column - 1])
        return code

    def decode_tile(self, code):
        if code not in decode_dict.keys():
            return Block_Wall
        return decode_dict[code]

    def draw_world(self):
        for row in self.vis_map:
            for tile in row:
                tile.draw(self.screen)

    def run(self):
        steps = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break
                elif event.type == pygame.QUIT:
                    break

            key = pygame.key.get_pressed()
            dist = 1
            if key[pygame.K_LEFT]:
                car.turn(10)
            if key[pygame.K_RIGHT]:
                car.turn(-10)
            if key[pygame.K_UP]:
                car.move()

            self.screen.fill(0)
            self.draw_world()
            for car in self.cars:
                car.draw(self.screen)

            for car in self.cars:
                car.do_step()

            steps += 1
            # print(steps)
            pygame.display.flip()
            # pygame.display.update()
            self.clock.tick(30)


test_map = [[0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]]
tile_len = 100
speed = 50
# position = [100 + 0.5 * tile_len, 0 + 0.68 * tile_len]

car = Vis_Car((2, 0), tile_len, 'UP', speed)
car2 = Vis_Car((2, 0), tile_len, 'RIGHT', speed)
car3 = Vis_Car((1, 0), tile_len, 'UP', speed)
car4 = Vis_Car((0, 1), tile_len, 'LEFT', speed)
cars = [car4, car3]

vis = Visualization(test_map, tile_len, cars=cars)

for i in range(10):
    car4.go_step_straight()
    car4.go_left()
    car3.go_step_straight()
    car3.go_right()

# car3.go_step_straight()
# car3.go_right()
# car3.go_step_straight()
# car3.go_right()
vis.run()

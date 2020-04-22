from Road_Tiles import *

decode_dict = {
    '1010': Straight_Horizontally,
    '0101': Straight_Vertically,
    '1001': Turn_Right_Down,
    '1100': Turn_Left_Down,
    '0011': Turn_Right_Up,
    '0110': Turn_Left_Up,
    '1000': T_down,
    '0000': X_crossroads,
    '0010': T_up,
    '0001': T_right,
    '0100': T_left
}
orientations = ['LEFT', 'UP', 'RIGHT', 'DOWN']


class Visualization:

    def __init__(self, in_map, tile_len, cars, ticks, spawn_points, cars_points, solver):
        self.map = []

        for i in range(len(in_map)):
            tmp = []
            for j in range(len(in_map[0])):
                if i == 0 or j == 0 or i == len(in_map) - 1 or j == len(in_map[0]) - 1:
                    continue
                tmp.append(in_map[i][j])
            if len(tmp) == 0:
                continue
            self.map.append(tmp)
        for cp in cars_points:
            loc = cp.location
            self.map[loc[0] - 1][loc[1] - 1] = 0
        for i in self.map:
            print(i)

        self.solver = solver
        self.spawn_points = spawn_points
        self.cars_points = cars_points
        self.cars = cars
        self.tile_len = tile_len
        self.vis_map = []
        self.width = len(self.map[0]) * tile_len
        self.height = len(self.map) * tile_len
        self.ticks = ticks

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

            self.vis_map.append(vis_row)
        # for s in self.spawn_points.points:
        #    pos = s[0]
        #    new_pos = (pos[0] -1, pos[1] -1)
        #    self.vis_map[pos[0]-1][pos[1]-1] = Task_Down((new_pos[0] * self.tile_len, new_pos[1] * self.tile_len), self.tile_len)

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
        self.screen.fill((255, 255, 255))
        self.draw_world()
        for cp in self.cars_points:
            cp.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.ticks)
        auto = False
        while True:

            if steps % self.ticks == 0:
                while True:
                    end = False

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                end = True
                            if event.key == pygame.K_UP:
                                auto = True
                            if event.key == pygame.K_DOWN:
                                auto = False
                    if end or auto:
                        break

                while len(self.spawn_points.tasks) < self.spawn_points.max_cars - 2:
                    self.spawn_points.create_task(steps / self.ticks)

                self.solver.do_step()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break
                elif event.type == pygame.QUIT:
                    break

            self.screen.fill((255, 255, 255))
            self.draw_world()
            for cp in self.cars_points:
                cp.draw(self.screen)

            for car in self.cars:
                car.draw(self.screen)

            for car in self.cars:
                car.do_step()

            steps += 1
            pygame.display.flip()

            # pygame.display.update()
            self.clock.tick(self.ticks)

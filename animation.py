import pygame


class Animation:

    def __init__(self, map, window_scale, objects, tasks):
        pygame.init()
        self.objects = objects
        self.map = map
        self.tasks = tasks
        self.window_scale = window_scale
        self.window_size = [window_scale * self.map.width, window_scale * self.map.height]
        self.screen = pygame.display.set_mode(self.window_size)
        self.myFont = pygame.font.SysFont('Helvetica', self.window_scale)

        pygame.display.set_caption("Simulation")

        self.clock = pygame.time.Clock()

        self.colors = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255), 'GREEN': (0, 255, 0), 'RED': (255, 0, 0),
                       'GREY': (116, 111, 110), 'ORANGE': (231, 95, 67), 'YELLOW': (255, 247, 0)}

    def end(self):
        pygame.quit()

    def draw_map(self):
        for row in range(1, self.map.height + 1):
            for column in range(1, self.map.width + 1):
                color = self.map.map[row][column].get_color()
                pygame.draw.rect(self.screen,
                                 color,
                                 [(self.window_scale) * (column - 1),
                                  (self.window_scale) * (row - 1),
                                  self.window_scale,
                                  self.window_scale])

    def draw_cars(self):
        for car in self.objects:
            color = car.get_color()
            pygame.draw.rect(self.screen,
                             color,
                             [(self.window_scale) * (car.x - 1),
                              (self.window_scale) * (car.y - 1),
                              self.window_scale,
                              self.window_scale])

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end()
                    return False
                elif event.key == pygame.K_DOWN:
                    self.objects[0].go_down()
                elif event.key == pygame.K_UP:
                    self.objects[0].go_up()
                elif event.key == pygame.K_RIGHT:
                    self.objects[0].go_right()
                elif event.key == pygame.K_LEFT:
                    self.objects[0].go_left()

            elif event.type == pygame.QUIT:
                self.end()
                return False

        self.draw_map()
        self.draw_cars()
        self.print_labels()
        pygame.display.flip()
        return True

    def print_labels(self):
        for task in self.tasks:
            if task.state == 'NEW' or task.state == 'COMPLETED':
                continue
            task_id = self.myFont.render(str(task.task_id), 1, (0, 0, 0))
            if not task.state == 'ASSIGNED':
                start_loc = ((task.start[1] - 1) * self.window_scale + 0.3 * self.window_scale,
                             (task.start[0] - 1) * self.window_scale)
                self.screen.blit(task_id, start_loc)

            end_loc = (
                (task.end[1] - 1) * self.window_scale + 0.3 * self.window_scale, (task.end[0] - 1) * self.window_scale)
            self.screen.blit(task_id, end_loc)

        for car in self.objects:
            object_id = self.myFont.render('C' + str(car.id - 10), 1, (0, 0, 0))
            loc = ((car.x - 1) * self.window_scale + 0.0 * self.window_scale, (car.y - 1) * self.window_scale)
            self.screen.blit(object_id, loc)

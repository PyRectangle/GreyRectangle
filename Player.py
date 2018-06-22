from Render import Render
import pygame


class Player():
    def __init__(self, window):
        self.WIDTH = 50
        self.HEIGHT = 100
        self.UP = 0
        self.DOWN = 1
        self.RIGHT = 2
        self.LEFT = 3
        self.COLOR = (150, 150, 150)

        self.X_ON_SCREEN = window.surface.get_width() / 2 - self.WIDTH / 2
        self.Y_ON_SCREEN = window.surface.get_height() / 2 - self.HEIGHT / 2
        
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.surface.fill(self.COLOR)

        self.x = 0
        self.y = 0
        
        self.jump_time = 10
        self.jump_height = 127
        self.jump_active = False
        self.jump_count = 0
        
        self.player_render = Render()
        
        self.window = window
    
    def jump(self):
        self.jump_active = True
        self.last_jump_dist = 0
        self.jump_dist = self.jump_height - 3
           
    def jump_update(self, main):
        self.jump_dist /= 2
        self.jump_dist += self.last_jump_dist
        self.last_jump_dist = self.jump_dist - int(self.jump_dist)
        self.move((self.UP, ), self.jump_dist, True, main)
 
        if int(self.jump_dist) == 0:
            self.jump_active = False

    def make_movements(self, physics, main):
        if physics:
            if main.window.get_key_press(main.pg.K_SPACE) and self.check_collisions(self.DOWN, main) and not self.jump_active:
                self.jump()
     
            if self.jump_active:
                self.jump_update(main)
            else:
                self.move((self.DOWN, ), main.speed * 2, True, main)
        else:
            if main.window.get_key_press(main.pg.K_DOWN):
                self.move((self.DOWN, ), main.speed, True, main)
            if main.window.get_key_press(main.pg.K_UP):
                self.move((self.UP, ), main.speed, True, main)

        if main.window.get_key_press(main.pg.K_RIGHT):
            self.move((self.RIGHT, ), main.speed, True, main)
        if main.window.get_key_press(main.pg.K_LEFT):
            self.move((self.LEFT, ), main.speed, True, main)
    
    def check_collisions(self, direction, main):
        real_x = self.x + self.X_ON_SCREEN
        real_y = self.y + self.Y_ON_SCREEN
   
        point_list = [] 
        if direction == self.UP:
            point_list.append([real_x, real_y - 1])
            point_list.append([real_x + self.WIDTH - 1, real_y - 1])
        if direction == self.DOWN:
            point_list.append([real_x, real_y + self.HEIGHT])
            point_list.append([real_x + self.WIDTH - 1, real_y + self.HEIGHT])
        if direction == self.RIGHT:
            point_list.append([real_x + self.WIDTH, real_y])
            point_list.append([real_x + self.WIDTH, real_y + self.HEIGHT / 2])
            point_list.append([real_x + self.WIDTH, real_y + self.HEIGHT - 1])
        if direction == self.LEFT:
            point_list.append([real_x - 1, real_y])
            point_list.append([real_x - 1, real_y + self.HEIGHT / 2])
            point_list.append([real_x - 1, real_y + self.HEIGHT - 1])
       
        for point in point_list:
            array_pos = int(point[1] / self.player_render.BLOCKWIDTH), int(point[0] / self.player_render.BLOCKWIDTH)
            try:
                if main.block.blocks[main.opened_section.region[array_pos[0]][array_pos[1]]].solid or point[0] < 0 or point[1] < 0:
                    return True
            except IndexError:
                return True
        return False
    
    def move(self, direction, dist, check_collisions, main):
        last_direction = None

        for direct in direction:
            if last_direction == direct:
                return
            last_direction = direct
            collide = False
        
            for i in range(int(dist)):
                if check_collisions:
                    collide = self.check_collisions(direct, main)
         
                if not collide:
                    if direct == self.UP:
                        self.y -= 1
                    if direct == self.DOWN:
                        self.y += 1
                    if direct == self.RIGHT:
                        self.x += 1
                    if direct == self.LEFT:
                        self.x -= 1

    def render(self):
        self.window.surface.blit(self.surface, (self.X_ON_SCREEN, self.Y_ON_SCREEN))

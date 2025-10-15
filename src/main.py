import pygame as pg

class Robotin:
    
    def __init__(self):
        pg.init()

        self.tile_size = 40
        self.width = 20 * self.tile_size  
        self.height = 15 * self.tile_size 

        self.new_game()

        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Saltarin")
        
        self.clock = pg.time.Clock()
        self.main_loop()

    def world(self):

        # here i took a lot of help from https://www.youtube.com/@CodingWithRuss
        self.tile_list = []
        self.monsters = []
        self.coins = []
        self.moving = []
        self.doors = []
        self.lava = []


        monster = pg.image.load("monster.png")
        self.monster = pg.transform.scale(monster,(40,40))

        coin = pg.image.load("coin.png")
        self.coin = pg.transform.scale(coin,(40,40))

        door = pg.image.load("door.png")
        self.door = pg.transform.scale(door,(60,131))

        border = pg.Surface((40, 40))
        border.fill((160, 160, 160))

        bottom = pg.Surface((40, 35))
        bottom.fill((153, 76, 0))

        top = pg.Surface((40, 5))
        top.fill((102, 204, 0))

        row_count = 0
        for row in self.map:
            col_count = 0
            for tile in row:

                x = col_count * self.tile_size
                y = row_count * self.tile_size

                if tile == 1:
                    img = pg.transform.scale(border, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img_bottom = pg.transform.scale(bottom, (self.tile_size, 35))
                    rect_bottom = img_bottom.get_rect(topleft=(x, y + 5)) 
                    self.tile_list.append((img_bottom, rect_bottom))
                    
                    img_top = pg.transform.scale(top, (self.tile_size, 5))
                    rect_top = img_top.get_rect(topleft=(x, y))  
                    self.tile_list.append((img_top, rect_top))

                if tile == 4:
                    monster_rect = self.monster.get_rect()
                    monster_rect.x = col_count * self.tile_size
                    monster_rect.y = row_count * self.tile_size
                    tile = (self.monster, monster_rect)
                    self.monsters.append(tile)
                
                if tile == 5:
                    coin_rect = self.coin.get_rect()
                    coin_rect.x = col_count * self.tile_size
                    coin_rect.y = row_count * self.tile_size
                    tile = (self.coin, coin_rect)
                    self.coins.append(tile)
                
                if tile == 6:
                    door_rect = self.door.get_rect()
                    door_rect.x = col_count * self.tile_size
                    door_rect.y = row_count * self.tile_size
                    tile = (self.door, door_rect)
                    self.doors.append(tile)

                if tile == 7:
                    img_bottom = pg.transform.scale(bottom, (self.tile_size, self.tile_size))
                    rect_bottom = img_bottom.get_rect()
                    rect_bottom.x = col_count * self.tile_size
                    rect_bottom.y = row_count * self.tile_size
                    tile = (img_bottom, rect_bottom)
                    self.moving.append(tile)


                col_count += 1
            row_count += 1
    
    def draw_world(self):
        for tile in self.tile_list:
            self.window.blit(tile[0], tile[1])
            #pg.draw.rect(self.window,(255, 255, 255), tile[1], 2)
        for monster in self.monsters:
            self.window.blit(monster[0], monster[1])
            #pg.draw.rect(self.window,(255, 255, 255), monster[1], 2)
        for coin in self.coins:
            self.window.blit(coin[0], coin[1])
            #pg.draw.rect(self.window,(255, 255, 255), coin[1], 2)
        for m in self.moving:
            self.window.blit(m[0], m[1])
            #pg.draw.rect(self.window,(255, 255, 255), coin[1], 2)
        for d in self.doors:
            self.window.blit(d[0], d[1])
            #pg.draw.rect(self.window,(255, 255, 255), coin[1], 2)


    def new_player(self, x, y):
        robot = pg.image.load("robot.png")
        self.player = pg.transform.scale(robot, (30,60))
        self.player_rect = self.player.get_rect()
        self.player_rect.x = x
        self.player_rect.y = y         

    def p_movement(self):
        x = 0
        y = 0

        for monster, monster_rect in self.monsters:
            self.m_c += 0.5
            monster_rect.x += self.m_v
            if self.m_c > 120:
                self.m_v *= -1
                self.m_c = 0
        
        for moving, moving_rect in self.moving:
            self.b_c += 0.5
            moving_rect.y += self.b_v
            if self.b_c > 40:
                self.b_v *= -1
                self.b_c = 0


        if self.right:
            x += 2.5
        if self.left:
            x -= 2.5

        if self.up and self.grav == 0:
            self.grav = -9
            self.up = False

        self.grav += 0.4
        if self.grav > 6:
            self.grav = 6
        y += self.grav

    
        self.player_rect.x += x
        for tile in self.tile_list:
            if tile[1].colliderect(self.player_rect):
                if x > 0:  
                    self.player_rect.right = tile[1].left
                if x < 0: 
                    self.player_rect.left = tile[1].right
        for tile in self.moving:
            if tile[1].colliderect(self.player_rect):
                if x > 0:  
                    self.player_rect.right = tile[1].left
                if x < 0: 
                    self.player_rect.left = tile[1].right
        
        self.player_rect.y += y
        for tile in self.tile_list:
            if tile[1].colliderect(self.player_rect):
                if y > 0:  
                    self.player_rect.bottom = tile[1].top
                    self.grav = 0
                if y < 0:  
                    self.player_rect.top = tile[1].bottom
                    self.grav = 0
        for tile in self.moving:
            if tile[1].colliderect(self.player_rect):
                if y > 0:  
                    self.player_rect.bottom = tile[1].top
                    self.grav = 0
                if y < 0:  
                    self.player_rect.top = tile[1].bottom
                    self.grav = 0

        for tile in self.monsters:
            if tile[1].colliderect(self.player_rect):
                self.lost = True
                #print(self.lost)
        for tile in self.coins:
            if tile[1].colliderect(self.player_rect):
                self.coin_c -= 1
                self.coins.remove(tile)
        for tile in self.doors:
            if tile[1].colliderect(self.player_rect):
                self.won = True
                print(self.won) 
        
        if self.player_rect.y >600 :
            self.lost = True       

    def draw_player(self):
        self.window.blit(self.player, self.player_rect)
        
    def new_game(self):
        self.map = [
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 1],
                    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 7, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    ]

        
        self.new_player(670, 420)
        self.left = False
        self.right = False
        self.up = False
        self.grav = 0
        self.m_v = 1
        self.m_c = 0
        self.b_v = 1
        self.b_c = 0
        self.won = False
        self.lost = False
        self.coin_c = 3

        self.world()
  
    def main_loop(self):
        while True:
            self.check_events()
            if self.lost:
                self.lose()
            elif self.won and self.coin_c == 0:
                self.win()
            else:
                self.draw_window()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.right = True   
                if event.key == pg.K_LEFT:
                    self.left = True
                if event.key == pg.K_SPACE:
                    self.up = True
                if event.key == pg.K_1:
                    self.new_game()
                 
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.right = False
                if event.key == pg.K_LEFT:
                    self.left = False 
                if event.key == pg.K_SPACE:
                    self.up = False
            
    def win(self):

        font = pg.font.SysFont("Arial", 48)
        text1 = font.render("YOU WON!", True, (0, 255, 0))
        text2 = font.render("Press 1 to restart", True, (0, 255, 0))
        self.window.fill((0,0,0))
        self.window.blit(text1, (300, 250))
        self.window.blit(text2, (300, 310))
        pg.display.flip()

    def lose(self):
        font = pg.font.SysFont("Arial", 48)
        text1 = font.render("YOU LOST D:!", True, (255, 0, 0))
        text2 = font.render("Press 1 to restart", True, (255, 0, 0))
        self.window.fill((0,0,0))
        self.window.blit(text1, (300, 250))
        self.window.blit(text2, (300, 310))
        pg.display.flip()

    def draw_window(self):
        font = pg.font.SysFont("Arial", 24)
        text1 = font.render("Use the arrowkeys and spacebar to move", True, (255, 0, 0))
        text2 = font.render("Coins left to unlock the door: " + str(self.coin_c), True, (255, 0, 0))
        text3 = font.render("        Don´t  fall !", True, (255, 255, 255))

        self.window.fill((0,51,102))
        self.draw_world()
    
        
        self.p_movement()
        self.draw_player()

        
        self.window.blit(text1, (60,10))
        self.window.blit(text2, (480,10))
        self.window.blit(text3, (330,530))
        pg.display.flip()
        self.clock.tick(60)

Robotin()




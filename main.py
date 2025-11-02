import asyncio
import pygame as pg
from spritesheet import SpriteSheet as Sp

class Game:
    def __init__(self):
        pg.init()

        self.tile_size = 40
        self.width = 20 * self.tile_size  
        self.height = 15 * self.tile_size 

        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Ritter")
        
        self.clock = pg.time.Clock()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.player.right = True   
                if event.key == pg.K_LEFT:
                    self.player.left = True
                if event.key == pg.K_SPACE:
                    self.player.up = True
                if event.key == pg.K_1:
                    self.new_game()
                 
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.player.right = False
                if event.key == pg.K_LEFT:
                    self.player.left = False 
                if event.key == pg.K_SPACE:
                    self.player.up = False
                 
    async def start(self):

        font = pg.font.SysFont("Arial", 28)
        text1 = font.render("WELCOME", True, (205, 205, 205))
        text2 = font.render("Move with the arrowkeys and jump with the spacebar", True, (205, 205, 205))
        text5 = font.render("Press 1 to start", True, (205, 205, 205))
        text4 = font.render("Have fun, better graphics and more levels are coming !", True, (205, 205, 205))

        waiting = True
        while waiting: 
            self.window.fill((0,0,0))
            self.window.blit(text1, text1.get_rect(center=(self.width // 2, self.height // 2 - 150)))
            self.window.blit(text2, text2.get_rect(center=(self.width // 2, self.height // 2 - 50)))
            self.window.blit(text4, text4.get_rect(center=(self.width // 2, self.height // 2 + 50)))
            self.window.blit(text5, text5.get_rect(center=(self.width // 2, self.height // 2 + 100)))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    waiting = False
            await asyncio.sleep(0)

    def new_game(self):
        self.world = World()
        self.player = Player(670, 420)
        self.player.tiles = self.world.tiles
        self.player.platforms = self.world.platforms
        self.world.all_sprites.add(self.player)
        self.won = False
        self.lost = False
        self.coin_c = 3
        self.locked = True

    async def main_loop(self):
        while True:
            self.check_events()
            if self.lost:
                self.lose()
            elif self.won and self.locked == False:
                self.win()
            else:
                self.draw_window()
            await asyncio.sleep(0)

    def draw_window(self):
        font = pg.font.SysFont("Arial", 24)
       
        text2 = font.render("Coins left to unlock the door: " + str(self.coin_c), True, (255, 0, 0))
        text3 = font.render("        Don´t  fall !", True, (255, 255, 255))

        self.world.all_sprites.update()

        if self.player.hitbox.top > self.height:
            self.lost = True

        t_monster = pg.sprite.spritecollide(self.player, self.world.monsters, False, pg.sprite.collide_mask)
        if t_monster:
            self.lost = True

        
        t_coin = pg.sprite.spritecollide(self.player, self.world.coins, True, pg.sprite.collide_mask)
        if t_coin: 
            self.coin_c -= len(t_coin)

        t_door = pg.sprite.spritecollide(self.player, self.world.doors, False, pg.sprite.collide_mask)
        if t_door: 
            if self.coin_c <= 0:  
                self.won = True
                self.locked = False

        self.window.fill((0,51,102))
        self.world.all_sprites.draw(self.window)

        self.window.blit(text2, (280,10))
        self.window.blit(text3, (310,530))
        pg.display.flip()
        self.clock.tick(60)

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

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
class Door(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Sp("knight.png")
        self.animations = {
            "idle": self.image.get_imgs(0, 0, 3, 32, 32, 2.5),
            "run": self.image.get_imgs(0, 64, 7, 32, 32, 2.5),
            "jump": self.image.get_imgs(0, 160, 7, 32, 32, 2.5)
        }
        self.action = "idle"
        self.frame_i = 0
        self.image = self.animations[self.action][self.frame_i]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = pg.Rect(0, 0, 20, 28) 
        self.hitbox.center = self.rect.center
        self.mask = pg.mask.from_surface(self.image)
        
        self.animation_spd = 0.09
        self.left = False
        self.right = False
        self.up = False
        self.grav = 0
        self.lookig_l = False

    def update(self):

        x = 0
        y = 0

        if self.right:
            x += 2.5
            self.lookig_l = False
        if self.left:
            x -= 2.5
            self.lookig_l = True

        if abs(self.grav) > 0.5:
            self.action = "jump"
            self.animation_spd = 0.15
        elif x != 0: 
            self.action = "run"
            self.animation_spd = 0.15
            
        else:    
            self.action = "idle"
            self.animation_spd = 0.09
        
        
        if self.up and self.grav == 0:
            self.grav = -9
            self.up = False

        self.grav += 0.4
        if self.grav > 6:
            self.grav = 6
        y += self.grav

        self.hitbox.x += x
        
        for tile in self.tiles:
            if tile.rect.colliderect(self.hitbox):
                if x > 0: 
                    self.hitbox.right = tile.rect.left
                if x < 0: 
                    self.hitbox.left = tile.rect.right
        
        for plat in self.platforms:
            if plat.rect.colliderect(self.hitbox):
                if x > 0: 
                    self.hitbox.right = plat.rect.left
                if x < 0: 
                    self.hitbox.left = plat.rect.right

        self.hitbox.y += y

        for tile in self.tiles:
            if tile.rect.colliderect(self.hitbox):
                if y > 0: 
                    self.hitbox.bottom = tile.rect.top
                    self.grav = 0
                if y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.grav = 0
        
        for plat in self.platforms:
            if plat.rect.colliderect(self.hitbox):
                if y > 0: 
                    self.hitbox.bottom = plat.rect.top
                    self.grav = 0
                if y < 0: 
                    self.hitbox.top = plat.rect.bottom
                    self.grav = 0

        

        self.frame_i += self.animation_spd
        if self.frame_i >= len(self.animations[self.action]):
            self.frame_i = 0

        original = self.animations[self.action][int(self.frame_i)]
        if self.lookig_l:
            self.image = pg.transform.flip(original, True, False)
        else:
            self.image = original

        self.rect = self.image.get_rect() 
        self.rect.center = self.hitbox.center
        topping = 15
        
        self.rect.y -= topping
        self.mask = pg.mask.from_surface(self.image)

class Monster(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = Sp("slime_purple.png")
        self.animation = self.image.get_imgs(0, 0, 4, 24, 24, 2.5)
        self.frame_i = 0
        self.image = self.animation[self.frame_i]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.animation_spd = 0.09
        self.m_v = 0.6
        self.m_c = 0
        

    def update(self):
        self.m_c += 0.5
        self.rect.x += self.m_v
        if self.m_c > 60:
            self.m_v *= -1
            self.m_c = 0

        self.frame_i += self.animation_spd
        if self.frame_i >= len(self.animation):
            self.frame_i = 0 
        
        original = self.animation[int(self.frame_i)]
             
        if self.m_v < 0: 
            self.image = pg.transform.flip(original, True, False)
        else:             
            self.image = original

        self.mask = pg.mask.from_surface(self.image)

class MovingPlatform(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = Sp("platforms.png").get_bg(0,0,16,8,2.5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.b_v = 0.6
        self.b_c = 0
    
    def update(self):
        self.b_c += 0.5
        self.rect.y += self.b_v
        if self.b_c > 50:
            self.b_v *= -1
            self.b_c = 0

class Coin(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = Sp("coin.png")
        self.animation = self.image.get_imgs(0, 0, 12, 16, 16, 2.5)
        self.frame_i = 0
        self.image = self.animation[self.frame_i]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.animation_spd = 0.15

    def update(self):
        self.frame_i += self.animation_spd
        if self.frame_i >= len(self.animation):
            self.frame_i = 0
        self.image = self.animation[int(self.frame_i)]
        self.mask = pg.mask.from_surface(self.image)

class World(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.map = [
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 7, 0, 6, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 1],
                    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1],
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
      
        self.tiles = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

        self.tile_size = 40
        original_size = 16
        scale = self.tile_size / original_size

        world_tiles = Sp("world_tileset.png")
        door = pg.image.load("door.png")
        self.border = world_tiles.get_bg(128, 16, 16, 16, scale)
        self.ground = world_tiles.get_bg(0, 0, 16, 16, scale)
        self.door = pg.transform.scale(door,(60,131))

        row_count = 0 
        for row in self.map:
            col_count = 0
            for tile in row:

                x = col_count * self.tile_size
                y = row_count * self.tile_size

                if tile == 1:
                    border = Tile(x, y, self.border)
                    self.tiles.add(border)
                    self.all_sprites.add(border)


                if tile == 2:
                    ground = Tile(x,y, self.ground)
                    self.tiles.add(ground)
                    self.all_sprites.add(ground)

                if tile == 4:
                    m_b = (row_count + 1) * self.tile_size
                    monster = Monster(x,m_b)
                    self.monsters.add(monster)
                    self.all_sprites.add(monster)
                
                if tile == 5:
                    coin = Coin(x,y)
                    self.coins.add(coin)
                    self.all_sprites.add(coin)
                
                if tile == 6:
                    door = Door(x,y, self.door)
                    self.doors.add(door)
                    self.all_sprites.add(door)


                if tile == 7:
                    moving = MovingPlatform(x,y)
                    self.platforms.add(moving)
                    self.all_sprites.add(moving)

                col_count += 1
            row_count += 1

async def main():
    juego = Game()
    await juego.start()
    juego.new_game()
    await juego.main_loop()

asyncio.run(main())
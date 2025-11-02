import pygame as pg
class SpriteSheet:
    def __init__(self, image): 
        self.sheet = pg.image.load(image).convert_alpha()

    def get_imgs(self, x, y, frames, width, height, scale=1):
        
        images = []
        for i in range(frames):
            image = pg.Surface((width, height), pg.SRCALPHA)
            image.blit(self.sheet, (0, 0), (x + i * width, y, width, height))

            """ new_w = int(width * scale)
            new_h = int(height * scale)
            image = pg.transform.scale(image, (new_w, new_h)) """

            image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
            images.append(image)
        return images
    
    def get_bg(self, x, y, width, height, scale):
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        return image
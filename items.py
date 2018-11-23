import pygame as pg
from random import uniform, choice
from os import path
import settings as stg
vec = pg.math.Vector2

class droppable(pg.sprite.Sprite):
    def __init__(self, game, pos, type_is):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type_is = type_is
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_folder, stg.item_sprite_paths[self.type_is]))
        self.image = pg.transform.scale(self.image,(int(self.image.get_width()/1.5),int(self.image.get_height()/1.5)))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):

        if pg.time.get_ticks() - self.spawn_time > 10000:
            print(self.type_is + " despawned")
            self.kill()
    
    def effect(self):
        if self.type_is == "health_small":
            self.game.health += 10
            self.game.slurp_sound.play()
        elif self.type_is == "health_medium":
            self.game.health += 25
            self.game.slurp_sound.play()
        elif self.type_is == "health_large":
            self.game.health += 50
            self.game.slurp_sound.play()
import pygame as pg
from os import path
import settings as stg
from utilities import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
  
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        #self.image = game.wall_img
        self.image = pg.Surface((w, h))
        self.image.set_alpha(0)
        self.rect = pg.Rect(x,y,w,h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
     
class Connection(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, start_map, end_map, orientation, start_door, end_door):
        self.groups = game.all_sprites, game.connections
        pg.sprite.Sprite.__init__(self, self.groups)
        self.start_map = start_map
        self.end_map = end_map
        self.orientation = orientation
        self.start_door = start_door
        self.end_door = end_door
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(stg.YELLOW)
        self.image.set_alpha(0)     
        self.rect = pg.Rect(x,y,w,h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        if self.game.draw_debug:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(0)
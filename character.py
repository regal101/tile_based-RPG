import pygame as pg
from random import uniform, choice
from os import path
import settings as stg
from utilities import collide_hit_rect
from other_objects import collide_with_walls

vec = pg.math.Vector2

def swap_aoe_color(surf, colour):
    arr = pg.PixelArray(surf)
    
    if colour == "redd":
        arr.replace((0,0,82),(62,0,0))
        arr.replace((0,21,130),(105,11,0))
        arr.replace((19,49,161),(160,21,0))
        arr.replace((48,93,182),(230,11,0))
        arr.replace((74,121,208),(255,0,0))
        arr.replace((110,166,235),(255,99,106))
        arr.replace((151,206,255),(255,160,160))
        arr.replace((205,250,255),(255,220,220))
    elif colour == "red":
        arr.replace((0,0,82),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((0,21,130),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((19,49,161),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((48,93,182),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((74,121,208),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((110,166,235),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((151,206,255),(255,128,255),0, weights=(0.333, 0.333, 0.334))
        arr.replace((205,250,255),(255,128,255),0, weights=(0.333, 0.333, 0.334))
    elif colour == "green":
        arr.replace((0,0,82),(0,0,0))
        arr.replace((0,21,130),(0,7,0))
        arr.replace((19,49,161),(0,32,0))
        arr.replace((48,93,182),(0,59,0))
        arr.replace((74,121,208),(0,87,0))
        arr.replace((110,166,235),(0,114,0))
        arr.replace((151,206,255),(0,141,0))
        arr.replace((205,250,255),(0,169,0))
    elif colour == "white":
        arr.replace((0,0,82),stg.WHITE)
        arr.replace((0,21,130),stg.WHITE)
        arr.replace((19,49,161),stg.WHITE)
        arr.replace((48,93,182),stg.WHITE)
        arr.replace((74,121,208),stg.WHITE)
        arr.replace((110,166,235),stg.WHITE)
        arr.replace((151,206,255),stg.WHITE)
        arr.replace((205,250,255),stg.WHITE)
    elif colour == "g":
        arr.replace((0,0,82),(0,255,0))
        arr.replace((0,21,130),(0,255,0))
        arr.replace((19,49,161),(0,255,0))
        arr.replace((48,93,182),(0,255,0))
        arr.replace((74,121,208),(0,255,0))
        arr.replace((110,166,235),(0,255,0))
        arr.replace((151,206,255),(0,255,0))
        arr.replace((205,250,255),(0,255,0))
    del arr
       
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.equipment = 'range'
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = stg.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.orientation = vec(0,1)
        self.last_update = 0
        self.current_frame = 0
        self.last_rot = 0
        self.last_attack = 0
        self.last_hit = 0
        self.attacking = False
        self.attack_rate = stg.BASE_ATTACK_RATE
         
    def load_images(self):
        
        if self.equipment == 'melee':
            if self.game.melee_equipment_level == 1:
                self.type_is = 'Villager'
                path_ext = '\\Male\\Standard'
            elif self.game.melee_equipment_level == 2:
                self.type_is = 'Manarms'
                path_ext = ''
        elif self.equipment == 'range':
            if self.game.range_equipment_level == 1:
                self.type_is = 'Villager'
                path_ext = '\\Male\\Hunt'
            elif self.game.range_equipment_level == 2:
                self.type_is = 'Archer'
                path_ext = ''

            

        self.walking_frames = []
        self.num_walk_frames = stg.number_of_frames[self.type_is+' walk']
        for i in range (1,self.num_walk_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + path_ext + '\\Walk\\' + '{}walk00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + path_ext + '\\Walk\\' + '{}walk0{}.png'.format(self.type_is,i)
            self.walking_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_walk_frames*(j),self.num_walk_frames*(j+1)):
                self.walking_frames.append(pg.transform.flip(self.walking_frames[i],True,False))
        
        self.standing_frames = []
        self.num_stand_frames = stg.number_of_frames[self.type_is+' stand']
        for i in range (1,self.num_stand_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + path_ext + '\\Stand Ground\\' + '{}stand00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + path_ext + '\\Stand Ground\\' + '{}stand0{}.png'.format(self.type_is,i)
            self.standing_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_stand_frames*(j),self.num_stand_frames*(j+1)):
                self.standing_frames.append(pg.transform.flip(self.standing_frames[i],True,False))
        
        self.attacking_frames = []
        self.num_attack_frames = stg.number_of_frames[self.type_is+' attack']
        for i in range (1,self.num_attack_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + path_ext + '\\Attack\\' + '{}attack00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + path_ext + '\\Attack\\' + '{}attack0{}.png'.format(self.type_is,i)
            self.attacking_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_attack_frames*(j),self.num_attack_frames*(j+1)):
                self.attacking_frames.append(pg.transform.flip(self.attacking_frames[i],True,False))
        
        self.dying_frames = []
        self.num_dying_frames = stg.number_of_frames[self.type_is+' die']
        for i in range (1,self.num_dying_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + path_ext + '\\Die\\' + '{}die00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + path_ext + '\\Die\\' + '{}die0{}.png'.format(self.type_is,i)
            self.dying_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_dying_frames*(j),self.num_dying_frames*(j+1)):
                self.dying_frames.append(pg.transform.flip(self.dying_frames[i],True,False))
        
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE]:
            self.attack()        
        else:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x = -stg.PLAYER_SPEED
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x = stg.PLAYER_SPEED
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y = -stg.PLAYER_SPEED
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y = stg.PLAYER_SPEED
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
                     
    def attack(self):
        now = pg.time.get_ticks()
        if self.equipment == 'range':
            if now - self.last_attack > self.attack_rate:
                self.game.arrow_fire.play()
                self.attacking = True
                self.last_attack = now
                pos = self.pos
                Arrow(self.game, pos, self.orientation )
                
        elif self.equipment == 'melee':
            if now - self.last_attack > self.attack_rate:
                self.attacking = True
                self.last_attack = now
        
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > stg.ARROW_RATE:
            self.attacking = False
        self.get_keys()
        if self.attacking == True:
            self.vel = vec(0,0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        
        largest_dot = 0
        for direction in stg.directions:
            dot = self.vel.dot(direction)
            if dot > largest_dot:
                largest_dot = dot
                self.orientation = direction
                
        if self.attacking == True:
            self.vel = vec(0,0)
        self.animate()

    def animate(self):
        fms = []
        if self.vel.length() == 0 and self.attacking == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_stand_frames,(i+1)*self.num_stand_frames):
                        fms.append(self.standing_frames[frame_num])
        
        elif self.vel.length() != 0 and self.attacking == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_walk_frames,(i+1)*self.num_walk_frames):
                        fms.append(self.walking_frames[frame_num])
                        
        elif self.attacking == True:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_attack_frames,(i+1)*self.num_attack_frames):
                        fms.append(self.attacking_frames[frame_num])
        
        elif self.dying == True:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_dying_frames,(i+1)*self.num_dying_frames):
                        fms.append(self.dying_frames[frame_num])
        
        if self.attacking:
            update_interval = 33
        else:
            update_interval = 40
        current_time = pg.time.get_ticks()
        if current_time - self.last_update > update_interval:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(fms)
                rect_center = self.rect.center
                self.image = fms[self.current_frame]
                self.image = pg.transform.scale(self.image,(int(self.image.get_width()/1.5),int(self.image.get_height()/1.5)))
                swap_aoe_color(self.image,"red")
                self.rect = self.image.get_rect()
                self.rect.center = rect_center

        self.mask = pg.mask.from_surface(self.image)

               
class Arrow(pg.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self.groups = game.all_sprites, game.arrows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img_orig = pg.transform.scale( pg.image.load(path.join(self.game.img_folder, stg.ARROW_IMG)).convert_alpha(),(5,20))            
        self.image = pg.transform.rotate(self.img_orig,-vec(0,-1).angle_to(direction))
        self.vel = vec(direction)*stg.ARROW_SPEED
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.hit_rect = stg.ARROW_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.spawn_time = pg.time.get_ticks()
 
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False, False)
        for hit in hits:
            if hit.name != 'water':
                self.kill()
        if pg.time.get_ticks() - self.spawn_time > stg.range_equipment_stats[str(self.game.range_equipment_level)][2]:
            self.kill()
            
        self.mask = pg.mask.from_surface(self.image)    
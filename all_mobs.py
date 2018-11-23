import pygame as pg
from os import path
import settings as stg
import random as rnd
from other_objects import collide_with_walls
from utilities import Spritesheet
from items import droppable
vec = pg.math.Vector2

def drop_items(game,pos,mob_type):

    rand = rnd.random()
    for item in stg.drop_rates[mob_type]:
        if rand < item[1]:
            print(item[0] + " dropped")
            droppable(game,pos,item[0])
    
            

class Demon(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.frames = []
        self.type_is = "Demon"
        #0-5 n/s 6-11 l/r
        for i in range (1,10):
            fullPath = 'minotaur_frames\minotaur ({}).png'.format(i) 
            self.frames.append( pg.image.load(path.join(game.img_folder, fullPath)) )
        for i in range (6,9):
            self.frames.append(pg.transform.flip( self.frames[i], True, False))
        self.image = self.frames[0]
        
        #self.image = pg.Surface((50,40))
        #self.image.fill(YELLOW)
        
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = pg.Rect(0,0,20,30)
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 30)
        self.rect.center = self.pos
        self.orientation = "N"
        self.last_update = 0
        self.current_frame = 0
        self.last_hit = 0
        self.attacking = False
        
        self.health = stg.mob_stats[self.type_is][0]
        self.damage = stg.mob_stats[self.type_is][1]
        
        self.game.demon_growl.play()

    def update(self):
        
        self.animate()
        
        self.vel += 3*(self.game.player.pos - self.pos)/(self.game.player.pos - self.pos).length()
        self.vel -= self.vel*0.05
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            drop_items(self.game,self.rect.center,self.type_is)
            self.kill()
    
    
        if abs(self.vel.x) == 0:
            self.vel.y += 3
        if abs(self.vel.y) == 0:
            self.vel.x += 3
        
        if abs(self.vel.x) > abs(self.vel.y):
            if self.vel.x > 0:
                self.orientation = "E"
            if self.vel.x < 0:
                self.orientation = "W"    
        else:
            if self.vel.y > 0:
                self.orientation = "S"
            if self.vel.y < 0:
                self.orientation = "N"

        self.draw_health()
    def animate(self):
        
        fms = []
        if self.orientation == "E":
            fms.extend([self.frames[10],self.frames[11],self.frames[9]]) 
        elif self.orientation == "W":
            fms.extend([self.frames[6],self.frames[8],self.frames[6]]) 
        elif self.orientation == "S":
            fms.extend([self.frames[4],self.frames[5],self.frames[3]]) 
        elif self.orientation == "N":
            fms.extend([self.frames[1],self.frames[2],self.frames[0]])
        
        current_time = pg.time.get_ticks()
        if current_time - self.last_update > 100:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % (len(fms)-1)
                center = self.rect.center
                self.image = fms[self.current_frame]
                self.image = pg.transform.scale(self.image,(35,55))
                self.rect = self.image.get_rect()
                self.rect.center = center
            
    def draw_health(self):
        health_fraction = self.health/stg.mob_stats[self.type_is][0]
        if health_fraction > 0.5:
            col = stg.BLUE
        elif health_fraction > 0.25:
            col = stg.YELLOW
        else:
            col = stg.RED
        width = int(30 * health_fraction)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < stg.mob_stats[self.type_is][0]:
            pg.draw.rect(self.image, col, self.health_bar)

class Aoe_melee(pg.sprite.Sprite):
    def __init__(self, game, x, y,type_is):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type_is = type_is
        
        self.health = stg.mob_stats[type_is][0]
        self.damage = stg.mob_stats[type_is][1]
        
        self.load_images()
        self.image = self.standing_frames[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = stg.MILITIA_HIT_RECT
        self.hit_rect.center = self.rect.center
        
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.orientation = rnd.choice(stg.directions)
        self.last_orientation = self.orientation
        self.attacking = False
        self.dying = False
        self.last_update = 0
        self.current_frame = 0
        self.last_hit = 0
        
        try:
            pg.mixer.Sound(path.join(self.game.snd_folder,stg.mob_spawn_sounds[self.type_is])).play()
        except:
            print("Spawn sound not available")
            
    def load_images(self):
        self.walking_frames = []
        self.num_walk_frames = stg.number_of_frames[self.type_is+' walk']
        for i in range (1,self.num_walk_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + '\\Walk\\' + '{}walk00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + '\\Walk\\' + '{}walk0{}.png'.format(self.type_is,i)
            self.walking_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_walk_frames*(j),self.num_walk_frames*(j+1)):
                self.walking_frames.append(pg.transform.flip(self.walking_frames[i],True,False))
        
        self.standing_frames = []
        self.num_stand_frames = stg.number_of_frames[self.type_is+' stand']
        for i in range (1,self.num_stand_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + '\\Stand Ground\\' + '{}stand00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + '\\Stand Ground\\' + '{}stand0{}.png'.format(self.type_is,i)
            self.standing_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_stand_frames*(j),self.num_stand_frames*(j+1)):
                self.standing_frames.append(pg.transform.flip(self.standing_frames[i],True,False))
        
        self.attacking_frames = []
        self.num_attack_frames = stg.number_of_frames[self.type_is+' attack']
        for i in range (1,self.num_attack_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + '\\Attack\\' + '{}attack00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + '\\Attack\\' + '{}attack0{}.png'.format(self.type_is,i)
            self.attacking_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_attack_frames*(j),self.num_attack_frames*(j+1)):
                self.attacking_frames.append(pg.transform.flip(self.attacking_frames[i],True,False))
        
        self.dying_frames = []
        self.num_dying_frames = stg.number_of_frames[self.type_is+' die']
        for i in range (1,self.num_dying_frames*5 + 1):
            if i < 10:
                Path = 'Units\\' + self.type_is + '\\Die\\' + '{}die00{}.png'.format(self.type_is,i)
            else:
                Path = 'Units\\' + self.type_is + '\\Die\\' + '{}die0{}.png'.format(self.type_is,i)
            self.dying_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_dying_frames*(j),self.num_dying_frames*(j+1)):
                self.dying_frames.append(pg.transform.flip(self.dying_frames[i],True,False))
        
    def update(self):
        
        self.vel = vec(0,0)
        self.chase_player()
        self.avoid_mobs()
        #self.apply_friction()
        
        if self.attacking == True or self.dying == True:
            self.vel = vec(0,0)
        
        #self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
   
        self.calc_orientation()
        
        if self.health <= 0 and self.dying == False:
            self.dying = True
            self.game.experience += stg.mob_exp[self.type_is]
            self.current_frame = 0
        
        if len(pg.sprite.spritecollide(self, self.game.player_group, False)) == 0:
            self.attacking = False
            
        self.animate()
        self.draw_health()
    
    def chase_player(self):
        disp = self.game.player.pos - self.pos
        if disp.length() < 200:
            self.vel += stg.mob_stats[self.type_is][3]*disp.normalize()

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                disp = self.pos - mob.pos
                if 0 < disp.length() < 25:
                    self.vel += disp.normalize()*2
                    
    def calc_orientation(self):
        if self.vel.length() > 1:
            largest_dot = 0
            for direction in stg.directions:
                dot = self.vel.dot(direction)
                if dot > largest_dot:
                    largest_dot = dot
                    self.orientation = direction
                    self.last_orientation = self.orientation
        else:
            self.orientation = self.last_orientation
            
    def apply_friction(self):
        self.acc -= self.vel*stg.MOB_FRICTION
        if self.vel.length() < 1:
            self.acc = vec(0,0)
            self.vel = vec(0,0)
    
    def animate(self):
        fms = []
        if self.vel.length() == 0 and self.attacking == False and self.dying == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_stand_frames,(i+1)*self.num_stand_frames):
                        fms.append(self.standing_frames[frame_num])
        
        elif self.vel.length() != 0 and self.attacking == False and self.dying == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_walk_frames,(i+1)*self.num_walk_frames):
                        fms.append(self.walking_frames[frame_num])
                        
        elif self.attacking == True and self.dying == False:
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
            update_interval = stg.mob_stats[self.type_is][2]/self.num_attack_frames
        else:
            update_interval = stg.mob_frame_rates[self.type_is]
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_update > update_interval:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(fms)
                rect_center = self.rect.center
                self.image = fms[self.current_frame]
                self.image = pg.transform.scale(self.image,(int(self.image.get_width()/1.5),int(self.image.get_height()/1.5)))
                self.rect = self.image.get_rect()
                self.rect.center = rect_center
                if self.dying == True and self.current_frame == self.num_dying_frames - 1:
                    drop_items(self.game,self.rect.center,self.type_is)
                    self.kill()

        self.mask = pg.mask.from_surface(self.image)
        
    def draw_health(self):
        health_fraction = self.health/stg.mob_stats[self.type_is][0]
        if health_fraction > 0.5:
            col = stg.BLUE
        elif health_fraction > 0.25:
            col = stg.YELLOW
        else:
            col = stg.RED
        width = int(30 * health_fraction)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < stg.mob_stats[self.type_is][0]:
            pg.draw.rect(self.image, col, self.health_bar)



class Undead(pg.sprite.Sprite):
    def __init__(self, game, x, y,type_is):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type_is = type_is
        
        self.health = stg.mob_stats[type_is][0]
        self.damage = stg.mob_stats[type_is][1]
        
        self.spritesheet = Spritesheet(path.join(self.game.img_folder,stg.UNDEAD_SPRITES))
        self.directions_4 = [vec(0,1),vec(0,-1), vec(1,0), vec(-1,0) ]
        self.load_images()
        self.image = self.frames[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = stg.MILITIA_HIT_RECT
        self.hit_rect.center = self.rect.center
        
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.orientation = rnd.choice(self.directions_4)
        self.last_orientation = self.orientation
        self.attacking = False
        self.dying = False
        self.last_update = 0
        self.current_frame = 0
        self.last_hit = 0
        self.regen_timer = 0
        
        try:
            pg.mixer.Sound(path.join(self.game.snd_folder,stg.mob_spawn_sounds[self.type_is])).play()
        except:
            print("Spawn sound not available")
            
    def load_images(self):
        
        self.frames = []
        spritesheet_coords = stg.Undead_spritesheet_coords[self.type_is]
        for coord in spritesheet_coords:
            frame = self.spritesheet.get_image(*coord,0.75)
            self.frames.append(frame)
        for i in range(14,21):
            self.frames.append(pg.transform.flip(self.frames[i], True, False))
            
        for i in range(0,len(self.frames)):
            if int((i+1)/7) == (i+1)/7 and self.type_is != "Sludge":
                self.frames[i].set_colorkey((191,97,226))
            else:    
                self.frames[i].set_colorkey((0,128,255))

        
        
    def update(self):
        
        self.vel = vec(0,0)
        self.chase_player()
        self.avoid_mobs()
        #self.apply_friction()
        
        if self.attacking == True or self.dying == True:
            self.vel = vec(0,0)
        
        #self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
   
        self.calc_orientation()
        
        if self.health <= 0 and self.dying == False:
            self.dying = True
            self.game.experience += stg.mob_exp[self.type_is]
            self.current_frame = 0
        
        if len(pg.sprite.spritecollide(self, self.game.player_group, False)) == 0:
            self.attacking = False
        
        current_time = pg.time.get_ticks()
        if current_time - self.regen_timer > 1000:
            self.regen_timer = current_time
            self.health += 1
        self.animate()
        self.draw_health()
    
    def chase_player(self):
        disp = self.game.player.pos - self.pos
        if disp.length() < 200:
            self.vel += stg.mob_stats[self.type_is][3]*disp.normalize()

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                disp = self.pos - mob.pos
                if 0 < disp.length() < 25:
                    self.vel += disp.normalize()*2
                    
    def calc_orientation(self):
        if self.vel.length() > 1:
            largest_dot = 0
            for direction in self.directions_4:
                dot = self.vel.dot(direction)
                if dot > largest_dot:
                    largest_dot = dot
                    self.orientation = direction
                    self.last_orientation = self.orientation
        else:
            self.orientation = self.last_orientation
            
    def apply_friction(self):
        self.acc -= self.vel*stg.MOB_FRICTION
        if self.vel.length() < 1:
            self.acc = vec(0,0)
            self.vel = vec(0,0)
    
    def animate(self):
        
        
        fms = []
        
        if self.vel.length() != 0 and self.attacking == False and self.dying == False:
            for i in range(0,4):
                direction = self.directions_4[i]
                if self.orientation == direction:
                    for frame_num in range(i*7 + 1, i*7 + 1 + 4):
                        fms.append(self.frames[frame_num])
                    for frame_num in range(4 + i*7, 0 + i*7, -1):
                        fms.append(self.frames[frame_num])
        
        elif self.vel.length() == 0 and self.attacking == False and self.dying == False:
            for i in range(0,4):
                direction = self.directions_4[i]
                if self.orientation == direction:
                    fms.append(self.frames[i*7])
        
        elif self.attacking == True and self.dying == False:
            for i in range(0,4):
                direction = self.directions_4[i]
                if self.orientation == direction:
                    fms.append(self.frames[i*7])
                    fms.append(self.frames[i*7 + 5])
                    
        elif self.dying == True:
            for i in range(0,4):
                direction = self.directions_4[i]
                if self.orientation == direction:
                    fms.append(self.frames[i*7 + 6])

        
        update_interval = stg.mob_frame_rates[self.type_is]
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_update > update_interval:
                if self.dying == True and current_time - self.last_update > 1500:
                    drop_items(self.game,self.rect.center,self.type_is)
                    self.kill()
                if not self.dying:
                    self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(fms)
                rect_center = self.rect.center
                self.image = fms[self.current_frame]
                #self.image = pg.transform.scale(self.image,(int(self.image.get_width()/1.5),int(self.image.get_height()/1.5)))
                self.rect = self.image.get_rect()
                self.rect.center = rect_center
                #print(self.current_frame)
                
                

        self.mask = pg.mask.from_surface(self.image)
        
    def draw_health(self):
        health_fraction = self.health/stg.mob_stats[self.type_is][0]
        if health_fraction > 0.5:
            col = stg.BLUE
        elif health_fraction > 0.25:
            col = stg.YELLOW
        else:
            col = stg.RED
        width = int(30 * health_fraction)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < stg.mob_stats[self.type_is][0]:
            pg.draw.rect(self.image, col, self.health_bar)

class Aoe_villager(pg.sprite.Sprite):
    def __init__(self, game, x, y,type_is, start_orientation,speech):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type_is = type_is
        self.speech = speech
        if self.type_is == "Farm":
            self.gender = 'Male\\'
        else:
            self.gender = rnd.choice(['Male\\','Female\\'])
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = stg.MILITIA_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.orientation = start_orientation
        self.last_orientation = self.orientation
        self.last_update = 0
        self.current_frame = 0
        self.dying = False
        self.health = stg.mob_stats["Villager"][0]
        self.acting = True
        try:
            pg.mixer.Sound(path.join(self.game.snd_folder,stg.mob_spawn_sounds[self.type_is])).play()
        except:
            print(self.type_is + " spawn sound not available")
            
    def load_images(self):
        self.walking_frames = []
        self.num_walk_frames = stg.number_of_frames[self.type_is+' walk']
        for i in range (1,self.num_walk_frames*5 + 1):
            if i < 10:
                Path = 'Units\\Villager\\'+ self.gender + "\\" + self.type_is + '\\Walk\\' + 'Villagerwalk00{}.png'.format(i)
            else:
                Path = 'Units\\Villager\\'+ self.gender + "\\" + self.type_is + '\\Walk\\' + 'Villagerwalk0{}.png'.format(i)
            self.walking_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_walk_frames*(j),self.num_walk_frames*(j+1)):
                self.walking_frames.append(pg.transform.flip(self.walking_frames[i],True,False))
        
        self.standing_frames = []
        self.num_stand_frames = stg.number_of_frames[self.type_is+' stand']
        for i in range (1,self.num_stand_frames*5 + 1):
            if i < 10:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Stand Ground\\' + 'Villagerstand00{}.png'.format(i)
            else:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Stand Ground\\' + 'Villagerstand0{}.png'.format(i)
            self.standing_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_stand_frames*(j),self.num_stand_frames*(j+1)):
                self.standing_frames.append(pg.transform.flip(self.standing_frames[i],True,False))
        
        self.acting_frames = []
        self.num_acting_frames = stg.number_of_frames[self.type_is+' act']
        for i in range (1,self.num_acting_frames*5 + 1):
            if i < 10:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Act\\' + 'Villageract00{}.png'.format(i)
            elif i < 100:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Act\\' + 'Villageract0{}.png'.format(i)
            else:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Act\\' + 'Villageract{}.png'.format(i)
            self.acting_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_acting_frames*(j),self.num_acting_frames*(j+1)):
                self.acting_frames.append(pg.transform.flip(self.acting_frames[i],True,False))
        """
        self.dying_frames = []
        self.num_dying_frames = stg.number_of_frames[self.type_is+' die']
        for i in range (1,self.num_dying_frames*5 + 1):
            if i < 10:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Die\\' + 'Villagerdie00{}.png'.format(i)
            else:
                Path = 'Units\\Villager\\' + self.gender + "\\" + self.type_is + '\\Die\\' + 'Villagerdie0{}.png'.format(i)
            self.dying_frames.append( pg.image.load(path.join(self.game.img_folder, Path)) )
        for j in range(3,0,-1):
            for i in range(self.num_dying_frames*(j),self.num_dying_frames*(j+1)):
                self.dying_frames.append(pg.transform.flip(self.dying_frames[i],True,False))

        """
    def update(self):
        
        self.vel = vec(0,0)
        
        #self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')
        self.rect.center = self.hit_rect.center
        self.calc_orientation()
        
        if self.health <= 0 and self.dying == False:
            self.dying = True
            self.game.experience += stg.mob_exp[self.type_is]
            self.current_frame = 0
               
        self.animate()
        #self.draw_health()
                    
    def calc_orientation(self):
        if self.vel.length() > 1:
            largest_dot = 0
            for direction in stg.directions:
                dot = self.vel.dot(direction)
                if dot > largest_dot:
                    largest_dot = dot
                    self.orientation = direction
                    self.last_orientation = self.orientation
        else:
            self.orientation = self.last_orientation
            
    def apply_friction(self):
        self.acc -= self.vel*stg.MOB_FRICTION
        if self.vel.length() < 1:
            self.acc = vec(0,0)
            self.vel = vec(0,0)
    
    def animate(self):
        fms = []
        if self.vel.length() == 0 and self.acting == False and self.dying == False and self.acting == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_stand_frames,(i+1)*self.num_stand_frames):
                        fms.append(self.standing_frames[frame_num])
        
        elif self.vel.length() != 0 and self.acting == False and self.dying == False and self.acting == False:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_walk_frames,(i+1)*self.num_walk_frames):
                        fms.append(self.walking_frames[frame_num])
        
        elif self.acting ==  True:
            for i in range(0,8):
                direction = stg.directions[i]
                if self.orientation == direction:
                    for frame_num in range(i*self.num_acting_frames,(i+1)*self.num_acting_frames):
                        fms.append(self.acting_frames[frame_num])
                        
        update_interval = stg.mob_frame_rates[self.type_is]
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_update > update_interval:
                self.last_update = current_time
                self.current_frame = (self.current_frame + 1) % len(fms)
                rect_center = self.rect.center
                self.image = fms[self.current_frame]
                self.image = pg.transform.scale(self.image,(int(self.image.get_width()/1.5),int(self.image.get_height()/1.5)))
                self.rect = self.image.get_rect()
                self.rect.center = rect_center
                #print(self.current_frame)

        self.mask = pg.mask.from_surface(self.image)











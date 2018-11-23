import pygame as pg
import sys
from os import path
import random as rnd
import settings as stg
from menus import Pause_Menu, Gameover_Menu, Start_Menu, Create_Account_Menu, message_box
from other_objects import Obstacle, Connection
from character import Player
from tilemap import TiledMap, Camera
from all_mobs import Demon, Aoe_melee, Aoe_villager, Undead
from utilities import collide_hit_rect, draw_text, TextInput
vec = pg.math.Vector2

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 12
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = stg.GREEN
    elif pct > 0.3:
        col = stg.YELLOW
    else:
        col = stg.RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, stg.WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((stg.WIDTH, stg.HEIGHT))
        pg.display.set_caption(stg.TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        

    def load_data(self):

        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.snd_folder = path.join(self.game_folder, 'snd')
        
        self.map_list = []
        self.start_map = TiledMap(self,path.join(self.map_folder, 'Map1_Start_Map.tmx'),1)
        self.map_2 = TiledMap(self,path.join(self.map_folder, 'Map2_Field.tmx'),2)
        self.map_3 = TiledMap(self,path.join(self.map_folder, 'Map3_Start_Map_House1.tmx'),3)
        self.map_4 = TiledMap(self,path.join(self.map_folder, 'Map4_Meadows.tmx'),4)
        self.map_5 = TiledMap(self,path.join(self.map_folder, 'Map5_Undead_Cave.tmx'),5)
        self.map_6 = TiledMap(self,path.join(self.map_folder, 'Map6_Castle_Walkway.tmx'),6)
        self.map_7 = TiledMap(self,path.join(self.map_folder, 'Map7_Desert_Town.tmx'),7)
        self.map_list.extend([self.start_map,self.map_2,self.map_3,self.map_4,
                              self.map_5,self.map_6,self.map_7])
        
        self.slurp_sound = pg.mixer.Sound(path.join(self.snd_folder,"slurp_sound.wav"))
        self.arrow_fire = pg.mixer.Sound(path.join(self.snd_folder,"arrow_fire.wav"))
        self.demon_growl = pg.mixer.Sound(path.join(self.snd_folder,"demon_growl.wav"))
        self.pause_sound = pg.mixer.Sound(path.join(self.snd_folder,"pause_sound.wav"))
        self.continue_sound = pg.mixer.Sound(path.join(self.snd_folder,"continue_sound.wav"))
        self.gameover_sound = pg.mixer.Sound(path.join(self.snd_folder,"gameover_sound.wav"))
        self.save_sound = pg.mixer.Sound(path.join(self.snd_folder,"save_sound.wav"))
        self.sword_sounds = [pg.mixer.Sound(path.join(self.snd_folder,"sword_clang1.wav")),
                             pg.mixer.Sound(path.join(self.snd_folder,"sword_clang2.wav")),
                             pg.mixer.Sound(path.join(self.snd_folder,"sword_clang3.wav")) ]
        self.music1 = pg.mixer.music.load(path.join(self.snd_folder,"TownTheme.mp3"))
        

        
    def new_map(self,m):
        # initialize all variables and do all the setup for a new game
        self.all_sprites.empty()
        self.obstacles.empty()
        self.mobs.empty()
        self.npcs.empty()
        self.arrows.empty()
        self.connections.empty()
        self.items.empty()
        
        try:
            map_name = stg.map_dict[str(self.current_map.map_num)]
            pg.mixer.music.load(path.join( self.snd_folder,"{}".format( stg.map_music[map_name])))
            pg.mixer.music.play(-1)
        except:
            pg.mixer.music.fadeout(1000)

        for tile_object in m.tmxdata.objects:
            if tile_object.type == 'obstacle':
                if tile_object.name == 'water':
                    Obstacle(self, tile_object.x,tile_object.y,
                             tile_object.width,tile_object.height,tile_object.name)
                else:
                    Obstacle(self, tile_object.x,tile_object.y,
                             tile_object.width,tile_object.height,tile_object.name)

            if tile_object.type == 'cnct':
                Connection(self, tile_object.x,tile_object.y,
                         tile_object.width,tile_object.height,
                         tile_object.name[0],tile_object.name[2],tile_object.name[3],
                         tile_object.name[4],tile_object.name[6]
                         )    
                
            if tile_object.type == 'mob':
                if tile_object.name == 'militia':
                    Aoe_melee(self,tile_object.x,tile_object.y,'Militia')
                elif tile_object.name == 'champion':
                    Aoe_melee(self,tile_object.x,tile_object.y,'Champion')
                elif tile_object.name == 'knight':
                    Aoe_melee(self,tile_object.x,tile_object.y,'Knight')
                #elif tile_object.name == 'demon':
                 #   Demon(self,tile_object.x,tile_object.y)
                elif tile_object.name == 'undead':
                    Undead(self,tile_object.x,tile_object.y,rnd.choice(["Mummy","Zombie"]))
                    

                    
            if tile_object.type == 'npc':
               print(tile_object.name)
               for npc in stg.npc_data[str(self.current_map.map_num)]:
                   print(npc)
                   if tile_object.name == npc[0]:
                       print("created")
                       Aoe_villager(self,tile_object.x,tile_object.y,npc[1],npc[2],npc[3])
               
    
                
                #Demon(self,tile_object.x,tile_object.y)
                
        self.camera = Camera(m.width, m.height)
        
        
    def new_game(self):#,spawn_map):
        
        g.show_start_screen()
        
        
        self.current_map = self.spawn_map
        
        self.is_paused = False
        self.draw_debug = False
        
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.GroupSingle()
        self.obstacles = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.connections = pg.sprite.Group()
        self.items = pg.sprite.Group()
        
        
        self.new_map(self.spawn_map)
        
        self.player = Player(self,self.spawn_location[0],self.spawn_location[1])
        self.range_power = stg.RANGE_BASE_POWER + self.level/2 + stg.range_equipment_stats[str(self.range_equipment_level)][0]
        self.melee_power = stg.MELEE_BASE_POWER + self.level + stg.melee_equipment_stats[str(self.melee_equipment_level)][0]
        self.range_defense = stg.RANGE_BASE_POWER + self.level/2 + stg.range_equipment_stats[str(self.range_equipment_level)][1]
        self.melee_defense = stg.MELEE_BASE_POWER + self.level + stg.melee_equipment_stats[str(self.melee_equipment_level)][1]
        self.equipment = 'melee'
        
        self.current_map_img = self.current_map.make_map()
        self.current_map_rect = self.current_map_img.get_rect()
        
        
        
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(stg.FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):       
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.check_connections()
        self.all_sprites.update()
        self.camera.update(self.player)
        
        # mobs hit player
        if pg.sprite.spritecollide(self.player, self.mobs, False):
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
            for hit in hits:
                hit.attacking = True
                current_time = pg.time.get_ticks()
                if current_time - hit.last_hit > stg.mob_stats[hit.type_is][2]:
                    hit.last_hit = current_time
                    
                    if self.equipment == 'melee':
                        self.health -= max(hit.damage-self.melee_defense,1)
                    elif self.equipment == 'range':
                        self.health -= max(hit.damage-self.range_defense,1)   
                                           
                    if isinstance(hit,Aoe_melee):
                        rnd.choice(self.sword_sounds).play()
                if self.health <= 0:
                    self.playing = False
                    self.health = 100
        
        
        # range damage
        if pg.sprite.groupcollide(self.mobs, self.arrows, False,False):
            hits = pg.sprite.groupcollide(self.mobs, self.arrows, False,True, pg.sprite.collide_mask)
            for hit in hits:
                hit.health -= self.range_power
                hit.vel = vec(0, 0)
            
        # melee damage
        if pg.sprite.spritecollideany(self.player, self.mobs, False):
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
            for hit in hits:
                if self.player.attacking == True and self.player.equipment == 'melee':
                    current_time = pg.time.get_ticks()
                    if current_time - self.player.last_hit > self.player.attack_rate:
                        self.player.last_hit = current_time
                        hit.health -= self.melee_power
                        rnd.choice(self.sword_sounds).play()
        
        # check speech
        self.messages = []
        hits = pg.sprite.spritecollide(self.player, self.npcs, False)
        for hit in hits:
            #print("colllide")
            self.messages.append(message_box(hit.speech,stg.WHITE,hit.rect.centerx,hit.rect.centery-50,size = "small"))
                
        # check bed collisions
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        for hit in hits:
            print(hit.name)
            if hit.name == 'bed':
                #self.sleep()
                self.health = 100
        
        # check item collisions-
        hits = pg.sprite.spritecollide(self.player, self.items, True)
        for hit in hits:
            hit.effect()
            
        if self.health > 100:
            self.health = 100
                
    def draw_grid(self):
        for x in range(0, stg.WIDTH, stg.TILESIZE):
            pg.draw.line(self.screen, stg.LIGHTGREY, (x, 0), (x, stg.HEIGHT))
        for y in range(0, stg.HEIGHT, stg.TILESIZE):
            pg.draw.line(self.screen, stg.LIGHTGREY, (0, y), (stg.WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        
        # blit rendered map and sprites to screen
        self.screen.fill(stg.BGCOLOR)
        self.current_map_img = self.current_map.make_map()
        self.current_map_rect = self.current_map_img.get_rect()
        if self.current_map_rect.height < stg.HEIGHT or self.current_map_rect.width < stg.WIDTH:
            self.screen.blit( pg.transform.scale(self.current_map_img,(stg.WIDTH,stg.HEIGHT)), (0,0))
        else:
            self.screen.blit(self.current_map_img, self.camera.apply_rect(self.current_map_rect))

        # draw player health
        draw_player_health(self.screen, 10, 10, self.health / stg.PLAYER_HEALTH)
        
        #draw npc messages
        if self.messages:
            for message in self.messages:
                self.screen.blit(message.display(), message.pos)
                message.display()
                
        # draw debug features     
        if self.draw_debug:           
            self.draw_grid()          
            for sprite in self.all_sprites:
                pg.draw.rect(self.screen, stg.RED, self.camera.apply_rect(sprite.hit_rect), 1)
                pg.draw.rect(self.screen, stg.BLUE, self.camera.apply_rect(sprite.rect), 1)
            for obs in self.obstacles:
                pg.draw.rect(self.screen, stg.RED, self.camera.apply_rect(obs.rect), 1)    
     
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.show_pause_screen()
                if event.key == pg.K_z:
                    self.equipment = 'melee'
                    self.player.equipment = 'melee'
                    self.player.load_images()
                if event.key == pg.K_x:
                    self.equipment = 'range'
                    self.player.equipment = 'range'
                    self.player.load_images()
                              
    def check_connections(self):
        connection_collisions = pg.sprite.spritecollide(self.player,self.connections,False,False)
        if connection_collisions:
            print("Leaving : " +  stg.map_dict[ str(connection_collisions[0].start_map) ] )   
            print("Entering : " +  stg.map_dict[ str(connection_collisions[0].end_map) ] )             
            self.current_map = self.map_list[ int(connection_collisions[0].end_map)-1 ]
            self.current_map_img = self.current_map.make_map()
            self.current_map_rect = self.current_map_img.get_rect()           
            self.new_map(self.map_list[ int(connection_collisions[0].end_map)-1 ])   
            
            for cnct in self.connections:
                if cnct.start_map == connection_collisions[0].end_map and cnct.end_map == connection_collisions[0].start_map \
                and cnct.start_door == connection_collisions[0].end_door and cnct.end_door == connection_collisions[0].start_door:
                    if cnct.orientation == 'E':
                        self.player = Player(self, cnct.rect.centerx+30, cnct.rect.centery)
                        print("player_spawned")
                        break
                    elif cnct.orientation == 'W':
                        self.player = Player(self, cnct.rect.centerx-30, cnct.rect.centery)
                        print("player_spawned")
                        break
                    elif cnct.orientation == 'N':
                        self.player = Player(self, cnct.rect.centerx, cnct.rect.centery-30)
                        print("player_spawned")
                        break
                    elif cnct.orientation == 'S':
                        self.player = Player(self, cnct.rect.centerx, cnct.rect.centery+30)
                        print("player_spawned")
                        break
                    
            self.player.equipment = self.equipment
            self.player.load_images()         
    
    def show_start_screen(self):  
        menu = Start_Menu(self,stg.WIDTH,stg.HEIGHT)
        self.save_file_num = 0    
        while self.save_file_num == 0:
            self.dt = self.clock.tick(stg.FPS) / 1000.0
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_o:
                        self.create_account()           
            self.screen.blit(menu.make_menu(), (0,0))          
            pg.display.flip()
        self.continue_sound.play()        
        self.save_file = 'save_state{}.txt'.format(self.save_file_num)
        print(self.save_file)
        self.load_save_file(self.save_file)
            
    def show_go_screen(self):
        self.gameover_sound.play()
        try:
            pg.mixer.music.load(path.join(self.snd_folder,"gameover_music.wav"))
            pg.mixer.music.play(-1)
        except:
            print("Gameover music failed to load")
        menu = Gameover_Menu(self,stg.WIDTH,stg.HEIGHT)
        self.is_paused = True
        while self.is_paused:
            self.dt = self.clock.tick(stg.FPS) / 1000.0
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
            self.screen.blit(menu.make_menu(), (0,0))
            pg.display.flip()
        self.continue_sound.play()
    
    def show_pause_screen(self):
        menu = Pause_Menu(self,stg.WIDTH,stg.HEIGHT)
        self.pause_sound.play()
        self.is_paused = True
        while self.is_paused:
            self.dt = self.clock.tick(stg.FPS) / 1000.0
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.is_paused = False
            self.screen.blit(menu.make_menu(), (0,0))
            pg.display.flip()
        self.pause_sound.play()
            
    def save(self):    
         with open(path.join(self.dir,self.save_file), 'w') as f:
                f.write("Account: " + self.account_name + "\n" +
                        "Current_map:" + str(self.current_map.map_num) + "\n" +
                        "x-coordinate:" + str(int(self.player.pos.x)) + "\n" +
                        "y-coordinate:" + str(int(self.player.pos.x)) + "\n" +
                        "Level:" + str(self.level) + "\n" +
                        "Experience:" + str(self.experience) + "\n" +
                        "Health:" + str(self.health) + "\n" +
                        "Melee Equipment Level:" + str(self.melee_equipment_level) + "\n" +
                        "Range Equipment Level:" + str(self.range_equipment_level) + "\n"
                        )
         self.save_sound.play()
         print("GAME SAVED")
         
    def load_save_file(self,save_file):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir,save_file), 'r') as f:
            try:
                lines = f.readlines()
                new_lines = []
                for line in lines:
                    line.strip("\n")
                    line = line.split(":")[1]
                    new_lines.append(line)
                self.account_name = new_lines[0]
                self.spawn_map = self.map_list[int(new_lines[1])-1]
                self.spawn_location = (int(new_lines[2]),int(new_lines[3]))  
                self.level = int(new_lines[4])
                self.experience = int(new_lines[5])
                self.health = int(new_lines[6])
                self.melee_equipment_level = int(new_lines[7])
                self.range_equipment_level = int(new_lines[8])
                print("Save file load successful")
            except:
                self.account_name = "name"
                self.spawn_map = self.map_list[0]
                self.spawn_location = (200,200)
                self.level = 1
                self.experience = 0
                self.health = 100
                self.melee_equipment_level = 1
                self.range_equipment_level = 1
                print("Save file load failed")
        
    def create_account(self):
        self.dir = path.dirname(__file__)
        menu = Create_Account_Menu(self,stg.WIDTH,stg.HEIGHT)
        self.valid_account_creation = False
        while not self.valid_account_creation:
            self.dt = self.clock.tick(stg.FPS) / 1000.0
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            
            self.screen.blit(menu.make_menu(), (0,0))
            
            (output) = menu.handle_action()
            if output != (None,None):
                if output[0] == None:
                    select_file = output[1]
                    print("select file " + str(select_file))
                if output[1] == None:
                    new_account_name = output[0]
                    print(new_account_name)

            if self.valid_account_creation == True:
                try:
                    print("File: " + str(select_file))
                    print("Account Name: " + new_account_name)
                except:
                    self.valid_account_creation = False                       
            pg.display.flip()

        if self.valid_account_creation == True:
            new_current_map = 1
            new_x_pos = 200
            new_y_pos = 200
            new_level = 1
            new_experience = 0
            new_health = 1
            new_melee_equipment_level = 100
            new_range_equipment_level = 100
           
            with open(path.join(self.dir,'save_state{}.txt'.format(select_file)), 'w') as f:
                     f.write("Account:" + new_account_name + "\n" +
                             "Current_map:" + str(new_current_map) + "\n" +
                             "x-coordinate:" + str(int(new_x_pos)) + "\n" +
                             "y-coordinate:" + str(int(new_y_pos)) + "\n" +
                             "Level:" + str(new_level) + "\n" +
                             "Experience:" + str(new_experience) + "\n" +
                             "Health:" + str(new_health) + "\n" +
                             "Melee Equipment Level:" + str(new_melee_equipment_level) + "\n" +
                             "Range Equipment Level:" + str(new_range_equipment_level) + "\n"
                             )
            
            self.valid_account_creation = False
            self.show_start_screen()
        
# create the game object
g = Game()
while True:
    g.new_game()#g.spawn_map)
    g.run()
    g.show_go_screen()

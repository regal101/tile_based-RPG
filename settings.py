import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

pg.font.init()
smallfont = pg.font.SysFont("calisto", 20) 
mediumfont = pg.font.SysFont("calisto", 40)
largefont = pg.font.SysFont("calisto", 60)
gameover_font = pg.font.SysFont("castellar", 50)

# game settings
WIDTH = int(640*1)   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = int(480*1)  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BLACK

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# paths
PAUSE_GUI_PATH = 'GUI\menu_GUI.png'
ARROW_IMG = 'arrow.png'
UNDEAD_SPRITES = 'undead.png'



# Game setting
SAVE_FILE = 'save_state.txt'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 80
PLAYER_HIT_RECT = pg.Rect(0, 0, 16, 16)
RANGE_BASE_POWER = 5
MELEE_BASE_POWER = 10
BASE_ATTACK_RATE = 500

range_equipment_stats = { "1" : [0,0,350],
                        "2" : [5,2,500],
                        "3" : [10,4,650]
                        }
melee_equipment_stats = { "1" : [5,2],
                        "2" : [10,4],
                        "3" : [15,6]
                        }

# Arrow settings
ARROW_SPEED = 500
ARROW_LIFETIME = 750
ARROW_RATE = 500
ARROW_HIT_RECT = pg.Rect(0, 0, 10, 10)

STRIKE_DAMAGE = 15


# Mob settings
MILITIA_HIT_RECT = pg.Rect(0,0,15,20)


######## ITEM SETTINGS ###########
item_sprite_paths = { "health_small" : "items\health_small.png",
                      "health_medium" : "items\health_medium.png",
                      "health_large" : "items\health_large.png"
                     }




######### MAP SETTINGS ###########
map_dict = { "1": "start_map",
            "2": "field",
            "3": "start_map - house 1", 
            "4": "meadows",
            "5": "map_4 - cave",
            "6": "castle walkway",
            "7": "desert town"
            
           }

map_music = {"start_map" : "TownTheme.mp3",
             "field": "adventure_music1.mp3",
             "meadows": "adventure_music1.mp3",
             "map_4 - cave" : "eery_cave_music.mp3"
             }





############ MOB SETTINGS #############
#health,damage,attack rate,speed,defense
mob_stats = {"Knight" : [100,5,800,60,0],
             "Champion" : [50,3,800,30,0],
             "Militia" : [20,2,800,30,0],
             "Villager" : [10,0,0,30,0],
             "Demon" : [250,20,1600,35,0],
             "Mummy" : [50,20,1000,30,0],
             "Zombie" : [50,20,1000,30,0]
             }

mob_exp = {"Militia" : 10,
           "Champion": 50,
           "Knight" : 50,
           "Demon" : 500,
           "Mummy": 200,
           "Zombie" : 200
           }

drop_rates = {"Militia" : [("health_small",0.1)],
           "Champion": [("health_small",1)],
           "Knight" : [("health_small",0.1)],
           "Demon" : [("health_small",0.1)],
           "Mummy": [("health_small",0.1)],
           "Zombie" : [("health_small",0.1)],
           }

mob_frame_rates = {"Knight" : 60,
                   "Champion" : 80,
                   "Militia" : 80,
                   "Manarms" : 80,
                   "Farm" : 80,
                   "Fishing" : 80,
                   "Mummy": 250,
                   "Zombie": 250
                   }

number_of_frames = {"Militia stand": 6, "Militia walk": 12, "Militia attack": 10, "Militia die" : 10,
                    "Champion stand": 10, "Champion walk": 10, "Champion attack": 10, "Champion die" : 10,
                    "Knight stand": 10, "Knight walk": 10, "Knight attack": 10, "Knight die" : 10,
                    "Archer stand": 10, "Archer walk": 10, "Archer attack": 10, "Archer die" : 10,
                    "Villager stand": 15, "Villager walk": 15, "Villager attack": 15, "Villager die" : 15,
                    "Farm stand": 15, "Farm walk": 15, "Farm act": 16, "Farm die" : 15,
                    "Fishing stand": 15, "Fishing walk": 15, "Fishing act": 28, "Fishing die" : 15,
                    "Manarms stand": 11, "Manarms walk": 11, "Manarms attack": 11, "Manarms die" : 11,
                    }

mob_spawn_sounds = {"Knight" : "spawn_sounds\horse_sound.wav",
                    "Champion" : "",
                    "Militia" : "",
                    "Mummy" : "spawn_sounds\mummy_sound.wav",
                    "Zombie" : "spawn_sounds\zombie_sound.wav"
                    }

npc_data = {"1" : [[ "Farmer1","Farm",vec(1,0),"Farmer: Hola"]],
            "4" : [["Fisher1","Fishing", vec(1,0),"hi"]]
                       
           }


Undead_spritesheet_coords = { "Mummy" : [
                                         (306,122,30,33),(242,122,30,33),(274,122,30,33),
                                         (338,122,30,33),(370,122,30,33),(407,122,30,33),
                                         (535,122,30,33),
                                         (306,157,30,33),(242,157,30,33),(274,157,30,33),
                                         (338,157,30,33),(370,157,30,33),(407,157,30,33),
                                         (535,157,30,33),
                                         (306,192,30,33),(242,192,30,33),(274,192,30,33),
                                         (338,192,30,33),(370,192,30,33),(407,192,30,33),
                                         (535,192,30,33)
                                        ],
                              "Zombie" : [
                                         (306,10,30,33),(242,10,30,33),(274,10,30,33),
                                         (338,10,30,33),(370,10,30,33),(407,10,30,33),
                                         (535,10,30,33),
                                         (306,44,30,33),(242,44,30,33),(274,44,30,33),
                                         (338,44,30,33),(370,44,30,33),(407,44,30,33),
                                         (535,44,30,33),
                                         (306,78,30,33),(242,78,30,33),(274,78,30,33),
                                         (338,78,30,33),(370,78,30,33),(407,78,30,33),
                                         (535,78,30,33)
                                        ]
                            }


########### Math ##############
invsqrt2 = 0.7071

directions = [vec(0,1),vec(-0.7071,0.7071),vec(-1,0),vec(-0.7071,-0.7071),
              vec(0,-1),vec(0.7071,-0.7071),vec(1,0),vec(0.7071,0.7071),]








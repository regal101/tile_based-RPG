import pygame as pg
import settings as stg
import sys
from os import path
from utilities import Spritesheet, draw_text, TextInput

def text_objects(text = "default" , colour = stg.BLACK,size = "small"):
    if size == "small":
        textSurface = stg.smallfont.render(text, True, colour)
    elif size == "medium":
        textSurface = stg.mediumfont.render(text, True, colour)
    elif size == "large":
        textSurface = stg.largefont.render(text, True, colour)
    return textSurface,textSurface.get_rect() 

def text_to_button(surface, msg,colour,buttonX,buttonY,buttonWidth,buttonHeight,size = "small"):
    textSurf, textRect = text_objects(msg,colour,size)
    textRect.center = buttonX+(buttonWidth/2), buttonY+(buttonHeight/2)
    surface.blit(textSurf,textRect)

def button(game, surface, x, y, image1, image2, text, action):   
    cursor_pos = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()   
    rect = image1.get_rect()    
    if x + rect.width > cursor_pos[0] > x and y + rect.height > cursor_pos[1] > y:
        surface.blit(image2,(x,y))
        if click[0] == 1:
            return action           
    else:
        surface.blit(image1,(x,y))
        pass
    text_to_button(surface,text,stg.BLACK,x,y,rect.width,rect.height)

class message_box:
    def __init__(self,msg,colour,boxX,boxY,size = "small"):
        self.pos = (boxX,boxY)
        self.textSurf, self.textRect = text_objects(msg,colour,size)
  
    def display(self):
        temp_surface = pg.Surface((self.textRect.width, self.textRect.height))
        temp_surface.set_colorkey(stg.BLACK)
        temp_surface.blit(self.textSurf,(0,0))
        return temp_surface
   
class Gameover_Menu:
    def __init__(self,game, width, height):
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_folder,stg.PAUSE_GUI_PATH))
        self.width = width
        self.height = height
        self.load_images()

    def load_images(self):
        self.background_image = pg.image.load(path.join(self.game.img_folder, "GUI\GUI_background.png"))
        self.background_image = pg.transform.scale(self.background_image,(self.width,self.height))       
        self.button_1_up = self.spritesheet.get_image(13,124,287,59,1.5*640/stg.WIDTH)
        self.button_1_up.set_colorkey(stg.BLACK)
        self.button_1_down = self.spritesheet.get_image(13,204,287,59,1.5*640/stg.WIDTH)
        self.button_1_down.set_colorkey(stg.BLACK)
        
    def render(self,surface):
        surface.blit(self.background_image,(0,0))        
        self.button_presses = []
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.55),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Exit", 2))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.1),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Load Save", 1))

        draw_text(surface,"GAME OVER", stg.BLACK,300,200, stg.gameover_font)        
        self.handle_action()
        
    def handle_action(self):
        for action in self.button_presses:
            if action != None:
                if action == 1:
                        self.game.is_paused = False
                if action == 2:
                        self.game.quit()
                    
    def make_menu(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Pause_Menu:
    def __init__(self,game, width, height):
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_folder,stg.PAUSE_GUI_PATH))
        self.width = width
        self.height = height
        self.load_images()

    def load_images(self):
        self.background_image = pg.image.load(path.join(self.game.img_folder, "GUI\GUI_background.png"))
        self.background_image = pg.transform.scale(self.background_image,(self.width,self.height))        
        self.button_1_up = self.spritesheet.get_image(13,124,287,59,1.5*640/stg.WIDTH)
        self.button_1_up.set_colorkey(stg.BLACK)
        self.button_1_down = self.spritesheet.get_image(13,204,287,59,1.5*640/stg.WIDTH)
        self.button_1_down.set_colorkey(stg.BLACK)
        self.icon_outline1 = pg.image.load(path.join(self.game.img_folder, "icon_outline1.png"))
        self.icon_outline1.set_colorkey(stg.WHITE)
        self.icon_outline2 = pg.image.load(path.join(self.game.img_folder, "icon_outline2.png"))
        self.icon_outline2.set_colorkey(stg.WHITE)
        self.icon_outline3 = pg.image.load(path.join(self.game.img_folder, "icon_outline3.png"))
        self.icon_outline3.set_colorkey(stg.WHITE)
        self.melee1_icon = pg.image.load(path.join(self.game.img_folder, "Melee1_icon.png"))
        self.melee1_icon.set_colorkey(stg.WHITE)
        self.melee2_icon = pg.image.load(path.join(self.game.img_folder, "Melee2_icon.png"))
        self.melee2_icon.set_colorkey(stg.WHITE)
        self.range1_icon = pg.image.load(path.join(self.game.img_folder, "Range1_icon.png"))
        self.range1_icon.set_colorkey(stg.WHITE)
        self.range2_icon = pg.image.load(path.join(self.game.img_folder, "Range2_icon.png"))
        self.range2_icon.set_colorkey(stg.WHITE)

        
    def render(self,surface):
        surface.blit(self.background_image,(0,0))
        surface.blit(self.icon_outline1,(40,100))     
        surface.blit(self.icon_outline2,(40,160))    
        surface.blit(self.icon_outline3,(40,220))
        surface.blit(self.icon_outline1,(102,100))     
        surface.blit(self.icon_outline2,(102,160))    
        surface.blit(self.icon_outline3,(102,220))
        if self.game.melee_equipment_level == 2:
            surface.blit(self.melee1_icon,(40,100))  
            surface.blit(self.melee2_icon,(40,160))  
        
        if self.game.range_equipment_level == 1:
            surface.blit(self.range1_icon,(102,100))
        elif self.game.range_equipment_level == 2:
            surface.blit(self.range1_icon,(102,100))
            surface.blit(self.range2_icon,(102,160)) 
            
        self.button_presses = []
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.55),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Resume", 2))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.1),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Save", 1))
        
        draw_text(surface,"lvl: " + str(self.game.level), stg.BLACK,30,10, stg.smallfont)
        draw_text(surface,"XP: " + str(self.game.experience), stg.BLACK,45,40, stg.smallfont )
        draw_text(surface, self.game.account_name, stg.BLACK,stg.WIDTH/2,40, stg.smallfont )     
        self.handle_action()
        
    def handle_action(self):
        for action in self.button_presses:
            if action != None:
                if action == 1:
                        self.game.save()                     
                if action == 2:
                        self.game.is_paused = False
                        
    def make_menu(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface  

class Start_Menu:
    def __init__(self,game, width, height):
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_folder,stg.PAUSE_GUI_PATH))
        self.width = width
        self.height = height
        self.load_images()       
        self.account_names = []
        self.dir = path.dirname(__file__)
        for i in range(1,4):
            with open(path.join(self.dir,'save_state{}.txt'.format(i)), 'r') as f:
                try:
                    line = f.readline()
                    line.strip("\n")
                    line = line.split(":")[1]
                    self.account_names.append(line)
                except:
                    print("Error Loading file name in start menu")
                    
    def load_images(self):
        self.background_image = pg.image.load(path.join(self.game.img_folder, "GUI\GUI_background.png"))
        self.background_image = pg.transform.scale(self.background_image,(self.width,self.height))       
        self.button_1_up = self.spritesheet.get_image(13,124,287,59,1.5*640/stg.WIDTH)
        self.button_1_up.set_colorkey(stg.BLACK)
        self.button_1_down = self.spritesheet.get_image(13,204,287,59,1.5*640/stg.WIDTH)
        self.button_1_down.set_colorkey(stg.BLACK)
        
    def render(self,surface):
        surface.blit(self.background_image,(0,0))        
        self.button_presses = []
        account_index = 1
        button1_pos = int(stg.HEIGHT*0.25)
        for account_name in self.account_names:
            self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.2),button1_pos*account_index,
                                 self.button_1_up, self.button_1_down, account_name, account_index))
            account_index += 1
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.70),int(stg.HEIGHT*0.75),
                             self.button_1_up, self.button_1_down, "New Game", 4))        
        self.handle_action()
        
    def handle_action(self):
        print(self.button_presses)
        for action in self.button_presses:
            if action == 1 or action == 2 or action == 3:
                self.game.save_file_num = action  
                action = None
            if action == 4:
                self.game.create_account()
                action = None
                return
                
    def make_menu(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface 

class Create_Account_Menu:
    def __init__(self,game, width, height):
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_folder,stg.PAUSE_GUI_PATH))
        self.width = width
        self.height = height
        self.load_images()
        self.account_name_input = TextInput()
                            
    def load_images(self):
        self.background_image = pg.image.load(path.join(self.game.img_folder, "GUI\GUI_background.png"))
        self.background_image = pg.transform.scale(self.background_image,(self.width,self.height))      
        self.button_1_up = self.spritesheet.get_image(13,124,287,59,1.5*640/stg.WIDTH)
        self.button_1_up.set_colorkey(stg.BLACK)
        self.button_1_down = self.spritesheet.get_image(13,204,287,59,1.5*640/stg.WIDTH)
        self.button_1_down.set_colorkey(stg.BLACK)
        
    def render(self,surface):
        surface.blit(self.background_image,(0,0))       
        self.button_presses = []
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.35),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Create", 1))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.01),int(stg.HEIGHT*0.5),
                             self.button_1_up, self.button_1_down, "Account 1", 2))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.35),int(stg.HEIGHT*0.5),
                             self.button_1_up, self.button_1_down, "Account 2", 3))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.70),int(stg.HEIGHT*0.5),
                             self.button_1_up, self.button_1_down, "Account 3", 4))
        self.button_presses.append(button(self.game, surface, int(stg.WIDTH*0.01),int(stg.HEIGHT*0.8),
                             self.button_1_up, self.button_1_down, "Back", 5))
        draw_text(surface,"Enter an account name and press return", stg.BLACK,stg.WIDTH/2,100, stg.smallfont )
        draw_text(surface,"Select an account to overwrite", stg.BLACK,stg.WIDTH/2,200, stg.smallfont )
        
    def handle_action(self):
        
        new_account_name = None
        select_file = None
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.game.quit()       
        if self.account_name_input.update(events):
            print("account name set")
            new_account_name = self.account_name_input.get_text() 
        for action in self.button_presses:
            if action != None: 
                if action == 2:
                    print("1")
                    select_file = 1
                if action == 3:
                    select_file = 2
                    print("2")
                if action == 4:
                    select_file = 3
                    print("3")
                if action == 5:
                    self.game.show_start_screen()  
                if action == 1:
                    self.game.valid_account_creation = True     
        return (new_account_name, select_file) 
                   
    def make_menu(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        temp_surface.blit(self.account_name_input.get_surface(), (stg.WIDTH*0.4,150))
        return temp_surface        
import pygame, sys, time,math,random
import numpy as np
from collections import deque


class Tile:

    def __init__(self, texture, pos, solid=False,stump = False):
        self.x = pos[0]
        self.y = pos[1]
        self.texture = pygame.transform.scale_by(texture,5)
        self.solid = solid
        self.is_stump = stump
        self.rect = pygame.Rect(self.x,self.y-.067*self.texture.get_height(),self.texture.get_width(),self.texture.get_height())
        self.rect = pygame.Rect.scale_by(self.rect,.63)
        if self.is_stump:
            self.rect = pygame.Rect.scale_by(self.rect,.5,1)
        #self.rect.center = (self.x+self.texture.get_width()/2,self.y+self.texture.get_height()/2)

    def draw_tile(self,window):
        window.blit(self.texture,(self.x,self.y))
        #pygame.draw.rect(window,"red",self.rect)

class Spawn_Tile(Tile):
    def __init__(self,pos,solid=False):
        super().__init__(pygame.image.load("Environment Tiles\Water\WaterAnim1.png"),pos,solid)
        self.current_frame = 0
        self.water_animation = [pygame.image.load("Environment Tiles\Water\WaterAnim1.png"),pygame.image.load("Environment Tiles\Water\WaterAnim2.png"),
                           pygame.image.load("Environment Tiles\Water\WaterAnim3.png"),pygame.image.load("Environment Tiles\Water\WaterAnim4.png")]
    
    def animate_water(self):
        if self.current_frame >= len(self.water_animation)*15-1:
            self.current_frame = 0
        
        self.texture = pygame.transform.scale_by(self.water_animation[math.floor(self.current_frame/15)],10)


        self.current_frame += 1
        
class Tile_Manager:

    def __init__(self):
        self.tile_array = np.zeros((6,8))
        self.tile_queue = deque()
        self.spawner_tile = []
        self.solid_tile_queue = deque()
        self.solid_tile_dic = {
            1:pygame.image.load("Environment Tiles\Rock2.png"),
            2:pygame.image.load("Environment Tiles\Trees\Branch.png"),
            3:pygame.image.load("Environment Tiles\Trees\Tree1.png"),
            4:pygame.image.load("Environment Tiles\Trees\Tree2.png"),
            
        }
        self.liquid_tile_dic = {
            5:pygame.image.load("Environment Tiles\Dark Grass 2x tile.png"),
            6:pygame.image.load("Environment Tiles\Dirt.png"),
            7:pygame.image.load("Environment Tiles\Trees\Treeshadow.png"),
            8:pygame.image.load("Environment Tiles\Flowers\\tile001.png"),
            9:pygame.image.load("Environment Tiles\Flowers\\tile002.png"),

        }

    def custom_map(self,width,height):
        x_index = 0
        y_index = 0
        ar=np.array([[5,5,5,0,8,5,5,5],
                     [5,3,0,8,0,6,3,5],
                     [0,9,4,1,0,9,0,0],
                     [0,2,0,8,2,0,2,8],
                     [0,0,2,0,0,1,0,9],
                     [10,10,10,10,10,10,10,10]])

        for x in ar:
            y_index = 0
            for y in x:
                if y in range(1,5):
                    if y == 2:
                        self.solid_tile_queue.appendleft(Tile(self.solid_tile_dic[y],(width*y_index,height*x_index),True, True))
                        y_index += 1
                    else:
                        self.solid_tile_queue.appendleft(Tile(self.solid_tile_dic[y],(width*y_index,height*x_index),True))
                        y_index += 1
                elif y == 0:
                    y_index += 1
                    continue
                elif y == 10:
                    self.spawner_tile.append(Spawn_Tile((width*y_index,height*x_index),True))
                    y_index += 1
                else:
                    self.tile_queue.append(Tile(self.liquid_tile_dic[y],(width*y_index,height*x_index),False))
                    y_index += 1
            x_index += 1
    
    def draw_liquidtiles(self,window):
        for x in range(len(self.tile_queue)):
            self.tile_queue[0].draw_tile(window)
            temp = self.tile_queue.pop()
            self.tile_queue.appendleft(temp)
    
    def draw_solidtiles(self,window):
        for x in range(len(self.solid_tile_queue)):
            self.solid_tile_queue[0].draw_tile(window)
            #pygame.draw.rect(window,"red",self.solid_tile_queue[0].rect)
            temp = self.solid_tile_queue.pop()
            self.solid_tile_queue.appendleft(temp)

    def player_tile_collision(self,player,dt):
        for x in range(len(self.solid_tile_queue)):
            player.tile_collision(self.solid_tile_queue[0],dt)
            temp = self.solid_tile_queue.pop()
            self.solid_tile_queue.appendleft(temp)

    def enemy_tile_collision(self,enemies,dt):
        for x in range(len(self.solid_tile_queue)):
            for y in enemies.enemy_array:
                y.tile_collision(self.solid_tile_queue[0],dt)
                temp = self.solid_tile_queue.pop()
                self.solid_tile_queue.appendleft(temp)
    
    def random_map(self,width,height):
        x_index = 0
        y_index = 0
        tiles_placed = 0
        spawner_tiles_placed = 0
        for x in self.tile_array:
            y_index = 0
            for y in x:
                if bool(random.getrandbits(1)) and tiles_placed < 14:
                    random_tile = random.choice(list(self.solid_tile_dic.items()))[1]
                    liquid_tile = random.choice(list(self.liquid_tile_dic.items()))[1] 
                    self.solid_tile_queue.appendleft(Tile(random_tile,(width*y_index,height*x_index),True))
                    #self.tile_queue.append(Tile(liquid_tile,(width*y_index,height*x_index),False))
                    tiles_placed += 1
                    y_index += 1
                    continue
                if bool(random.getrandbits(1)) and spawner_tiles_placed < 4:
                    self.spawner_tile.append(Spawn_Tile((width*y_index,height*x_index),True))
                y_index += 1
            x_index += 1
    
    def animate_spawn_tiles(self,window):
        for x in self.spawner_tile:
            x.animate_water()
            x.draw_tile(window)
        
#random_tile = random.choice(list(self.solid_tile_dic.items()))[1]
#liquid_tile = random.choice(list(self.liquid_tile_dic.items()))[1]
#self.solid_tile_queue.appendleft(Tile(random_tile,(width*y_index_list[x],height*x_index_list[x]),True))
#self.tile_queue.append(Tile(liquid_tile,(width*y_index_list[x],height*x_index_list[x]),False))
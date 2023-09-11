from player import Player
import pygame, sys, time,random,threading,math


class Enemy(Player):
    
    def __init__(self,x,y,status = "uninjured"):
        super().__init__(x,y,status)
        self.texture = pygame.image.load("Enemy Sprites\Idle\Frame1.png")
        self.texture = pygame.transform.scale_by(self.texture,4)
        self.injury_animation = [pygame.image.load("Enemy Sprites\Hit\Frame1.png"),
        pygame.image.load("Enemy Sprites\Hit\Frame2.png"), pygame.image.load("Enemy Sprites\Hit\Frame3.png")]
        self.walk_animation = [pygame.image.load("Enemy Sprites\Movement\Walk\Frame1.png"),
            pygame.image.load("Enemy Sprites\Movement\Walk\Frame2.png"), pygame.image.load("Enemy Sprites\Movement\Walk\Frame3.png"), 
            pygame.image.load("Enemy Sprites\Movement\Walk\Frame4.png"),pygame.image.load("Enemy Sprites\Movement\Walk\Frame5.png")
            ,pygame.image.load("Enemy Sprites\Movement\Walk\Frame6.png")]
        self.sprint_animation = [pygame.image.load("Enemy Sprites\Movement\Run\Frame1.png"),pygame.image.load("Enemy Sprites\Movement\Run\Frame2.png"),pygame.image.load("Enemy Sprites\Movement\Run\Frame3.png"),
                                 pygame.image.load("Enemy Sprites\Movement\Run\Frame4.png"),pygame.image.load("Enemy Sprites\Movement\Run\Frame5.png"),pygame.image.load("Enemy Sprites\Movement\Run\Frame6.png"),
                                 pygame.image.load("Enemy Sprites\Movement\Run\Frame7.png")]
        self.max_health = 3
        self.health_points = 3
        self.spawned = False
        self.default_speed = 125
        self.speed = self.default_speed
        self.aoe = self.rect
        self.lunge_direction = None
        self.sprinting_modifier = 1.35
        self.cooldown = 0
        self.aoe = pygame.Rect.scale_by(self.rect,4)

    def draw_enemy(self, window,):
        super().draw_player(window)
        self.draw_healthbar(window)
        #pygame.draw.rect(window,"blue", self.aoe)
        #pygame.draw.rect(window,"red", self.rect)
    
    
    #Decides a random direction for the enemy to move (not in use)
    def rand_move_direct(self):
        #TODO: make it so that it can't move in the direction of the wall its facing
        if self.movedict["move_north"]:
            self.movedict["move_north"] = False
        if self.movedict["move_south"]:
            self.movedict["move_south"] = False
        if self.movedict["move_east"]:
            self.movedict["move_east"] = False
        if self.movedict["move_west"]:
            self.movedict["move_west"] = False
        direct = random.choice(list(self.movedict.items()))[0]
        self.movedict[direct] = True
    
    def in_aoe_range(self,player):
        if self.aoe.colliderect(player.rect):
            return True
        else:
            return False

    def stop_movement(self):
        for x in self.movedict.keys():
            self.movedict[x] = False
    
    def set_lunge_direction(self,player):
        #TODO: make it angle from center of animation not top right
        (dx,dy) = (self.center[0]-player.center[0]),(self.center[1]-player.center[1])
        self.lunge_direction = math.degrees(math.atan(dy/dx))
        self.current_move = 0
        self.lunging == True
        if player.center[0] - self.center[0] < 0:
            self.lunge_direction += 180
        self.lunge(player)
    
    #WIP, probably wont be finished tbh
    def lunge(self,dt):
        if self.cooldown == 0:
            if self.current_move <= len(self.sprint_animation):
                self.sprinting == True
                self.x += math.cos(math.radians(self.lunge_direction))*self.speed*dt
                self.y += math.sin(math.radians(self.lunge_direction))*self.speed*dt
            else:
                self.lunging == False
                self.cooldown = 10000
    
    def chase_player(self,player):
        self.sprinting = False
        if player.x > self.x:
            self.movedict["move_east"] = True
            self.movedict["move_west"] = False
        if player.x < self.x:
            self.movedict["move_west"] = True
            self.movedict["move_east"] = False
        if player.y < self.y:
            self.movedict["move_north"] = True
            self.movedict["move_south"] = False
        if player.y > self.y+self.texture.get_height():
            self.movedict["move_south"] = True
            self.movedict["move_north"] = False
    
    def chase_player_sprinting(self,player):
        self.chase_player(player)
        self.sprinting = True
    
    def set_sprinting(self,bool):
        self.sprinting = bool
    
    def update_player_texture(self):
        super().update_player_texture()

    def set_default_texture(self):
        self.texture = pygame.transform.scale_by(pygame.image.load("Enemy Sprites\Idle\Frame1.png"),4)

    def detect_player_hit(self, projectile):
        if self.rect.colliderect(projectile.rect) and (self.status == "uninjured"):
            self.health_points -= 1
            self.status = "injured"
            projectile.active = False

    def statusupdater(self):
        super().statusupdater()
    

    #updates the position of the player model, dependent on the dt or delta time of the window
    def update_char(self):    
       super().update_char()
       self.aoe = pygame.Rect.scale_by(self.rect,3)
       self.rect = self.rect.scale_by(.9,.7)
       if self.cooldown <0:
           self.cooldown -= 1
    
    #detects if player is out of bounds
    def outofbounds(self,width,height):
        super().outofbounds(width,height-20)

    def draw_healthbar(self,window):
        n = 0
        for x in range(0,self.health_points):
            rect = pygame.Rect(self.x+n,self.y+self.texture.get_height()+10,int(self.texture.get_width()/3),9)
            pygame.draw.rect(window,"red",rect)
            n+=int(self.texture.get_width()/3)
        border_rect = pygame.Rect(self.x,self.y+self.texture.get_height()+10,self.texture.get_width(),9)
        pygame.draw.rect(window,"black",border_rect, 2)
    
    def spawn_animation(self,window,n):
            if self.spawned == False:
                img = pygame.transform.scale_by(self.texture,n)
                window.blit(img,img.get_rect())
            if n >= 1:
                self.spawned = True
                print("Spawned")

    def tile_collision(self, tile, dt):
        step = round(self.speed*dt)
        temp = self.rect.copy().move(-step,0)
        if temp.colliderect(tile.rect):
            self.movedict["move_west"] = False
            self.x + round(self.speed*self.sprinting_modifier*dt)
        temp = self.rect.move(step,0)
        if temp.colliderect(tile.rect):
            self.movedict["move_east"] = False
            self.x - round(self.speed*self.sprinting_modifier*dt)
        temp = self.rect.move(0,-step)
        if temp.colliderect(tile.rect):
            self.movedict["move_north"] = False
            self.y + round(self.speed*self.sprinting_modifier*dt)
        temp = self.rect.move(0, step)    
        if temp.colliderect(tile.rect):
            self.movedict["move_south"] = False
            self.y - round(self.speed*self.sprinting_modifier*dt)


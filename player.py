import pygame, sys, time,math,Projectile_Manager


class Player:
    def __init__(self,x,y,status = "uninjured"):
        self.x = x
        self.y = y
        self.texture = pygame.image.load("Slime Survival\Player Sprites\move0.png")
        self.texture = pygame.transform.scale_by(self.texture,4)
        self.walk_animation = [pygame.image.load("Slime Survival\Player Sprites\move3.png"),
            pygame.image.load("Slime Survival\Player Sprites\move4.png"), pygame.image.load("Slime Survival\Player Sprites\move5.png"), 
            pygame.image.load("Slime Survival\Player Sprites\move6.png"),pygame.image.load("Slime Survival\Player Sprites\move7.png")
            ,pygame.image.load("Slime Survival\Player Sprites\move8.png"),pygame.image.load("Slime Survival\Player Sprites\move9.png")]
        
        self.injury_animation = [pygame.image.load("Slime Survival\Player Sprites\injured1.png"),
        pygame.image.load("Slime Survival\Player Sprites\injured2.png"), pygame.image.load("Slime Survival\Player Sprites\injured3.png")]
        self.sprint_animation = [pygame.image.load("Slime Survival\Player Sprites\Frame2.png"),
            pygame.image.load("Slime Survival\Player Sprites\Frame3.png"),pygame.image.load("Slime Survival\Player Sprites\Frame4.png"), pygame.image.load("Slime Survival\Player Sprites\Frame5.png"),
            pygame.image.load("Slime Survival\Player Sprites\Frame6.png"),pygame.image.load("Slime Survival\Player Sprites\Frame7.png"),pygame.image.load("Slime Survival\Player Sprites\Frame8.png")]
        self.rect = self.texture.get_rect()
        self.status = status
        self.default_speed = 200
        self.current_attack = 0
        self.current_move = 0
        self.max_health = 5
        self.health_points = 5
        self.is_attacking = False
        self.direc_facing = 0
        self.center = (self.x+self.texture.get_width()/2,self.y+self.texture.get_height()/2)
        self.injury_counter = 0
        self.speed = self.default_speed
        self.sprinting_modifier = 2
        self.sprinting = False
        self.lunging = False
        self.movedict ={
        "move_north" :False,
        "move_south" : False,
        "move_east" :False,
        "move_west" :False
        }
        self.wallhit = {
            "north_wall": False,
            "south_wall": False,
            "east_wall": False,
            "west_wall": False
        }

    def draw_player(self, window):
        window.blit(self.texture,(self.x-self.rect.width*.1,self.y))
        #pygame.draw.rect(window,"blue",self.rect)

    def reset_player(self, x, y):
        self.x = x
        self.y = y
        self.health_points = self.max_health
        self.is_attacking = False
        self.is_sprinting = False
        self.injury_counter = 0

    def checkKeypress(self,event):
        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_s:
                self.movedict["move_south"] = True
            if event.key == pygame.K_a:
                self.movedict["move_west"] = True
            if event.key == pygame.K_d:
                self.movedict["move_east"] = True
            if event.key == pygame.K_w:
                self.movedict["move_north"] = True
        elif event.type == pygame.KEYUP:
            if  event.key == pygame.K_s:
                self.movedict["move_south"] = False
            if event.key == pygame.K_a:
                self.movedict["move_west"] = False
            if event.key == pygame.K_d:
                self.movedict["move_east"] = False
            if event.key == pygame.K_w:
                self.movedict["move_north"] = False
    
    def check_sprint_keypress(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                self.sprinting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                self.sprinting = False
    
    def update_player_texture(self):
        #updates player texture in accordance to frame of walk cycle
        if self.sprinting == True:
            if self.current_move >= len(self.sprint_animation)*4:
                self.current_move = 0
            else:
                if True in self.movedict.values():
                    self.texture = pygame.transform.scale_by(self.sprint_animation[math.floor(self.current_move/5)],4)
                    self.current_move += 1
                else:
                    self.set_default_texture()
        else:
            if self.current_move >= len(self.walk_animation)*5:
                self.current_move = 0
            else:
                if True in self.movedict.values():
                    self.texture = pygame.transform.scale_by(self.walk_animation[math.floor(self.current_move/5)],4)
                    self.current_move += 1
                else:
                    self.set_default_texture()
    
    
    def set_default_texture(self):
        self.texture = pygame.transform.scale_by(pygame.image.load("Slime Survival\Player Sprites\move0.png"),4)

    
    def statusupdater(self):
        if self.injury_counter >= len(self.injury_animation)*15:
            self.status = "uninjured"
        if self.status == "injured":
            self.texture = pygame.transform.scale_by(self.injury_animation[math.floor(self.injury_counter/15)],4)
            self.injury_counter += 1
            self.speed = self.default_speed*2

        else:
            if self.sprinting:
                self.speed = self.sprinting_modifier * self.default_speed
            else:
                self.injury_counter = 0
                self.speed = self.default_speed     


    #updates the position of the player model, dependent on the dt or delta time of the window
    def standard_position_update(self,dt):
            if(self.movedict["move_north"] and not self.wallhit["north_wall"]):
                self.y -= round(self.speed * dt)
            if(self.movedict["move_south"] and not self.wallhit["south_wall"]):
                self.y += round(self.speed * dt)
            if(self.movedict["move_east"] and not self.wallhit["east_wall"]):
                self.x += round(self.speed * dt)
            if(self.movedict["move_west"] and not self.wallhit["west_wall"]):
                self.x -= round(self.speed * dt)
    
    def update_char(self):
        self.update_player_texture()
        self.statusupdater()
        self.rect = pygame.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_width())
        self.rect = self.rect.scale_by(.55,.70)
        self.center = (self.x+self.rect.width/2,self.y+self.rect.height/2)
        for x in self.wallhit:
            self.wallhit[x] = False



    def body_collision(self,enemy_rect):
        if self.rect.colliderect(enemy_rect) and self.status != "injured":
            self.status = "injured"
            self.health_points -= 1
    
    def tile_collision(self,tile,dt):
        step = round(self.speed*dt)
        temp = self.rect.copy().move(-step,0)
        if temp.colliderect(tile.rect):
            self.wallhit["west_wall"] = True        
        temp = self.rect.copy().move(step,0)
        if temp.colliderect(tile.rect):
            self.wallhit["east_wall"] = True        
        temp = self.rect.copy().move(0,-step)
        if temp.colliderect(tile.rect):
            self.wallhit["north_wall"] = True     
        temp = self.rect.copy().move(0, step)    
        if temp.colliderect(tile.rect):
            self.wallhit["south_wall"] = True

    #detects if player is out of bounds
    def outofbounds(self,width,height):
    #static number 50 should be variable of player dimensions
        if self.x <= 0:
            self.x = 0
        if self.y <= 0:
            self.y = 0
        if self.x+self.texture.get_width() >= width:
            self.x = width - self.texture.get_width()
        if self.y+self.texture.get_height() >= height:
            self.y = height - self.texture.get_height()

    #Detects when the mouse button is pressed. and then tells the attack function
    #to begin the attack animation, in the specified angle of rotation.

    def attack_pressed(self,event,projectiles,dt):
        if event.type == pygame.MOUSEBUTTONDOWN and self.injury_counter == 0 and self.sprinting == False:
            pos = pygame.mouse.get_pos()
            #TODO: make it angle from center of animation not top right
            (dx,dy) = (pos[0]-self.center[0]),(self.center[1]-pos[1])
            dx += 0.1
            self.direc_facing = math.degrees(math.atan(dy/dx))
            if pos[0] - self.center[0] < 0:
                self.direc_facing += 180
            projectiles.spawn_projectile(self.x,self.y,self.direc_facing,dt)

        

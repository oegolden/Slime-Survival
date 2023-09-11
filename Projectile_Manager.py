import pygame, math, random, os
speed = 800
class Projectiles:

    def __init__(self):
        self.proj_array = []

    def spawn_projectile(self,x,y,direc_facing,dt):
        self.proj_array.append(Projectile(x,y,direc_facing,dt))
    
    def despawn_projectiles(self,width,height):
        for x in self.proj_array:
            if x.outofbounds(width,height) or not x.active:
                self.proj_array.remove(x)
            if x.time == 0:
                try:
                    self.proj_array.remove(x)
                except:
                    continue
    
    def draw_projectiles(self,window):
        for x in self.proj_array:
            x.draw(window)

    def update(self):
        for x in self.proj_array:
            x.update()

class Projectile:

    def __init__(self,x,y,direc_facing,dt):
        self.x = x
        self.y = y
        self.vel = (speed*math.cos(math.radians(direc_facing))*dt, speed*math.sin(math.radians(direc_facing))*dt)
        self.current_frame = 0
        self.texture = pygame.transform.scale_by(pygame.image.load("Projectile Animations\m1.png"),5)
        self.rect = pygame.Rect(self.x,self.y,self.texture.get_width(),self.texture.get_height())
        self.direc_facing = direc_facing
        self.active = True
        self.time = 40

    def update(self):
        self.x += self.vel[0]
        self.y -= self.vel[1]
        self.projectile_animation()
        self.rect = pygame.Rect(self.x,self.y,self.texture.get_width()*.7,self.texture.get_height()*.7)
        self.time -= 1
        #print(self.time)
    
    def draw(self,window):
        #pygame.draw.rect(window,"red",self.rect)
        window.blit(self.texture,self.rect)

    def outofbounds(self,width,height):
    #static number 50 should be variable of player dimensions
        if self.x+self.texture.get_width() <= 0:
            return True
        if self.y+self.texture.get_height() <= 0:
            return True
        if self.x + self.texture.get_width() >= width:
            return True
        if self.y + self.texture.get_height() >= height:
            return True
        return False

    def projectile_animation(self):
        #Sample Relative Path: Projectile Animations\m13.png
        root_dir = "Projectile Animations"
        animation = []

        for path in os.listdir(root_dir):
            # check if current path is a file
            if os.path.isfile(os.path.join(root_dir, path)):
                animation.append(root_dir+  "\\" + path)

        if self.current_frame >= len(animation)-1:
            self.current_frame = 0
        
        self.texture = pygame.transform.rotate(pygame.image.load(str(animation[self.current_frame])),self.direc_facing)
        self.texture = pygame.transform.scale_by(self.texture,5)

        self.current_frame += 1

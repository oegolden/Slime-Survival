import pygame, sys, time,math,player

class Hud:

    #Menu_Buttons = {
    #    "Play":pygame.image.load("Buttons text pack\play.png"),
    #    "Restart":pygame.image.load("Buttons text pack\\restart.png"),
    #    "Leaderboard":pygame.image.load("Buttons text pack\leaderboard.png")
    #}

    def __init__(self,player,score = 0):
        self.health = player.health_points
        self.max_health = player.max_health
        self.score = score
        self.text_font = pygame.font.Font("Fonts\Grand9K Pixel.ttf",25)
        self.round_text_font = pygame.font.Font("Fonts\Grand9K Pixel.ttf",125)
        self.round_text_timer = 120
        self.round = 1
        self.round_animating = True

    def update(self,player):
        self.health = player.health_points
        self.max_health = player.max_health

    
    def draw_score(self,window,x,y):
        img = self.text_font.render("Score: " + str(self.score), True, "White")
        window.blit(img, (x,y))
    
    def draw_health(self,window,x,y):
        img = self.text_font.render("Health: " + str(self.health) + "/" + str(self.max_health), True, "White")
        window.blit(img, (x,y))
    
    def draw_round(self,window,x,y):
        if self.round_animating:
            print(self.round_text_timer)
            if self.round_text_timer <= 0:
                self.round_text_timer = 120
                self.round_animating = False    
            if self.round_text_timer > 0:
                img = self.round_text_font.render("Round: " + str(self.round), True, "White")
                window.blit(img, (x,y))
                self.round_text_timer -= 1
    
    def new_round(self):
        self.round += 1
        self.round_animating = True
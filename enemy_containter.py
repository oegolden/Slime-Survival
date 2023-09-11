import pygame, enemy,player,random,UI,EnemyBehavior,mapManager
from enemy import Enemy
from player import Player

class Enemies:
    def __init__(self):
        self.enemy_array = []
        self.size = 0
    
    #Spanws an enemy ina random x y within the bounds of the map.
    def spawn_enemy(self,map):
        spawner = random.choice(map.spawner_tile)
        x = spawner.x
        y=spawner.y
            #TODO: figure out enemy positioning with more than 1 enemy
        enemy = Enemy(x,y)
        self.enemy_array.append(enemy)
        self.size += 1
    
    def spawn_animations(self, window,n):
        for x in self.enemy_array:
            x.spawn_animation(window,n)

    #Checks for all enemies in the list of enemies with a health of 0 or less, and deletes them accordingly
    def despawn_enemies(self,Hud):
        for x in self.enemy_array:
            if x.health_points <= 0:
                self.enemy_array.remove(x)
                Hud.score += 1

    def draw_enemies(self,window):
        for x in self.enemy_array:
            x.draw_enemy(window)
    
    def rand_direc_select(self):
        for x in self.enemy_array:
            x.rand_move_direct()

    def stop_enemies(self):
        for x in self.enemy_array:
            x.stop_movement()
    
    def detect_player_hit(self,projectiles):
        for x in self.enemy_array:
                for y in projectiles.proj_array:
                    x.detect_player_hit(y)
        else:
            return

    def update_enemies(self,dt):
        for x in self.enemy_array:
            if x.lunging:
                x.lunge(dt)
            else:
                x.standard_position_update(dt)
            x.update_char()

    def out_of_bounds(self,width,height):
        for x in self.enemy_array:
            x.outofbounds(width,height)
    
    def enemy_behavior(self,player):
        for x in self.enemy_array:
            EnemyBehavior.Behavioral_Tree(x,player).run_tree()
    
    def enemy_chasing(self,player):
            for x in self.enemy_array:
                x.chase_player(player)
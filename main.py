import pygame, sys, time, player,enemy,threading,enemy_containter,UI,Projectile_Manager,mapManager,EnemyBehavior
from enemy import Enemy
from  player import Player
#Main clas final variables
WIDTH = 1080
HEIGHT = 810
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_color = pygame.Color(135,159,41)
screen.fill(background_color)
clock = pygame.time.Clock()
player = Player(WIDTH/2,HEIGHT/2+70)
enemies = enemy_containter.Enemies()
previous_time = time.time()

#Game State Variables
game_paused = False
game_over = False
#Timer eVENTS
spawn_delay = 3000 # 0.5 seconds
new_round_delay = 15000
spawn_event = pygame.USEREVENT + 1
new_round = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_event , spawn_delay )
pygame.time.set_timer(new_round, new_round_delay)

#Initizlie UI elemnts
ui = UI.Hud(player)

#Initialize projectile manager
projectiles = Projectile_Manager.Projectiles()

#Initialize Map manager()
tiles = mapManager.Tile_Manager()
tiles.custom_map(WIDTH/8,HEIGHT/6)

while True:
    #Clock for all the animations
    clock.tick(60)
    if game_paused:
        pass
    if game_over == True:
        pygame.quit()
    
    #Creatign delta time, which will be used for movement
    dt = time.time() - previous_time
    previous_time = time.time()
    
    #Timer for enemy movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        player.checkKeypress(event)
        player.check_sprint_keypress(event)
        player.attack_pressed(event,projectiles,dt)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               game_paused = True
        if event.type == spawn_event:
            enemies.spawn_enemy(tiles)
        if event.type == new_round:
            ui.new_round()
            if ui.round <= 20:
                spawn_delay -= 10
            pygame.time.set_timer(spawn_event , spawn_delay )
    if player.health_points == 0:
        player.reset_player(WIDTH/2,HEIGHT/2+70)
        enemies = enemy_containter.Enemies()
        ui = UI.Hud(player)
        projectiles = Projectile_Manager.Projectiles()
        spawn_delay = 3000 # 0.5 seconds
        pygame.time.set_timer(spawn_event,spawn_delay)
        new_round_delay = 15000
        pygame.time.set_timer(new_round, new_round_delay)  
    #checks for collision of player to enemy, and enemy to player attack
    for x in enemies.enemy_array:
        player.body_collision(x.rect)
        enemies.detect_player_hit(projectiles)

    #Despawns dead enemies
    enemies.despawn_enemies(ui)
    #Sets the enemy behavior for the current game state
    enemies.enemy_behavior(player)
    #enemies.enemy_chasing(player)    
    #updating entities with new position
    tiles.player_tile_collision(player,dt)
    tiles.enemy_tile_collision(enemies,dt)
    player.standard_position_update(dt)
    player.update_char()
    enemies.update_enemies(dt)
    projectiles.update()
    player.outofbounds(WIDTH,HEIGHT)
    enemies.out_of_bounds(WIDTH,HEIGHT)
    projectiles.despawn_projectiles(WIDTH,HEIGHT)
    ui.update(player)
    #Drawing to the screen

    
    screen.fill(background_color)
    tiles.draw_liquidtiles(screen)
    tiles.animate_spawn_tiles(screen)
    tiles.draw_solidtiles(screen)
    projectiles.draw_projectiles(screen)
    player.draw_player(screen)
    enemies.draw_enemies(screen)
    ui.draw_score(screen,100,25)
    ui.draw_health(screen,300,25)
    ui.draw_round(screen, 475, 125)
    pygame.display.update()
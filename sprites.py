import pygame
from config import *
import math
import random


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])

        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite


#   PLAYER RELATED SPRITES

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.p_sprite_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = 'up'
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_ground_animations = [
            self.game.character_spritesheet.get_sprite(0, 100, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 100, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 100, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 100, TILESIZE*2, TILESIZE*2)
        ]

        self.down_moving_animations = [
            self.game.character_spritesheet.get_sprite(0, 150, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 150, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 150, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 150, TILESIZE*2, TILESIZE*2)
        ]

        self.up_ground_animations = [
            self.game.character_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.up_moving_animations = [
            self.game.character_spritesheet.get_sprite(0, 50, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 50, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 50, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 50, TILESIZE*2, TILESIZE*2)
        ]

        self.left_ground_animations = [
            self.game.character_spritesheet.get_sprite(0, 300, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 300, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 300, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 300, TILESIZE*2, TILESIZE*2)
        ]

        self.left_moving_animations = [
            self.game.character_spritesheet.get_sprite(0, 350, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 350, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 350, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 350, TILESIZE*2, TILESIZE*2)
        ]

        self.right_ground_animations = [
            self.game.character_spritesheet.get_sprite(0, 200, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 200, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 200, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 200, TILESIZE*2, TILESIZE*2)
        ]

        self.right_moving_animations = [
            self.game.character_spritesheet.get_sprite(0, 250, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(50, 250, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(100, 250, TILESIZE*2, TILESIZE*2),
            self.game.character_spritesheet.get_sprite(150, 250, TILESIZE*2, TILESIZE*2)
        ]

        
        self.image = self.game.character_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.armed_melee = False
        self.armed_ranged = False

        self.health = 100
        self.pc_health = 100
        self.level = 1
        
        self.gun_ammo = 500
        self.flare_ammo = 50
        self.rocket_ammo = 0
        self.atgm_ammo = 0
        self.aam_ammo = 0

        

        self.landed = False

        self.flare_timer = pygame.time.get_ticks()
        self.gun_timer = pygame.time.get_ticks()
        self.rocket_timer = pygame.time.get_ticks()
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_blocks('x')
       
        
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0

        #   cap health
        self.max_health = 98 + self.level * 2

        if self.health >= self.max_health:
            self.health = self.max_health

        self.dec_health = self.health / self.max_health
        self.pc_health = self.dec_health * 100

        #   cap level
        if self.level > 99:
            self.level = 99


        if self.rocket_ammo < 0:
            self.rocket_ammo = 0
        if self.gun_ammo < 0:
            self.gun_ammo = 0
        if self.flare_ammo < 0:
            self.flare_ammo = 0
        if self.atgm_ammo < 0:
            self.atgm_ammo = 0
        if self.aam_ammo < 0:
            self.aam_ammo = 0

        #   weapon firing

        keys = pygame.key.get_pressed()
        buttons = self.game.joystick

        

        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if self.gun_ammo > 0:
                if now - self.gun_timer >= 100:
                    self.gun_ammo -= 3
                    self.game.gun_sound.set_volume(0.3)
                    self.game.gun_sound.play(0)
                    self.fire_cannon()
                    self.gun_timer = now

        if keys[pygame.K_f]:
            now = pygame.time.get_ticks()
            if self.flare_ammo > 0:
                if now - self.flare_timer >= 300:
                    self.flare_ammo -= 2
                    self.game.flare_sound.set_volume(0.9)
                    self.game.flare_sound.play(0)
                    self.fire_flares()
                    self.flare_timer = now

        if keys[pygame.K_h]:
            now = pygame.time.get_ticks()
            if self.rocket_ammo > 0:
                if now - self.rocket_timer >= 300:
                    self.rocket_ammo -= 3
                    self.fire_rockets()
                    self.game.missile_launch_sound.set_volume(0.5)
                    self.game.missile_launch_sound.play(0)
                    self.fire_rockets()
                    self.rocket_timer = now

        if keys[pygame.K_g]:
            now = pygame.time.get_ticks()
            if self.game.aoi_sprite.target:
                if self.atgm_ammo > 0:
                    if now - self.missile_timer >= 1000:
                        self.atgm_ammo -= 1
                        
                        self.game.missile_launch_sound.set_volume(0.5)
                        self.game.missile_launch_sound.play(0)
                        self.fire_missile()
                        self.missile_timer = now
                if self.aam_ammo > 0:
                    if now - self.missile_timer >= 1000:
                        self.aam_ammo -= 1
                        
                        self.game.missile_launch_sound.set_volume(0.5)
                        self.game.missile_launch_sound.play(0)
                        self.fire_missile()
                        self.missile_timer = now

    def movement(self):
        keys = pygame.key.get_pressed()
        #   left
        if keys[pygame.K_a] or keys[pygame.K_LEFT] or self.game.player_motion_x == 'left':
            
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            
            self.x_change -= PLAYER_SPEED
            
            self.facing = 'left'
        #   right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or self.game.player_motion_x == 'right':
            
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            
            self.x_change += PLAYER_SPEED
            
            self.facing = 'right'
        #   up
        if keys[pygame.K_w] or keys[pygame.K_UP] or self.game.player_motion_y == 'up':
            
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            
            self.y_change -= PLAYER_SPEED
            
            self.facing = 'up'
        #   down
        if keys[pygame.K_s] or keys[pygame.K_DOWN] or self.game.player_motion_y == 'down':
            
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            
            self.y_change += PLAYER_SPEED
            
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    
    def animate(self):

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.up_ground_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
            else:
                self.image = self.up_moving_animations[math.floor(self.animation_loop_2)]
                self.animation_loop_2 += 0.3
                if self.animation_loop_2 >= 4:
                    self.animation_loop_2 = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.down_ground_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
            else:
                self.image = self.down_moving_animations[math.floor(self.animation_loop_2)]
                self.animation_loop_2 += 0.3
                if self.animation_loop_2 >= 4:
                    self.animation_loop_2 = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.left_ground_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
            else:
                self.image = self.left_moving_animations[math.floor(self.animation_loop_2)]
                self.animation_loop_2 += 0.3
                if self.animation_loop_2 >= 4:
                    self.animation_loop_2 = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.right_ground_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
            else:
                self.image = self.right_moving_animations[math.floor(self.animation_loop_2)]
                self.animation_loop_2 += 0.3
                if self.animation_loop_2 >= 4:
                    self.animation_loop_2 = 0

    def fire_cannon(self):
        if self.facing == 'up':
            CannonFireY(self.game, self.rect.x + 12, self.rect.y - 75)
        elif self.facing == 'down':
            CannonFireY(self.game, self.rect.x + 12, self.rect.y + 50)
        elif self.facing == 'left':
            CannonFireX(self.game, self.rect.x - 75, self.rect.y + 12)
        elif self.facing == 'right':
            CannonFireX(self.game, self.rect.x + 50, self.rect.y + 12)

    def fire_flares(self):
        if self.facing == 'up':
            Flares(self.game, self.rect.x + 12, self.rect.y + 50)
        elif self.facing == 'down':
            Flares(self.game, self.rect.x + 12, self.rect.y - 25)
        elif self.facing == 'left':
            Flares(self.game, self.rect.x + 50, self.rect.y +12)
        elif self.facing == 'right':
            Flares(self.game, self.rect.x - 25, self.rect.y + 12)

    def fire_rockets(self):
        if self.facing == 'up':
            UnguidedRocket(self.game, self.rect.x+12, self.rect.y+12)
        elif self.facing == 'down':
            UnguidedRocket(self.game, self.rect.x+12, self.rect.y+12)
        elif self.facing == 'left':
            UnguidedRocket(self.game, self.rect.x+12, self.rect.y+12)
        elif self.facing == 'right':
            UnguidedRocket(self.game, self.rect.x+12, self.rect.y+12)

    def fire_missile(self):
        try:
            if self.atgm_ammo > 0:
                if self.facing == 'up':
                    AtGm(self.game, self.rect.x+12, self.rect.y)
                elif self.facing == 'down':
                    AtGm(self.game, self.rect.x+12, self.rect.y+12)
                elif self.facing == 'left':
                    AtGm(self.game, self.rect.x+12, self.rect.y)
                elif self.facing == 'right':
                    AtGm(self.game, self.rect.x+12, self.rect.y)

            if self.aam_ammo > 0:
                if self.facing == 'up':
                    AaM(self.game, self.rect.x+12, self.rect.y)
                elif self.facing == 'down':
                    AaM(self.game, self.rect.x+12, self.rect.y+12)
                elif self.facing == 'left':
                    AaM(self.game, self.rect.x+12, self.rect.y)
                elif self.facing == 'right':
                    AaM(self.game, self.rect.x+12, self.rect.y)
        except:
            pass
            

class AreaOfInfluence(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.aoi
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*8
        self.height = TILESIZE*8

        image_to_load = pygame.image.load('img/area_of_influence.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.once = True
        self.target = 0

    def update(self):
        self.collide_targets()

    def collide_targets(self):
        if self.game.player.atgm_ammo > 0:
            try:
                self.target.kill()
            except AttributeError:
                pass
            
            hits = pygame.sprite.spritecollide(self, self.game.enemy_ground, False)
            if hits:
                
                self.target = Targeting(self.game, hits[0].rect.x, hits[0].rect.y)
            else:
                self.target = 0

        if self.game.player.aam_ammo > 0:
            try:
                self.target.kill()
            except AttributeError:
                pass
            
            hits = pygame.sprite.spritecollide(self, self.game.enemy_air, False)
            if hits:
                
                self.target = Targeting(self.game, hits[0].rect.x+12, hits[0].rect.y+12)
            else:
                self.target = 0
            
            
class CannonFireX(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE*3
        self.height = TILESIZE

        self.animation_loop = 0

        self.right_animations = [
            self.game.cannon_fire_spritesheet_y.get_sprite(150, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(150, 25, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(150, 50, self.width, self.height)
        ]

        self.left_animations = [
            self.game.cannon_fire_spritesheet_y.get_sprite(225, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(225, 25, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(225, 50, self.width, self.height)
        ]

        self.image = self.game.cannon_fire_spritesheet_y.get_sprite(150, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 500:
                hits_enemies[0].health -= 30
                self.game.player.health += 1
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class CannonFireY(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE * 3

        self.animation_loop = 0

        self.up_animations = [
            self.game.cannon_fire_spritesheet_y.get_sprite(75, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(100, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(125, 0, self.width, self.height)
        ]

        self.down_animations = [
            self.game.cannon_fire_spritesheet_y.get_sprite(0, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(25, 0, self.width, self.height),
            self.game.cannon_fire_spritesheet_y.get_sprite(50, 0, self.width, self.height)
        ]

        self.image = self.game.cannon_fire_spritesheet_y.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 500:
                hits_enemies[0].health -= 30
                self.game.player.health += 1
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class Flares(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.flares
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.animations = [
            self.game.flares_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.flares_spritesheet.get_sprite(25, 0, self.width, self.height),
            self.game.flares_spritesheet.get_sprite(50, 0, self.width, self.height)
        ]

        

        self.image = self.game.flares_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

    def animate(self):

        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 3:
            self.kill()


class AtGm(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = self.game.player.facing
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_animations = [
            self.game.atgm_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        ]

        

        self.up_animations = [
            self.game.atgm_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

       

        self.left_animations = [
            self.game.atgm_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        

        self.right_animations = [
            self.game.atgm_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.atgm_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.atgm_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.atgm_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE)
        ]

        self.image = self.game.atgm_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.death_timer = pygame.time.get_ticks()

        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_enemy('x')
       
        
        self.rect.y += self.y_change
        self.collide_enemy('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        
        
        #   weapon firing

    def movement(self):
        now = pygame.time.get_ticks()
        try:
            if self.alive:
                if self.game.aoi_sprite.target.rect.y > self.rect.y:
                    
                    self.y_change += 4
                elif self.game.aoi_sprite.target.rect.y < self.rect.y:
                    
                    self.y_change -= 4

                if self.game.aoi_sprite.target.rect.x > self.rect.x:
                    
                    self.x_change += 4
                elif self.game.aoi_sprite.target.rect.x < self.rect.x:
                    
                    self.x_change -= 4

                if self.game.aoi_sprite.target.rect.x == self.rect.x and self.game.aoi_sprite.target.rect.y == self.rect.y:
                    self.alive = False
                elif now - self.missile_timer >= 4000:
                    self.alive = False

        except:
            self.kill()

    def collide_enemy(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.enemy_ground, False)
            if hits:
                hits[0].health -= 30    
                self.alive = False
                self.missile_timer = now
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.enemy_ground, False)
            if hits:
                hits[0].health -= 30
                self.alive = False
                self.missile_timer = now
   
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            self.game.missile_explosion_sound.set_volume(0.4)
            if now - self.death_timer >= 1200:
                self.game.missile_explosion_sound.play(0)
                self.death_timer = now
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 3:
                
                self.kill()


class AaM(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = self.game.player.facing
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_animations = [
            self.game.aam_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.aam_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.aam_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.aam_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.aam_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.aam_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.aam_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE)
        ]

        self.image = self.game.aam_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.death_timer = pygame.time.get_ticks()

        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_enemy('x')
       
        
        self.rect.y += self.y_change
        self.collide_enemy('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        
        
        #   weapon firing

    def movement(self):
        now = pygame.time.get_ticks()
        try:
            
            if self.game.aoi_sprite.target.rect.y > self.rect.y:
                
                self.y_change += 6
            elif self.game.aoi_sprite.target.rect.y < self.rect.y:
                
                self.y_change -= 6

            if self.game.aoi_sprite.target.rect.x > self.rect.x:
                
                self.x_change += 6
            elif self.game.aoi_sprite.target.rect.x < self.rect.x:
                
                self.x_change -= 6

            if self.game.aoi_sprite.target.rect.x == self.rect.x and self.game.aoi_sprite.target.rect.y == self.rect.y:
                self.alive = False
            elif now - self.missile_timer >= 6000:
                self.alive = False

        except:
            self.kill()

    def collide_enemy(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.enemy_air, False)
            if hits:
                hits[0].living = False    
                self.alive = False
                self.missile_timer = now
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.enemy_air, False)
            if hits:
                hits[0].living = False
                self.alive = False
                self.missile_timer = now
   
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            self.game.missile_explosion_sound.set_volume(0.4)
            if now - self.death_timer >= 1200:
                self.game.missile_explosion_sound.play(0)
                self.death_timer = now
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 3:
                
                self.kill()


class ReferenceSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.ref_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class UnguidedRocket(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        if self.game.player.facing == 'left':
            self.facing = 'left'
        elif self.game.player.facing == 'right':
            self.facing = 'right'
        elif self.game.player.facing == 'up':
            self.facing = 'up'
        elif self.game.player.facing == 'down':
            self.facing = 'down'
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_animations = [
            self.game.rocket_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        ]

        

        self.up_animations = [
            self.game.rocket_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

       

        self.left_animations = [
            self.game.rocket_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        

        self.right_animations = [
            self.game.rocket_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.rocket_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.rocket_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.rocket_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE)
        ]
    

        
        self.image = self.game.sam_missile_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        

        

        
        self.death_timer = pygame.time.get_ticks()
        
        
        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_enemies('x')
       
        
        self.rect.y += self.y_change
        self.collide_enemies('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        
        
        #   weapon firing

    def movement(self):
        now = pygame.time.get_ticks()

        if self.alive:
        
            if self.facing == 'right':
                
                self.x_change += 4
                if now - self.missile_timer >= 500:
                    self.x_change = 0
                    self.missile_timer = now
                    self.alive = False
            elif self.facing == 'left':
                
                self.x_change -= 4
                if now - self.missile_timer >= 500:
                    self.x_change = 0
                    self.missile_timer = now
                    self.alive = False

            elif self.facing == 'up':
                
                self.y_change -= 4
                if now - self.missile_timer >= 500:
                    self.y_change = 0
                    self.missile_timer = now
                    self.alive = False

            elif self.facing == 'down':
                
                self.y_change += 4
                if now - self.missile_timer >= 500:
                    self.y_change = 0
                    self.missile_timer = now
                    self.alive = False

    def collide_enemies(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                hits[0].health -= 50
                self.alive = False
                
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                hits[0].health -= 50
                self.alive = False
           
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            self.game.missile_explosion_sound.set_volume(0.4)
            if now - self.death_timer >= 1200:
                self.game.missile_explosion_sound.play(0)
                self.death_timer = now
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 3:
                
                self.kill()


class Targeting(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE


        self.animations = [
            self.game.targeting_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.targeting_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

      
        self.image = self.animations[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



        

    def update(self):
        pass


#   ENEMY RELATED SPRITES

class TankOneSpawnPoint(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.origin_x = x
        self.y = y * TILESIZE
        self.origin_y = y
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lv10 = False

        self.spawn_timer = pygame.time.get_ticks()
        self.spawned = 0

    def update(self):
        if self.spawned < 6:
            now = pygame.time.get_ticks()
            if now - self.spawn_timer >= 3000:     #   10sec
                TankOne(self.game, self.rect.x/TILESIZE, self.rect.y/TILESIZE)
                self.spawned += 1
                self.spawn_timer = now
            

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer >= 10000:     #   10sec
            #   spawn sprite
            self.spawn_timer = now


class SAMTruck(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies, self.game.enemy_ground
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.once = True

        self.down_animations = [
            self.game.sam_truck_spritesheet.get_sprite(0, 50, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(25, 50, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(50, 50, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.sam_truck_spritesheet.get_sprite(0, 75, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(25, 75, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(50, 75, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.sam_truck_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.sam_truck_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.sam_truck_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.sam_truck_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 50
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 20
        self.alive = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_aoi('x')
       
        
        self.rect.y += self.y_change
        self.collide_aoi('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass

    def collide_aoi(self, direction):
        now = pygame.time.get_ticks()
        if now - self.missile_timer >= 5000:
            if direction == 'x':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    self.fire_missile()
                    self.missile_timer = now
            if direction == 'y':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    self.fire_missile()
                    self.missile_timer = now
                    
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 3:
                    self.animation_loop_1 = 0
                
            if self.facing == 'down':
                self.image = self.down_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 3:
                    self.animation_loop_1 = 0
                
            if self.facing == 'left':
                self.image = self.left_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 3:
                    self.animation_loop_1 = 0
                
            if self.facing == 'right':
                self.image = self.right_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 3:
                    self.animation_loop_1 = 0

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemy_ground.remove(self)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3
                

    def fire_missile(self):
        if self.alive:
            self.game.missile_launch_sound.set_volume(0.3)
            self.game.missile_launch_sound.play(0)
            SAMMissile(self.game, self.rect.x, self.rect.y)

 
class SAMMissile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        if self.game.player.rect.x > self.x:
            self.facing = 'right'
        elif self.game.player.rect.x <= self.x:
            self.facing = 'left'
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_animations = [
            self.game.sam_missile_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(75, 25, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(75, 50, TILESIZE, TILESIZE)
        ]

        

        self.up_animations = [
            self.game.sam_missile_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(50, 50, TILESIZE, TILESIZE)
        ]

       

        self.left_animations = [
            self.game.sam_missile_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(25, 50, TILESIZE, TILESIZE)
        ]

        

        self.right_animations = [
            self.game.sam_missile_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(0, 50, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.sam_missile_spritesheet.get_sprite(0, 50, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(25, 50, TILESIZE, TILESIZE),
            self.game.sam_missile_spritesheet.get_sprite(50, 50, TILESIZE, TILESIZE)
        ]
    

        
        self.image = self.game.sam_missile_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        

        

        
        self.death_timer = pygame.time.get_ticks()
        
        
        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_player('x')
        self.collide_flares('x')
       
        
        self.rect.y += self.y_change
        self.collide_player('y')
        self.collide_flares('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        
        
        #   weapon firing

    def movement(self):
        now = pygame.time.get_ticks()
        
        if self.alive:

            if self.game.player.rect.x > self.rect.x:
                self.facing = 'right'
                self.x_change += NPC_SPEED
            elif self.game.player.rect.x < self.rect.x:
                self.facing = 'left'
                self.x_change -= NPC_SPEED

            

            
            if self.game.player.rect.y > self.rect.y:
                self.facing = 'down'
                self.y_change += NPC_SPEED
            elif self.game.player.rect.y < self.rect.y:
                self.facing = 'up'
                self.y_change -= NPC_SPEED

            if self.game.player.rect.x == self.rect.x and self.game.player.rect.y == self.rect.y:
                self.alive = False
            elif now - self.missile_timer >= 3000:
                self.alive = False

    def collide_player(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health -= 0.5    
                self.alive = False
                self.missile_timer = now
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health -= 0.5
                self.alive = False
                self.missile_timer = now

    def collide_flares(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.flares, False)
            if hits:    
                self.alive = False
                self.missile_timer = now
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.flares, False)
            if hits:
                self.alive = False
                self.missile_timer = now
                    
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            self.game.missile_explosion_sound.set_volume(0.4)
            if now - self.death_timer >= 1200:
                self.game.missile_explosion_sound.play(0)
                self.death_timer = now
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 3:
                
                self.kill()


class SpAaG(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies, self.game.enemy_ground
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.once = True

        self.down_animations = [
            self.game.spaag_spritesheet.get_sprite(0, 50, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(25, 50, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(50, 50, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(75, 50, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.spaag_spritesheet.get_sprite(0, 75, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(25, 75, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(50, 75, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(75, 75, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.spaag_spritesheet.get_sprite(0, 25, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(25, 25, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(50, 25, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(75, 25, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.spaag_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.spaag_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.spaag_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 50
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 20
        self.alive = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_aoi('x')
       
        
        self.rect.y += self.y_change
        self.collide_aoi('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass

    def collide_aoi(self, direction):
        now = pygame.time.get_ticks()
        if now - self.missile_timer >= 300:
            if direction == 'x':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    self.fire_gun()
                    self.missile_timer = now
            if direction == 'y':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    self.fire_gun()
                    self.missile_timer = now
                    
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.3
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
                
            if self.facing == 'down':
                self.image = self.down_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.1
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
                
            if self.facing == 'left':
                self.image = self.left_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.1
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0
                
            if self.facing == 'right':
                self.image = self.right_animations[math.floor(self.animation_loop_1)]
                self.animation_loop_1 += 0.1
                if self.animation_loop_1 >= 4:
                    self.animation_loop_1 = 0

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemy_ground.remove(self)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3

    def fire_gun(self):
        if self.alive:
            self.game.gun_sound.play(0)
            self.game.gun_sound.set_volume(0.06)
            AAARound(self.game, self.rect.x+8, self.rect.y+8)
            

class AAARound(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.x_change = 0
        self.y_change = 0

        if self.game.player.rect.x > self.x:
            self.facing = 'right'
        elif self.game.player.rect.x <= self.x:
            self.facing = 'left'
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.aaa_round_spritesheet.get_sprite(0, 0, 8, 8),
            self.game.aaa_round_spritesheet.get_sprite(8, 0, 8, 8),
            self.game.aaa_round_spritesheet.get_sprite(16, 0, 8, 8)
        ]

        self.dead_animations = [
            self.game.aaa_round_spritesheet.get_sprite(24, 0, 8, 8),
            self.game.aaa_round_spritesheet.get_sprite(32, 0, 8, 8)
        ]
    

        
        self.image = self.game.aaa_round_spritesheet.get_sprite(0, 0, 8, 8)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.death_timer = pygame.time.get_ticks()
        
        
        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_player('x')
       
        
        self.rect.y += self.y_change
        self.collide_player('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        
        
        #   weapon firing

    def movement(self):
        now = pygame.time.get_ticks()
        
        if self.alive:

            if self.game.player.rect.x > self.rect.x:
                self.facing = 'right'
                self.x_change += 5
            elif self.game.player.rect.x < self.rect.x:
                self.facing = 'left'
                self.x_change -= 5

            

            
            if self.game.player.rect.y > self.rect.y:
                self.facing = 'down'
                self.y_change += 5
            elif self.game.player.rect.y < self.rect.y:
                self.facing = 'up'
                self.y_change -= 5

            if self.game.player.rect.x == self.rect.x and self.game.player.rect.y == self.rect.y:
                self.alive = False
            elif now - self.missile_timer >= 200:
                self.alive = False

    def collide_player(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health -= 0.2    
                self.alive = False
                self.missile_timer = now
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health -= 0.2
                self.alive = False
                self.missile_timer = now
                    
    def animate(self):
        if self.alive:

            self.image = self.animations[math.floor(self.animation_loop_2)]
            self.animation_loop_2 += 0.3
            if self.animation_loop_2 >= 3:
                self.animation_loop_2 = 2

        else:
            now = pygame.time.get_ticks()
            self.game.missile_explosion_sound.set_volume(0.5)
            if now - self.death_timer >= 1200:
                self.game.missile_explosion_sound.play(0)
                self.death_timer = now
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 2:
                
                self.kill()


class Infantry(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.down_image = self.game.infantry_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)

        self.up_image = self.game.infantry_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.left_image = self.game.infantry_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)

        self.right_image = self.game.infantry_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)

        
      
        self.image = self.game.infantry_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 25
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 10
        self.alive = True

        self.max_travel = 50
        self.movement_counter = 0

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_aoi('x')
       
        
        self.rect.y += self.y_change
        self.collide_aoi('y')
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        if self.facing == 'left':
            if self.movement_counter < self.max_travel:
                self.rect.x -= 1
                self.movement_counter += 1
            else:
                self.movement_counter = 0
                self.facing = 'right'

        if self.facing == 'right':
            if self.movement_counter < self.max_travel:
                self.rect.x += 1
                self.movement_counter += 1
            else:
                self.movement_counter = 0
                self.facing = 'left'


    def collide_aoi(self, direction):
        now = pygame.time.get_ticks()
        if now - self.missile_timer >= 5000:
            if direction == 'x':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    
                    self.missile_timer = now
            if direction == 'y':
                hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
                if hits:
                    
                    self.missile_timer = now
                    
    def animate(self):
        if self.alive:

            if self.facing == 'up':
                self.image = self.up_image
                   
            if self.facing == 'down':
                self.image = self.down_image
                
            if self.facing == 'left':
                self.image = self.left_image
                
            if self.facing == 'right':
                self.image = self.right_image

        else:
            self.kill()
                

    def fire_missile(self):
        if self.alive:
            SAMMissile(self.game, self.rect.x, self.rect.y)


class TankOne(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies, self.game.enemy_ground
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.origin_x = self.x
        self.origin_y = self.y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'up'
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.once = True

        self.down_animations = [
            self.game.tank_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.tank_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.tank_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.tank_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.tank_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 2000
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 20
        self.living = True
        self.steps1 = 0
        self.range1 = random.randint(200, 250)
        self.steps2 = 0
        self.range2 = random.randint(800, 950)
        self.steps3 = 0
        self.range3 = random.randint(200, 350)
        self.speed = 1

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.living = False
        
        #   weapon firing

    def movement(self):
        
        if self.steps1 < self.range1:
            if self.living:
                self.y_change -= self.speed
                self.steps1 += self.speed
        else:
            self.facing = 'left'
            if self.steps2 < self.range2:
                if self.living:
                    self.x_change -= self.speed
                    self.steps2 += self.speed
            else:
                self.facing = 'up'
                if self.steps3 < self.range3:
                    if self.living:
                        self.y_change -= self.speed
                        self.steps3 += self.speed
                    
    def animate(self):
        if self.living:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemy_ground.remove(self)
                self.game.tanks_killed += 1
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3


class TransportPlane(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemy_air
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.origin_x = self.x
        self.origin_y = self.y
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = 'up'
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.once = True

        self.down_animations = [
            self.game.transport_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.up_animations = [
            self.game.transport_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.left_animations = [
            self.game.transport_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.right_animations = [
            self.game.transport_spritesheet.get_sprite(150, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.dead_animations = [
            self.game.transport_spritesheet.get_sprite(200, 0, TILESIZE*2, TILESIZE*2),
            self.game.transport_spritesheet.get_sprite(250, 0, TILESIZE*2, TILESIZE*2),
            self.game.transport_spritesheet.get_sprite(300, 0, TILESIZE*2, TILESIZE*2),
            self.game.transport_spritesheet.get_sprite(350, 0, TILESIZE*2, TILESIZE*2)
        ]
      
        self.image = self.game.transport_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 100
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 20
        self.living = True
        self.steps1 = 0
        self.range1 = random.randint(500, 550)
        self.steps2 = 0
        self.range2 = random.randint(800, 950)
        self.steps3 = 0
        self.range3 = random.randint(500, 650)
        self.loop_steps1 = 0
        self.loop_steps2 = 0
        self.loop_count = 0
        
        self.loop_range = random.randint(500, 650)
        self.speed = 3

        
        self.troop_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.living = False
        
        #   weapon firing

    def movement(self):
        
        if self.steps1 < self.range1:
            if self.living:
                self.y_change -= self.speed
                self.steps1 += self.speed
        else:
            self.facing = 'left'
            if self.steps2 < self.range2:
                if self.living:
                    self.x_change -= self.speed
                    self.steps2 += self.speed
            else:
                self.facing = 'up'
                if self.steps3 < self.range3:
                    if self.living:
                        self.y_change -= self.speed
                        self.steps3 += self.speed
                else:
                    self.facing = 'down'
                    if self.loop_steps1 < self.loop_range:
                        if self.living:
                            self.y_change += self.speed
                            self.loop_steps1 += self.speed
                    else:
                        self.facing = 'up'
                        if self.loop_steps2 < self.loop_range:
                            if self.loop_count >= 2:
                                self.drop_troops()
                            if self.living:
                                self.y_change -= self.speed
                                self.loop_steps2 += self.speed
                        else:
                            self.facing = 'down'
                            self.loop_steps1 = 0
                            self.loop_steps2 = 0
                            self.loop_count += 1
                    
    def animate(self):
        if self.living:

            if self.facing == 'up':
                self.image = self.up_animations[0]
                
                
            if self.facing == 'down':
                self.image = self.down_animations[0]
                
                
            if self.facing == 'left':
                self.image = self.left_animations[0]
                
                
            if self.facing == 'right':
                self.image = self.right_animations[0]
                

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemy_ground.remove(self)
                
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 4:
                self.game.aircraft_killed += 1
                self.kill()

    def drop_troops(self):
        now = pygame.time.get_ticks()
        if now - self.troop_timer >= 620:
            ParaTrooper(self.game, self.rect.x+12, self.rect.y+12)
            self.game.troops_landed += 1
            self.troop_timer = now


class ParaTrooper(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        if self.game.player.rect.x > self.x:
            self.facing = 'right'
        elif self.game.player.rect.x <= self.x:
            self.facing = 'left'
        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.paratrooper_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.paratrooper_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        
    

        
        self.image = self.game.paratrooper_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.death_timer = pygame.time.get_ticks()
        self.health = 10
        
        self.alive = True

        self.range_max = 200
        self.range_min = -200
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health
        if self.health <= 0:
            self.alive = False
        
        
        #   weapon firing
                    
    def animate(self):
        if self.alive:

            self.image = self.animations[math.floor(self.animation_loop_2)]
            self.animation_loop_2 += 0.3
            if self.animation_loop_2 >= 8:
                self.animation_loop_2 = 7

        else:
            self.kill()


#   TERRAIN AND BUILDING SPRITES

class StationaryFrigate(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*6
        self.height = TILESIZE*2

        image_to_load = pygame.image.load('img/frigate_stationary.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Dirt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.dirt_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.dirt_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.dirt_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        
        self.image = self.images[random.randint(0, 2)]
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Scrub(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.scrub_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.scrub_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.scrub_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        
        self.image = self.images[random.randint(0, 2)]
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.images = [
            self.game.water_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.water_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class RadarBuilding(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.radar_building_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.radar_building_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2),
            self.game.radar_building_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE*2)
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.radar_building_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True

        self.once = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.3
            if self.animation_loop_1 >= 3:
                self.animation_loop_1 = 0
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3
                

class ObjectiveRadarBuilding(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.radar_building_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.radar_building_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2),
            self.game.radar_building_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE*2)
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.radar_building_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True

        self.once = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.3
            if self.animation_loop_1 >= 3:
                self.animation_loop_1 = 0
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.game.mission_complete()
                

class TwoByTwoHole(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        image_to_load = pygame.image.load('img/2x2hole.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Barrels(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animations = [
            self.game.barrels_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.barrels_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 20
        self.alive = True
        self.animation_loop_1 = 0
        self.once = True

    def update(self):
        if self.health <= 0:
            self.alive = False
        self.animate()

    def animate(self):
        if self.alive:
            self.image = self.animations[0]

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3


class PalmTree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/palm_tree.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Watchtower(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/watchtower.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Hangar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        

        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.hangar_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)            
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.hangar_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True
        self.once = True

    def update(self):
        #   call movement and animate functions.
        self.animate()
        

        #   move and check collisions

        
        
        

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[0]
            
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3


class ObjectiveFactory(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        

        
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.factory.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)            
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.hangar_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 10000
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True
        self.once = True

    def update(self):
        #   call movement and animate functions.
        self.animate()
        

        #   move and check collisions

        
        
        

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[0]
            
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.mission_complete()
                self.game.enemies.remove(self)
                

class RoadOneY(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

   
class RoadOneX(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

   
class RoadOneUpRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RoadOneUpLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RoadOneDownRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RoadOneDownLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.road_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Runway(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        image_to_load = pygame.image.load('img/runway.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class ControlTower(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.control_tower_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.control_tower_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2),
            self.game.control_tower_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE*2),
            self.game.control_tower_spritesheet.get_sprite(150, 0, TILESIZE*2, TILESIZE*2)
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.control_tower_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True

        self.once = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.2
            if self.animation_loop_1 >= 4:
                self.animation_loop_1 = 0
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.game.enemies.remove(self)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3
                

class HeliPad(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.helipads
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.helipad_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.helipad_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2)
        ]


        self.dead_animations = [
            self.game.vehicle_explosion_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
            self.game.vehicle_explosion_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        ]
      
        self.image = self.game.control_tower_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True

        self.once = True

        
        self.missile_timer = pygame.time.get_ticks()

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_player('x')
        self.collide_player('y')
        
       
        
        self.rect.y += self.y_change
        
        
        self.x_change = 0
        self.y_change = 0

        #   check health

        if self.health <= 0:
            self.alive = False
        
        #   weapon firing

    def movement(self):
        pass

    def collide_player(self, direction):
        now = pygame.time.get_ticks()
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health = 100
                self.game.player.gun_ammo = 500
                self.game.player.flare_ammo = 50
                self.game.player.landed = True
            
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                self.game.player.health = 100
                self.game.player.gun_ammo = 500
                self.game.player.flare_ammo = 50
                self.game.player.landed = True
                
                
    def animate(self):
        if self.alive:
            self.image = self.animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 2:
                self.animation_loop_1 = 0
                
            

        else:
            now = pygame.time.get_ticks()
            if self.once:
                self.game.building_explosion_sound.set_volume(0.5)
                self.game.building_explosion_sound.play(0)
                self.once = False
            self.image = self.dead_animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.1
            if self.animation_loop_1 >= 5:
                self.animation_loop_1 = 3
                

class FencingX(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingY(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingBottomRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingBottomleft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingTopRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingTopleft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.image = self.game.fencing_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FencingGate(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BUILDING_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE

        self.open = False

        
        self.image = self.game.fencing_spritesheet.get_sprite(150, 0, TILESIZE*2, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.open:
            self.image = self.game.fencing_spritesheet.get_sprite(100, 0, TILESIZE*2, TILESIZE)
        else:
            self.image = self.game.fencing_spritesheet.get_sprite(150, 0, TILESIZE*2, TILESIZE)
        


#   UI SPRITES

class RadarScreen(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OVERLAY_LAYER
        self.groups = self.game.overlay_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE*6
        self.height = TILESIZE*6

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop_1 = 0
        self.animation_loop_2 = 0

        self.animations = [
            self.game.radar_screen_spritesheet.get_sprite(0, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(0, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(150, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(150, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(300, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(300, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(450, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(450, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(600, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(600, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(750, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(750, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(900, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(900, 150, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(1050, 0, TILESIZE*6, TILESIZE*6),
            self.game.radar_screen_spritesheet.get_sprite(1050, 150, TILESIZE*6, TILESIZE*6)
        ]

        self.image = self.animations[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200
        self.death_timer = pygame.time.get_ticks()
        
        self.exp = 50
        self.alive = True

        

    def update(self):
        #   call movement and animate functions.

        
        self.animate()

        #   move and check collisions

        #   weapon firing

    def movement(self):
        pass
                 
    def animate(self):
        if self.alive:
            self.image = self.animations[math.floor(self.animation_loop_1)]
            self.animation_loop_1 += 0.3
            if self.animation_loop_1 >= 16:
                self.animation_loop_1 = 0
                
            
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('jennifer.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center= (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



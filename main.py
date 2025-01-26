import pygame
import sys
from sprites import *
from config import *
import math


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.running = True

        #   sounds
        self.main_theme = pygame.mixer.Sound('snd/main-theme.wav')
        self.gun_sound = pygame.mixer.Sound('snd/clean-machine-gun-burst.wav')
        self.flare_sound = pygame.mixer.Sound('snd/flares.wav')
        self.missile_launch_sound = pygame.mixer.Sound('snd/missile-launch.wav')
        self.missile_explosion_sound = pygame.mixer.Sound('snd/missile-explosion.wav')
        self.helicopter_sound = pygame.mixer.Sound('snd/helicopter-sound.wav')
        self.building_explosion_sound = pygame.mixer.Sound('snd/building-explosion.wav')

        

        #   spritesheets
        self.character_spritesheet = SpriteSheet('img/playerspritesheet.png')
        self.dirt_spritesheet = SpriteSheet('img/dirt1.png')
        self.healthbar_spritesheet = SpriteSheet('img/healthbar_spritesheet.png')
        self.cannon_fire_spritesheet_y = SpriteSheet('img/cannon_fire_spritesheet.png')
        self.flares_spritesheet = SpriteSheet('img/flares_spritesheet.png')
        self.sam_truck_spritesheet = SpriteSheet('img/sam_truck_spritesheet.png')
        self.vehicle_explosion_spritesheet = SpriteSheet('img/vehicle_explosion_spritesheet.png')
        self.sam_missile_spritesheet = SpriteSheet('img/missile_spritesheet.png')
        self.radar_building_spritesheet = SpriteSheet('img/radar_building_spritesheet.png')
        self.hangar_spritesheet = SpriteSheet('img/hangar.png')
        self.road_spritesheet = SpriteSheet('img/road_spritesheet.png')
        self.infantry_spritesheet = SpriteSheet('img/infantry_spritesheet.png')
        self.control_tower_spritesheet = SpriteSheet('img/control_tower_spritesheet.png')
        self.helipad_spritesheet = SpriteSheet('img/helipad_spritesheet.png')
        self.rocket_spritesheet = SpriteSheet('img/unguided_rocket_spritesheet.png')
        self.atgm_spritesheet = SpriteSheet('img/atgm_spritesheet.png')
        self.aam_spritesheet = SpriteSheet('img/aam_spritesheet.png')
        self.targeting_spritesheet = SpriteSheet('img/targeting_spritesheet.png')
        self.radar_screen_spritesheet = SpriteSheet('img/radar_screen_spritesheet.png')
        self.fencing_spritesheet = SpriteSheet('img/fencing_spritesheet.png')
        self.spaag_spritesheet = SpriteSheet('img/spaag_spritesheet.png')
        self.aaa_round_spritesheet = SpriteSheet('img/aaa_round_spritesheet.png')
        self.water_spritesheet = SpriteSheet('img/waterspritesheet.png')
        self.scrub_spritesheet = SpriteSheet('img/scrub_spritesheet.png')
        self.tank_spritesheet = SpriteSheet('img/tank_spritesheet.png')
        self.factory = SpriteSheet('img/factory.png')
        self.transport_spritesheet = SpriteSheet('img/transport_spritesheet.png')
        self.paratrooper_spritesheet = SpriteSheet('img/paratrooper_spritesheet.png')
        self.barrels_spritesheet = SpriteSheet('img/barrels.png')

        #   fonts
        self.font = pygame.font.Font('jennifer.ttf', 26)
        self.font_mid = pygame.font.Font('jennifer.ttf', 18)
        self.font_small = pygame.font.Font('jennifer.ttf', 14)
        self.font_smaller = pygame.font.Font('jennifer.ttf', 10)

        #   overlay setup
        self.overlay_bg = pygame.image.load('img/overlaybg.png')
        self.overlay_bg.set_colorkey(WHITE)
        self.menu_bg = pygame.image.load('img/menu_bg.jpg')
        
        
        
        
        pygame.display.set_caption('ALPHA-HOTEL-1')
        pygame.display.set_icon(self.character_spritesheet.get_sprite(50, 300, TILESIZE*2, TILESIZE*2))
        

        self.intro_bg = pygame.image.load('img/game_over_bg.jpg')
        self.game_over_bg = pygame.image.load('img/game_over_bg.jpg')
        self.rocket_img = pygame.image.load('img/rocket_pod.png')
        self.rocket_img.set_colorkey(WHITE)
        self.atgm_img = pygame.image.load('img/atgm.png')
        self.atgm_img.set_colorkey(WHITE)
        self.aam_img = pygame.image.load('img/aam.png')
        self.aam_img.set_colorkey(WHITE)

        self.convo = ''
        self.text_timer = pygame.time.get_ticks()
        self.radar_animation_loop = 0
      
    def create_ground_map_lv1(self):
        for i, row in enumerate(ground_map_lv1):
            for j, col in enumerate(row):
                if col == 'D':
                    Dirt(self, j, i)
                if col == '2':
                    TwoByTwoHole(self, j, i)
                    RadarBuilding(self, j, i)
                if col == '3':
                    TwoByTwoHole(self, j, i)
                    ObjectiveRadarBuilding(self, j, i)
                if col == 'H':
                    TwoByTwoHole(self, j, i)
                    Hangar(self, j, i)
                if col == 'X':
                    RoadOneX(self, j, i)
                if col == 'Y':
                    RoadOneY(self, j, i)
                if col == 'R':
                    RoadOneUpRight(self, j, i)
                if col == 'r':
                    RoadOneDownRight(self, j, i)
                if col == 'L':
                    RoadOneUpLeft(self, j, i)
                if col == 'l':
                    RoadOneDownLeft(self, j, i)
                if col == '1':
                    Runway(self, j, i)
                if col == 'C':
                    TwoByTwoHole(self, j, i)
                    ControlTower(self, j, i)
                if col == 'P':
                    TwoByTwoHole(self, j, i)
                    HeliPad(self, j, i)
                if col == 'W':
                    Water(self, j, i)
                if col == 'S':
                    Dirt(self, j, i)
                    Scrub(self, j, i)
                if col == 'B':
                    Dirt(self, j, i)
                    Barrels(self, j, i)
                if col == 'T':
                    Dirt(self, j, i)
                    PalmTree(self, j, i)
                if col == 'w':
                    Dirt(self, j, i)
                    Watchtower(self, j, i)
                if col == 'h':
                    TwoByTwoHole(self, j, i)

    def create_vehicle_map_lv1(self):
        for i, row in enumerate(vehicle_map_lv1):
            for j, col in enumerate(row):
                if col == 'S':
                    SAMTruck(self, j, i)
                if col == 'I':
                    Infantry(self, j, i)
                if col == 'A':
                    SpAaG(self, j, i)
                if col == 'f':
                    StationaryFrigate(self, j, i)

    def create_fencing_map_lv1(self):
        for i, row in enumerate(fencing_map_lv1):
            for j, col in enumerate(row):
                if col == 'X':
                    FencingX(self, j, i)
                if col == 'Y':
                    FencingY(self, j, i)
                if col == 'l':
                    FencingBottomleft(self, j, i)
                if col == 'L':
                    FencingTopleft(self, j, i)
                if col == 'r':
                    FencingBottomRight(self, j, i)
                if col == 'R':
                    FencingTopRight(self, j, i)
                if col == 'G':
                    FencingGate(self, j, i)

    def create_reference_sprite(self):
        for i, row in enumerate(REFERENCE_SPRITE):
            for j, col in enumerate(row):
                if col == '1':
                    self.reference = ReferenceSprite(self, j, i)

    def create_blocks_lv1(self):
        for i, row in enumerate(blocks_lv1):
            for j, col in enumerate(row):
                if col == '1':
                    Block(self, j, i)

    def create_ground_map_lv2(self):
        for i, row in enumerate(ground_map_lv2):
            for j, col in enumerate(row):
                if col == 'D':
                    Dirt(self, j, i)
                if col == '2':
                    TwoByTwoHole(self, j, i)
                    RadarBuilding(self, j, i)
                if col == '3':
                    TwoByTwoHole(self, j, i)
                    ObjectiveRadarBuilding(self, j, i)
                if col == 'H':
                    TwoByTwoHole(self, j, i)
                    Hangar(self, j, i)
                if col == 'X':
                    RoadOneX(self, j, i)
                if col == 'Y':
                    RoadOneY(self, j, i)
                if col == 'R':
                    RoadOneUpRight(self, j, i)
                if col == 'r':
                    RoadOneDownRight(self, j, i)
                if col == 'L':
                    RoadOneUpLeft(self, j, i)
                if col == 'l':
                    RoadOneDownLeft(self, j, i)
                if col == '1':
                    Runway(self, j, i)
                if col == 'C':
                    TwoByTwoHole(self, j, i)
                    ControlTower(self, j, i)
                if col == 'P':
                    TwoByTwoHole(self, j, i)
                    HeliPad(self, j, i)
                if col == 'W':
                    Water(self, j, i)
                if col == 'S':
                    Dirt(self, j, i)
                    Scrub(self, j, i)
                if col == 'B':
                    Dirt(self, j, i)
                    Barrels(self, j, i)
                if col == 'T':
                    Dirt(self, j, i)
                    PalmTree(self, j, i)
                if col == 'w':
                    Dirt(self, j, i)
                    Watchtower(self, j, i)
                if col == 'h':
                    TwoByTwoHole(self, j, i)

    def create_vehicle_map_lv2(self):
        for i, row in enumerate(vehicle_map_lv2):
            for j, col in enumerate(row):
                if col == 'S':
                    SAMTruck(self, j, i)
                if col == 'I':
                    Infantry(self, j, i)
                if col == 'A':
                    SpAaG(self, j, i)
                if col == 'T':
                    TankOneSpawnPoint(self, j, i)

    def create_fencing_map_lv2(self):
        for i, row in enumerate(fencing_map_lv2):
            for j, col in enumerate(row):
                if col == 'X':
                    FencingX(self, j, i)
                if col == 'Y':
                    FencingY(self, j, i)
                if col == 'l':
                    FencingBottomleft(self, j, i)
                if col == 'L':
                    FencingTopleft(self, j, i)
                if col == 'r':
                    FencingBottomRight(self, j, i)
                if col == 'R':
                    FencingTopRight(self, j, i)
                if col == 'G':
                    FencingGate(self, j, i)

    def create_blocks_lv2(self):
        for i, row in enumerate(blocks_lv2):
            for j, col in enumerate(row):
                if col == '1':
                    Block(self, j, i)

    def create_ground_map_lv3(self):
        for i, row in enumerate(ground_map_lv3):
            for j, col in enumerate(row):
                if col == 'D':
                    Dirt(self, j, i)
                if col == '2':
                    TwoByTwoHole(self, j, i)
                    RadarBuilding(self, j, i)
                if col == '3':
                    TwoByTwoHole(self, j, i)
                    ObjectiveRadarBuilding(self, j, i)
                if col == 'H':
                    TwoByTwoHole(self, j, i)
                    Hangar(self, j, i)
                if col == 'X':
                    RoadOneX(self, j, i)
                if col == 'Y':
                    RoadOneY(self, j, i)
                if col == 'R':
                    RoadOneUpRight(self, j, i)
                if col == 'r':
                    RoadOneDownRight(self, j, i)
                if col == 'L':
                    RoadOneUpLeft(self, j, i)
                if col == 'l':
                    RoadOneDownLeft(self, j, i)
                if col == '1':
                    Runway(self, j, i)
                if col == 'C':
                    TwoByTwoHole(self, j, i)
                    ControlTower(self, j, i)
                if col == 'P':
                    TwoByTwoHole(self, j, i)
                    HeliPad(self, j, i)
                if col == 'W':
                    Water(self, j, i)
                if col == 'S':
                    Dirt(self, j, i)
                    Scrub(self, j, i)
                if col == 'B':
                    Dirt(self, j, i)
                    Barrels(self, j, i)
                if col == 'T':
                    Dirt(self, j, i)
                    PalmTree(self, j, i)
                if col == 'w':
                    Dirt(self, j, i)
                    Watchtower(self, j, i)
                if col == 'h':
                    TwoByTwoHole(self, j, i)
                if col == 'F':
                    TwoByTwoHole(self, j, i)
                    ObjectiveFactory(self, j, i)

    def create_vehicle_map_lv3(self):
        for i, row in enumerate(vehicle_map_lv3):
            for j, col in enumerate(row):
                if col == 'S':
                    SAMTruck(self, j, i)
                if col == 'I':
                    Infantry(self, j, i)
                if col == 'A':
                    SpAaG(self, j, i)
                if col == 'T':
                    TankOneSpawnPoint(self, j, i)
                if col == 'P':
                    TransportPlane(self, j, i)

    def create_fencing_map_lv3(self):
        for i, row in enumerate(fencing_map_lv3):
            for j, col in enumerate(row):
                if col == 'X':
                    FencingX(self, j, i)
                if col == 'Y':
                    FencingY(self, j, i)
                if col == 'l':
                    FencingBottomleft(self, j, i)
                if col == 'L':
                    FencingTopleft(self, j, i)
                if col == 'r':
                    FencingBottomRight(self, j, i)
                if col == 'R':
                    FencingTopRight(self, j, i)
                if col == 'G':
                    FencingGate(self, j, i)

    def create_blocks_lv3(self):
        for i, row in enumerate(blocks_lv3):
            for j, col in enumerate(row):
                if col == '1':
                    Block(self, j, i)

    def create_ground_map_lv4(self):
        for i, row in enumerate(ground_map_lv4):
            for j, col in enumerate(row):
                if col == 'D':
                    Dirt(self, j, i)
                if col == '2':
                    TwoByTwoHole(self, j, i)
                    RadarBuilding(self, j, i)
                if col == '3':
                    TwoByTwoHole(self, j, i)
                    ObjectiveRadarBuilding(self, j, i)
                if col == 'H':
                    TwoByTwoHole(self, j, i)
                    Hangar(self, j, i)
                if col == 'X':
                    RoadOneX(self, j, i)
                if col == 'Y':
                    RoadOneY(self, j, i)
                if col == 'R':
                    RoadOneUpRight(self, j, i)
                if col == 'r':
                    RoadOneDownRight(self, j, i)
                if col == 'L':
                    RoadOneUpLeft(self, j, i)
                if col == 'l':
                    RoadOneDownLeft(self, j, i)
                if col == '1':
                    Runway(self, j, i)
                if col == 'C':
                    TwoByTwoHole(self, j, i)
                    ControlTower(self, j, i)
                if col == 'P':
                    TwoByTwoHole(self, j, i)
                    HeliPad(self, j, i)
                if col == 'W':
                    Water(self, j, i)
                if col == 'S':
                    Dirt(self, j, i)
                    Scrub(self, j, i)
                if col == 'B':
                    Dirt(self, j, i)
                    Barrels(self, j, i)
                if col == 'T':
                    Dirt(self, j, i)
                    PalmTree(self, j, i)
                if col == 'w':
                    Dirt(self, j, i)
                    Watchtower(self, j, i)
                if col == 'h':
                    TwoByTwoHole(self, j, i)
                if col == 'F':
                    TwoByTwoHole(self, j, i)
                    ObjectiveFactory(self, j, i)

    def create_vehicle_map_lv4(self):
        for i, row in enumerate(vehicle_map_lv4):
            for j, col in enumerate(row):
                if col == 'S':
                    SAMTruck(self, j, i)
                if col == 'I':
                    Infantry(self, j, i)
                if col == 'A':
                    SpAaG(self, j, i)
                if col == 'T':
                    TankOneSpawnPoint(self, j, i)
                if col == 'P':
                    TransportPlane(self, j, i)

    def create_fencing_map_lv4(self):
        for i, row in enumerate(fencing_map_lv4):
            for j, col in enumerate(row):
                if col == 'X':
                    FencingX(self, j, i)
                if col == 'Y':
                    FencingY(self, j, i)
                if col == 'l':
                    FencingBottomleft(self, j, i)
                if col == 'L':
                    FencingTopleft(self, j, i)
                if col == 'r':
                    FencingBottomRight(self, j, i)
                if col == 'R':
                    FencingTopRight(self, j, i)
                if col == 'G':
                    FencingGate(self, j, i)

    def create_blocks_lv4(self):
        for i, row in enumerate(blocks_lv4):
            for j, col in enumerate(row):
                if col == '1':
                    Block(self, j, i)

    def new_lv1(self):
        #   start a new game
        self.playing = True
        self.level = 1
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.p_sprite_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.ref_sprite = pygame.sprite.LayeredUpdates()
        self.overlay_sprites = pygame.sprite.LayeredUpdates()
        self.aoi = pygame.sprite.LayeredUpdates()
        self.flares = pygame.sprite.LayeredUpdates()
        self.helipads = pygame.sprite.LayeredUpdates()
        self.enemy_ground = pygame.sprite.LayeredUpdates()
        self.enemy_air = pygame.sprite.LayeredUpdates()

        self.main_theme.play(-1)
        self.main_theme.set_volume(0.1)
        self.helicopter_sound.set_volume(0.7)
        self.helicopter_sound.play(-1)

        self.create_ground_map_lv1()
        self.create_vehicle_map_lv1()
        self.create_fencing_map_lv1()
        self.create_reference_sprite()
        self.create_blocks_lv1()
        self.player = Player(self, 14, 8)
        self.aoi_sprite = AreaOfInfluence(self, 10, 4)
        self.radar_screen = RadarScreen(self, 744, 260)
        self.last = pygame.time.get_ticks()

        for sprite in self.ref_sprite:
            self.ref_x_pix = sprite.rect.x
            self.ref_y_pix = sprite.rect.y
        
        if self.ref_x_pix != 0:
            self.rel_x = self.ref_x_pix/TILESIZE
        else:
            self.rel_x = self.ref_x_pix

        if self.ref_y_pix != 0:
            self.rel_y = self.ref_y_pix/TILESIZE
        else:
            self.rel_y = self.ref_y_pix

        self.healthbar_images = [
            self.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.health_text = self.font.render('Health:', True, WHITE)
        self.health_text_rect = self.health_text.get_rect(x= 20, y= 570)

        self.convo_text = self.font_mid.render(self.convo, True, BLACK)
        self.convo_text_rect = self.convo_text.get_rect(x= 100, y= 450)

        

        self.gun_ammo_text = self.font_mid.render(f'Gun Ammo: {self.player.gun_ammo}', True, WHITE)
        self.gun_ammo_text_rect = self.gun_ammo_text.get_rect(x=740, y=45)

        self.flare_ammo_text = self.font_mid.render(f'Flare Ammo: {self.player.flare_ammo}', True, WHITE)
        self.flare_ammo_text_rect = self.flare_ammo_text.get_rect(x=740, y=70)

        self.rocket_ammo_text = self.font_mid.render(f'Rocket Ammo: {self.player.rocket_ammo}', True, WHITE)
        self.rocket_ammo_text_rect = self.rocket_ammo_text.get_rect(x=740, y=95)

        self.atgm_ammo_text = self.font_mid.render(f'ATGM Ammo: {self.player.atgm_ammo}', True, WHITE)
        self.atgm_ammo_text_rect = self.atgm_ammo_text.get_rect(x=740, y=120)

        self.aam_ammo_text = self.font_mid.render(f'AAM Ammo: {self.player.aam_ammo}', True, WHITE)
        self.aam_ammo_text_rect = self.aam_ammo_text.get_rect(x=740, y=145)

        self.direction_text = self.font_mid.render(f'N', True, WHITE)
        self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)

        self.controls_button = Button(0, 2, 120, 30, WHITE, BLACK, 'Controls', 26)
        

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]

    def new_lv2(self):
        #   start level 2
        self.playing = True
        
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.p_sprite_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.ref_sprite = pygame.sprite.LayeredUpdates()
        self.overlay_sprites = pygame.sprite.LayeredUpdates()
        self.aoi = pygame.sprite.LayeredUpdates()
        self.flares = pygame.sprite.LayeredUpdates()
        self.helipads = pygame.sprite.LayeredUpdates()
        self.enemy_ground = pygame.sprite.LayeredUpdates()
        self.enemy_air = pygame.sprite.LayeredUpdates()

        
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.1)
        self.helicopter_sound.set_volume(0.7)
        self.helicopter_sound.play(-1)

        self.create_ground_map_lv2()
        self.create_vehicle_map_lv2()
        self.create_fencing_map_lv2()
        self.create_reference_sprite()
        self.create_blocks_lv2()
        self.player = Player(self, 14, 8)
        self.aoi_sprite = AreaOfInfluence(self, 10, 4)
        self.radar_screen = RadarScreen(self, 744, 260)
        self.last = pygame.time.get_ticks()

        for sprite in self.ref_sprite:
            self.ref_x_pix = sprite.rect.x
            self.ref_y_pix = sprite.rect.y
        
        if self.ref_x_pix != 0:
            self.rel_x = self.ref_x_pix/TILESIZE
        else:
            self.rel_x = self.ref_x_pix

        if self.ref_y_pix != 0:
            self.rel_y = self.ref_y_pix/TILESIZE
        else:
            self.rel_y = self.ref_y_pix

        self.healthbar_images = [
            self.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.health_text = self.font.render('Health:', True, WHITE)
        self.health_text_rect = self.health_text.get_rect(x= 20, y= 570)

        self.convo_text = self.font_mid.render(self.convo, True, BLACK)
        self.convo_text_rect = self.convo_text.get_rect(x= 100, y= 450)

        

        self.gun_ammo_text = self.font_mid.render(f'Gun Ammo: {self.player.gun_ammo}', True, WHITE)
        self.gun_ammo_text_rect = self.gun_ammo_text.get_rect(x=740, y=45)

        self.flare_ammo_text = self.font_mid.render(f'Flare Ammo: {self.player.flare_ammo}', True, WHITE)
        self.flare_ammo_text_rect = self.flare_ammo_text.get_rect(x=740, y=70)

        self.rocket_ammo_text = self.font_mid.render(f'Rocket Ammo: {self.player.rocket_ammo}', True, WHITE)
        self.rocket_ammo_text_rect = self.rocket_ammo_text.get_rect(x=740, y=95)

        self.atgm_ammo_text = self.font_mid.render(f'ATGM Ammo: {self.player.atgm_ammo}', True, WHITE)
        self.atgm_ammo_text_rect = self.atgm_ammo_text.get_rect(x=740, y=120)

        self.aam_ammo_text = self.font_mid.render(f'AAM Ammo: {self.player.aam_ammo}', True, WHITE)
        self.aam_ammo_text_rect = self.aam_ammo_text.get_rect(x=740, y=145)

        self.direction_text = self.font_mid.render(f'N', True, WHITE)
        self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)

        self.controls_button = Button(0, 2, 120, 30, WHITE, BLACK, 'Controls', 26)
        

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]


        self.tanks_killed = 0

    def new_lv3(self):
        #   start level 2
        self.playing = True
        
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.p_sprite_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.ref_sprite = pygame.sprite.LayeredUpdates()
        self.overlay_sprites = pygame.sprite.LayeredUpdates()
        self.aoi = pygame.sprite.LayeredUpdates()
        self.flares = pygame.sprite.LayeredUpdates()
        self.helipads = pygame.sprite.LayeredUpdates()
        self.enemy_ground = pygame.sprite.LayeredUpdates()
        self.enemy_air = pygame.sprite.LayeredUpdates()

        
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.1)
        self.helicopter_sound.set_volume(0.7)
        self.helicopter_sound.play(-1)

        self.create_ground_map_lv3()
        self.create_vehicle_map_lv3()
        self.create_fencing_map_lv3()
        self.create_reference_sprite()
        self.create_blocks_lv3()
        self.player = Player(self, 14, 8)
        self.aoi_sprite = AreaOfInfluence(self, 10, 4)
        self.radar_screen = RadarScreen(self, 744, 260)
        self.last = pygame.time.get_ticks()

        for sprite in self.ref_sprite:
            self.ref_x_pix = sprite.rect.x
            self.ref_y_pix = sprite.rect.y
        
        if self.ref_x_pix != 0:
            self.rel_x = self.ref_x_pix/TILESIZE
        else:
            self.rel_x = self.ref_x_pix

        if self.ref_y_pix != 0:
            self.rel_y = self.ref_y_pix/TILESIZE
        else:
            self.rel_y = self.ref_y_pix

        self.healthbar_images = [
            self.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.health_text = self.font.render('Health:', True, WHITE)
        self.health_text_rect = self.health_text.get_rect(x= 20, y= 570)

        self.convo_text = self.font_mid.render(self.convo, True, BLACK)
        self.convo_text_rect = self.convo_text.get_rect(x= 100, y= 450)

        

        self.gun_ammo_text = self.font_mid.render(f'Gun Ammo: {self.player.gun_ammo}', True, WHITE)
        self.gun_ammo_text_rect = self.gun_ammo_text.get_rect(x=740, y=45)

        self.flare_ammo_text = self.font_mid.render(f'Flare Ammo: {self.player.flare_ammo}', True, WHITE)
        self.flare_ammo_text_rect = self.flare_ammo_text.get_rect(x=740, y=70)

        self.rocket_ammo_text = self.font_mid.render(f'Rocket Ammo: {self.player.rocket_ammo}', True, WHITE)
        self.rocket_ammo_text_rect = self.rocket_ammo_text.get_rect(x=740, y=95)

        self.atgm_ammo_text = self.font_mid.render(f'ATGM Ammo: {self.player.atgm_ammo}', True, WHITE)
        self.atgm_ammo_text_rect = self.atgm_ammo_text.get_rect(x=740, y=120)

        self.aam_ammo_text = self.font_mid.render(f'AAM Ammo: {self.player.aam_ammo}', True, WHITE)
        self.aam_ammo_text_rect = self.aam_ammo_text.get_rect(x=740, y=145)

        self.direction_text = self.font_mid.render(f'N', True, WHITE)
        self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)

        self.controls_button = Button(0, 2, 120, 30, WHITE, BLACK, 'Controls', 26)
        

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]


        self.tanks_killed = 0

    def new_lv4(self):
        #   start level 4
        self.playing = True
        
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.p_sprite_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.ref_sprite = pygame.sprite.LayeredUpdates()
        self.overlay_sprites = pygame.sprite.LayeredUpdates()
        self.aoi = pygame.sprite.LayeredUpdates()
        self.flares = pygame.sprite.LayeredUpdates()
        self.helipads = pygame.sprite.LayeredUpdates()
        self.enemy_ground = pygame.sprite.LayeredUpdates()
        self.enemy_air = pygame.sprite.LayeredUpdates()

        
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.1)
        self.helicopter_sound.set_volume(0.7)
        self.helicopter_sound.play(-1)

        self.create_ground_map_lv4()
        self.create_vehicle_map_lv4()
        self.create_fencing_map_lv4()
        self.create_reference_sprite()
        self.create_blocks_lv4()
        self.player = Player(self, 14, 8)
        self.aoi_sprite = AreaOfInfluence(self, 10, 4)
        self.radar_screen = RadarScreen(self, 744, 260)
        self.last = pygame.time.get_ticks()

        for sprite in self.ref_sprite:
            self.ref_x_pix = sprite.rect.x
            self.ref_y_pix = sprite.rect.y
        
        if self.ref_x_pix != 0:
            self.rel_x = self.ref_x_pix/TILESIZE
        else:
            self.rel_x = self.ref_x_pix

        if self.ref_y_pix != 0:
            self.rel_y = self.ref_y_pix/TILESIZE
        else:
            self.rel_y = self.ref_y_pix

        self.healthbar_images = [
            self.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.health_text = self.font.render('Health:', True, WHITE)
        self.health_text_rect = self.health_text.get_rect(x= 20, y= 570)

        self.convo_text = self.font_mid.render(self.convo, True, BLACK)
        self.convo_text_rect = self.convo_text.get_rect(x= 100, y= 450)

        

        self.gun_ammo_text = self.font_mid.render(f'Gun Ammo: {self.player.gun_ammo}', True, WHITE)
        self.gun_ammo_text_rect = self.gun_ammo_text.get_rect(x=740, y=45)

        self.flare_ammo_text = self.font_mid.render(f'Flare Ammo: {self.player.flare_ammo}', True, WHITE)
        self.flare_ammo_text_rect = self.flare_ammo_text.get_rect(x=740, y=70)

        self.rocket_ammo_text = self.font_mid.render(f'Rocket Ammo: {self.player.rocket_ammo}', True, WHITE)
        self.rocket_ammo_text_rect = self.rocket_ammo_text.get_rect(x=740, y=95)

        self.atgm_ammo_text = self.font_mid.render(f'ATGM Ammo: {self.player.atgm_ammo}', True, WHITE)
        self.atgm_ammo_text_rect = self.atgm_ammo_text.get_rect(x=740, y=120)

        self.aam_ammo_text = self.font_mid.render(f'AAM Ammo: {self.player.aam_ammo}', True, WHITE)
        self.aam_ammo_text_rect = self.aam_ammo_text.get_rect(x=740, y=145)

        self.direction_text = self.font_mid.render(f'N', True, WHITE)
        self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)

        self.controls_button = Button(0, 2, 120, 30, WHITE, BLACK, 'Controls', 26)
        

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]


        self.aircraft_killed = 0
        self.troops_landed = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main_theme.stop()
                self.helicopter_sound.stop()
                self.playing = False
                self.running = False

            
        if self.player.health <= 0:
            self.main_theme.stop()
            self.helicopter_sound.stop()
            self.playing = False

        #   get click and pos events and button logic here
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.controls_button.is_pressed(mouse_pos, mouse_pressed):
            self.controls_menu()
       
    def update(self):

        self.all_sprites.update()
        self.overlay_sprites.update()
        self.aoi.update()
        
        
        #   conversation logic

        
        for sprite in self.ref_sprite:
            self.ref_x_pix = sprite.rect.x
            self.ref_y_pix = sprite.rect.y
        
        if self.ref_x_pix != 0:
            self.rel_x = self.ref_x_pix/TILESIZE
        else:
            self.rel_x = self.ref_x_pix

        if self.ref_y_pix != 0:
            self.rel_y = self.ref_y_pix/TILESIZE
        else:
            self.rel_y = self.ref_y_pix


        
        if self.level == 2:
            if self.tanks_killed == 6:
                self.mission_complete()

        if self.level == 4:
            if self.aircraft_killed == 2:
                self.mission_complete()
            elif self.troops_landed >= 10:
                self.mission_failed()

        #   overlay items that needs to update variables
        now = pygame.time.get_ticks()
        if now - self.last >= 1000:

            if self.player.landed:
                self.convo = 'Welcome home Leiutenant - press R for the weapons menu.'
                if now - self.text_timer >= 1000:
                    self.player.landed = False
                    self.convo = ''
                    self.text_timer = now
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.weapon_menu()
            else:
                if self.level == 1:
                    self.convo = 'Head South-East and destroy the RADAR facility. Be careful of the AA guns.'
                if self.level == 2:
                    self.convo = 'Destroy the enemy tanks coming from the South-East. Use rockets for best effect.'
                if self.level == 3:
                    self.convo = 'Destroy the tank factory, use ATGMs against the SAM trucks, green square = lock.'
                if self.level == 4:
                    self.convo = 'Destroy the enemy transport, before it drops its paratroopers in our territory.'

            self.convo_text = self.font_mid.render(self.convo, True, BLACK)
            self.convo_text_rect = self.convo_text.get_rect(x= 100, y= 450)

            self.gun_ammo_text = self.font_mid.render(f'Gun Ammo: {self.player.gun_ammo}', True, WHITE)
            self.gun_ammo_text_rect = self.gun_ammo_text.get_rect(x=740, y=45)

            self.flare_ammo_text = self.font_mid.render(f'Flare Ammo: {self.player.flare_ammo}', True, WHITE)
            self.flare_ammo_text_rect = self.flare_ammo_text.get_rect(x=740, y=70)

            self.rocket_ammo_text = self.font_mid.render(f'Rocket Ammo: {self.player.rocket_ammo}', True, WHITE)
            self.rocket_ammo_text_rect = self.rocket_ammo_text.get_rect(x=740, y=95)

            self.atgm_ammo_text = self.font_mid.render(f'ATGM Ammo: {self.player.atgm_ammo}', True, WHITE)
            self.atgm_ammo_text_rect = self.atgm_ammo_text.get_rect(x=740, y=120)

            self.aam_ammo_text = self.font_mid.render(f'AAM Ammo: {self.player.aam_ammo}', True, WHITE)
            self.aam_ammo_text_rect = self.aam_ammo_text.get_rect(x=740, y=145)

            if self.player.facing == 'up':
                self.direction_text = self.font_mid.render(f'N', True, WHITE)
                self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)
            elif self.player.facing == 'right':
                self.direction_text = self.font_mid.render(f'E', True, WHITE)
                self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)
            elif self.player.facing == 'down':
                self.direction_text = self.font_mid.render(f'S', True, WHITE)
                self.direction_text_rect = self.direction_text.get_rect(x=810, y=550)
            elif self.player.facing == 'left':
                self.direction_text = self.font_mid.render(f'W', True, WHITE)
                self.direction_text_rect = self.direction_text.get_rect(x=807, y=550)


            self.healthbar = self.healthbar_images[0]
            if self.player.pc_health > 90:
                self.healthbar = self.healthbar_images[0]
            elif self.player.pc_health == 90:
                self.healthbar = self.healthbar_images[1]
            elif self.player.pc_health >= 80:
                self.healthbar = self.healthbar_images[2]
            elif self.player.pc_health >= 70:
                self.healthbar = self.healthbar_images[3]
            elif self.player.pc_health >= 60:
                self.healthbar = self.healthbar_images[4]
            elif self.player.pc_health >= 50:
                self.healthbar = self.healthbar_images[5]
            elif self.player.pc_health >= 40:
                self.healthbar = self.healthbar_images[6]
            elif self.player.pc_health >= 30:
                self.healthbar = self.healthbar_images[7]
            elif self.player.pc_health >= 20:
                self.healthbar = self.healthbar_images[8]
            elif self.player.pc_health >= 10:
                self.healthbar = self.healthbar_images[9]
       
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.aoi.draw(self.screen)
        
        

        #   draw overlay
        

        self.screen.blit(self.overlay_bg, (0, 0))
        self.overlay_sprites.draw(self.screen)
        self.screen.blit(self.gun_ammo_text, self.gun_ammo_text_rect)
        self.screen.blit(self.flare_ammo_text, self.flare_ammo_text_rect)
        self.screen.blit(self.rocket_ammo_text, self.rocket_ammo_text_rect)
        self.screen.blit(self.atgm_ammo_text, self.atgm_ammo_text_rect)
        self.screen.blit(self.aam_ammo_text, self.aam_ammo_text_rect)
        self.screen.blit(self.convo_text, self.convo_text_rect)
        self.screen.blit(self.direction_text, self.direction_text_rect)
        self.screen.blit(self.controls_button.image, self.controls_button.rect)
        
        self.screen.blit(self.healthbar, (100, 580))
        self.screen.blit(self.health_text, self.health_text_rect)

        
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('You have been shot down.', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, 350))

        restart_button = Button(10, WIN_HEIGHT-60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                if self.level == 1:
                    self.new_lv1()
                    self.main()
                elif self.level == 2:
                    self.new_lv2()
                    self.main()
                elif self.level == 3:
                    self.new_lv3()
                    self.main()
                elif self.level == 4:
                    self.new_lv4()
                    self.main()

            self.screen.blit(self.game_over_bg, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)


            self.clock.tick(FPS)
            pygame.display.update()

    def mission_failed(self):
            text = self.font.render('MISSION FAILED - You failed your objective.', True, WHITE)
            text_rect = text.get_rect(center=(WIN_WIDTH/2, 350))

            restart_button = Button(10, WIN_HEIGHT-60, 120, 50, WHITE, BLACK, 'Restart', 32)

            for sprite in self.all_sprites:
                sprite.kill()

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()

                if restart_button.is_pressed(mouse_pos, mouse_pressed):
                    if self.level == 1:
                        self.new_lv1()
                        self.main()
                    elif self.level == 2:
                        self.new_lv2()
                        self.main()
                    elif self.level == 3:
                        self.new_lv3()
                        self.main()
                    elif self.level == 4:
                        self.new_lv4()
                        self.main()

                self.screen.blit(self.game_over_bg, (0, 0))
                self.screen.blit(text, text_rect)
                self.screen.blit(restart_button.image, restart_button.rect)


                self.clock.tick(FPS)
                pygame.display.update()

    def mission_complete(self):
        
        self.level += 1
        mission_completed = True

        text = self.font.render('Mission Complete - Congratulations Lieutenant.', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, 350))

        next_button = Button(10, WIN_HEIGHT-60, 180, 50, WHITE, BLACK, 'Next Mission', 32)
        self.helicopter_sound.stop()
        self.main_theme.stop()
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.7)

        for sprite in self.all_sprites:
            sprite.kill()
        for sprite in self.overlay_sprites:
            sprite.kill()
        

        while mission_completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    mission_completed = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if next_button.is_pressed(mouse_pos, mouse_pressed):
                if self.level == 2:
                    self.main_theme.stop()
                    mission_completed = False
                    self.scene_two()
                elif self.level == 3:
                    self.main_theme.stop()
                    mission_completed = False
                    self.scene_three()
                elif self.level == 4:
                    self.main_theme.stop()
                    mission_completed = False
                    self.scene_four()
                elif self.level == 5:
                    self.main_theme.stop()
                elif self.level == 6:
                    self.main_theme.stop()

            self.screen.blit(self.game_over_bg, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(next_button.image, next_button.rect)


            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        play_button = Button(10, WIN_HEIGHT-60, 100, 50, WHITE, BLACK, 'Play', 32)
        #   title = self.font.render('ALPHA-HOTEL-1', True, WHITE)
        #   title_rect = title.get_rect(center=(WIN_WIDTH/2 -10, 350))
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.7)
        last = pygame.time.get_ticks()

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    intro = False
                    self.running = False
                    

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                now = pygame.time.get_ticks()
                if now - last >= 500:
                    intro = False
                    self.scene_one()
                    
                

            self.screen.blit(self.intro_bg, (0, 0))
            #   self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def scene_one(self):
        scene_one = True

        play_button = Button(10, WIN_HEIGHT-60, 100, 50, WHITE, BLACK, 'Next', 32)
        title = self.font.render('ALPHA-HOTEL-1', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2 -10, 50))
        brief_line_1 = self.font_mid.render('AH-1:  That\'s your callsign.  Welcome Lieutenant, here we have the briefing for our first mission;', True, BLACK)
        brief_line_1_rect = brief_line_1.get_rect(x=40, y=150)
        brief_line_2 = self.font_mid.render('We have intelligence of enemy activity just SOUTH-EAST of our base,', True, BLACK)
        brief_line_2_rect = brief_line_2.get_rect(x=40, y=175)
        brief_line_3 = self.font_mid.render('it seems they have taken over a RADAR installation.  We need to strike fast!', True, BLACK)
        brief_line_3_rect = brief_line_3.get_rect(x=40, y=200)
        brief_line_4 = self.font_mid.render('We need to neutralise the facility, you shoud only need your cannon for this mission.  Good luck Lieutenant!', True, BLACK)
        brief_line_4_rect = brief_line_4.get_rect(x=40, y=225)
        brief_label_1 = self.font_mid.render('SPAAG - Self Propelled Anti-Aircraft Guns.', True, RED)
        brief_label_1_rect = brief_label_1.get_rect(x=170, y=310)
        brief_label_2 = self.font_mid.render('Enemy Infantry - Mostly harmless.', True, RED)
        brief_label_2_rect = brief_label_2.get_rect(x=240, y=430)
        brief_label_3 = self.font_mid.render('MISSION OBJECTIVE - Destroy the installation.', True, RED)
        brief_label_3_rect = brief_label_3.get_rect(x=145, y=535)
        objective_image = pygame.image.load('img/mission_1_brief.png')
        last = pygame.time.get_ticks()
        
        self.main_theme.set_volume(0.7)

        while scene_one:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    scene_one = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                now = pygame.time.get_ticks()
                if now - last >= 500:
                    self.main_theme.stop()
                    scene_one = False
                

            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(objective_image, (500, 300))
            self.screen.blit(title, title_rect)
            self.screen.blit(brief_line_1, brief_line_1_rect)
            self.screen.blit(brief_line_2, brief_line_2_rect)
            self.screen.blit(brief_line_3, brief_line_3_rect)
            self.screen.blit(brief_line_4, brief_line_4_rect)
            self.screen.blit(brief_label_1, brief_label_1_rect)
            self.screen.blit(brief_label_2, brief_label_2_rect)
            self.screen.blit(brief_label_3, brief_label_3_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def scene_two(self):
        scene_two = True

        play_button = Button(10, WIN_HEIGHT-60, 100, 50, WHITE, BLACK, 'Next', 32)
        title = self.font.render('ALPHA-HOTEL-1', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2 -10, 50))
        objective_image = pygame.image.load('img/mission_2_brief.png')

        brief_line_1 = self.font_mid.render('Welcome back Lieutenant, here we have the briefing for our next mission;', True, BLACK)
        brief_line_1_rect = brief_line_1.get_rect(x=40, y=150)
        brief_line_2 = self.font_mid.render('The enemy has had word of our strike on the RADAR installation they occupied,  They have sent a', True, BLACK)
        brief_line_2_rect = brief_line_2.get_rect(x=40, y=175)
        brief_line_3 = self.font_mid.render('group of tanks to wait nearby for a retaliatory strike.  We need you to neutralise the tanks.', True, BLACK)
        brief_line_3_rect = brief_line_3.get_rect(x=40, y=200)
        brief_line_4 = self.font_mid.render('Unguided rockets have been unlocked in the helipad menu.  Good luck Lieutenant!', True, BLACK)
        brief_line_4_rect = brief_line_4.get_rect(x=40, y=225)

        last = pygame.time.get_ticks()
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.7)

        while scene_two:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    scene_two = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                now = pygame.time.get_ticks()
                if now - last >= 500:
                    self.main_theme.stop()
                    self.new_lv2()
                    scene_two = False
                

            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(objective_image, (500, 300))
            self.screen.blit(title, title_rect)
            self.screen.blit(brief_line_1, brief_line_1_rect)
            self.screen.blit(brief_line_2, brief_line_2_rect)
            self.screen.blit(brief_line_3, brief_line_3_rect)
            self.screen.blit(brief_line_4, brief_line_4_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def scene_three(self):
        scene_three = True

        play_button = Button(10, WIN_HEIGHT-60, 100, 50, WHITE, BLACK, 'Next', 32)
        title = self.font.render('ALPHA-HOTEL-1', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2 -10, 50))
        objective_image = pygame.image.load('img/mission_3_brief.png')

        brief_line_1 = self.font_mid.render('Welcome back Lieutenant, here we have the briefing for our next mission;', True, BLACK)
        brief_line_1_rect = brief_line_1.get_rect(x=40, y=150)
        brief_line_2 = self.font_mid.render('Excellent work neutralising the tanks, we have intelligence of an enemy facility where they are', True, BLACK)
        brief_line_2_rect = brief_line_2.get_rect(x=40, y=175)
        brief_line_3 = self.font_mid.render('bulding tanks, we want you to strike this facility.  There are enemy SAM trucks protecting the.', True, BLACK)
        brief_line_3_rect = brief_line_3.get_rect(x=40, y=200)
        brief_line_4 = self.font_mid.render('facility so ATGMs have been unlocked in the helipad menu.  Good luck Lieutenant!', True, BLACK)
        brief_line_4_rect = brief_line_4.get_rect(x=40, y=225)

        last = pygame.time.get_ticks()
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.7)

        while scene_three:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    scene_three = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                now = pygame.time.get_ticks()
                if now - last >= 500:
                    self.main_theme.stop()
                    self.new_lv3()
                    scene_three = False
                

            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(objective_image, (500, 300))
            self.screen.blit(title, title_rect)
            self.screen.blit(brief_line_1, brief_line_1_rect)
            self.screen.blit(brief_line_2, brief_line_2_rect)
            self.screen.blit(brief_line_3, brief_line_3_rect)
            self.screen.blit(brief_line_4, brief_line_4_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def scene_four(self):
        scene_four = True

        play_button = Button(10, WIN_HEIGHT-60, 100, 50, WHITE, BLACK, 'Next', 32)
        title = self.font.render('ALPHA-HOTEL-1', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2 -10, 50))
        objective_image = pygame.image.load('img/mission_4_brief.png')

        brief_line_1 = self.font_mid.render('Welcome back Lieutenant, here we have the briefing for our next mission;', True, BLACK)
        brief_line_1_rect = brief_line_1.get_rect(x=40, y=150)
        brief_line_2 = self.font_mid.render('The tank factory raid was a great success, well done Lieutenant!  However, intelligence reports', True, BLACK)
        brief_line_2_rect = brief_line_2.get_rect(x=40, y=175)
        brief_line_3 = self.font_mid.render('enemy paratrooper transport approaching from the south.  We have no fast air at this base currently,', True, BLACK)
        brief_line_3_rect = brief_line_3.get_rect(x=40, y=200)
        brief_line_4 = self.font_mid.render('so you\'re our only hope, AAMs have been unlocked in the weapons menu.  Good luck Lieutenant!', True, BLACK)
        brief_line_4_rect = brief_line_4.get_rect(x=40, y=225)

        last = pygame.time.get_ticks()
        self.main_theme.play(-1)
        self.main_theme.set_volume(0.7)

        while scene_four:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_theme.stop()
                    scene_four = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                now = pygame.time.get_ticks()
                if now - last >= 500:
                    self.main_theme.stop()
                    self.new_lv4()
                    scene_four = False
                

            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(objective_image, (500, 300))
            self.screen.blit(title, title_rect)
            self.screen.blit(brief_line_1, brief_line_1_rect)
            self.screen.blit(brief_line_2, brief_line_2_rect)
            self.screen.blit(brief_line_3, brief_line_3_rect)
            self.screen.blit(brief_line_4, brief_line_4_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def weapon_menu(self):
        weapon_menu = True

        title = self.font.render('Weapons Menu - Choose your weapons.', True, BLACK)
        title_rect = title.get_rect(x=200, y=20)

        rockets_text = self.font_mid.render('Unguided Rocket Pods:  Unguided rockets are perfect for destroying', True, BLACK)
        rockets_text_rect = rockets_text.get_rect(x=200, y=111)
        rockets_text_2 = self.font_mid.render('buildings and convoys due to their quantity. - x 30  - Press 1 to arm.', True, BLACK)
        rockets_text_2_rect = rockets_text_2.get_rect(x=200, y=131)
        rockets_armed = self.font_mid.render('', True, RED)
        rockets_armed_rect = rockets_armed.get_rect(x=800, y=121)
        

        atgm_text = self.font_mid.render('Anti Tank Guided Missiles (ATGM):  Missiles with infra-red tracking', True, BLACK)
        atgm_text_rect = atgm_text.get_rect(x=200, y=236)
        atgm_text_2 = self.font_mid.render('and targeting, perfect for enemy ground vehicles. - x 4  - Press 2 to arm.', True, BLACK)
        atgm_text_2_rect = atgm_text_2.get_rect(x=200, y=256)
        atgm_armed = self.font_mid.render('', True, RED)
        atgm_armed_rect = atgm_armed.get_rect(x=800, y=246)
        

        aam_text = self.font_mid.render('Air to Air Missiles (AAM):  Highly manouverable missiles with infra-red', True, BLACK)
        aam_text_rect = aam_text.get_rect(x=200, y=361)
        aam_text_2 = self.font_mid.render('tracking and targeting, perfect for enemy aircraft. - x 4  - Press 3 to arm.', True, BLACK)
        aam_text_2_rect = aam_text_2.get_rect(x=200, y=381)
        aam_armed = self.font_mid.render('', True, RED)
        aam_armed_rect = aam_armed.get_rect(x=800, y=371)
        


        exit_txt = self.font.render('Press B to exit.', True, BLACK)
        exit_txt_rect = exit_txt.get_rect(x=WIN_WIDTH-200, y=WIN_HEIGHT-50)

        

        while weapon_menu:

            if self.player.rocket_ammo == 30:
                rockets_armed = self.font_mid.render('ARMED', True, RED)
                rockets_armed_rect = rockets_armed.get_rect(x=800, y=121)
            else:
                rockets_armed = self.font_mid.render('', True, RED)
                rockets_armed_rect = rockets_armed.get_rect(x=800, y=121)
            if self.player.atgm_ammo == 4:
                atgm_armed = self.font_mid.render('ARMED', True, RED)
                atgm_armed_rect = atgm_armed.get_rect(x=800, y=246)
            else:
                atgm_armed = self.font_mid.render('', True, RED)
                atgm_armed_rect = atgm_armed.get_rect(x=800, y=246)
            if self.player.aam_ammo == 4:
                aam_armed = self.font_mid.render('ARMED', True, RED)
                aam_armed_rect = aam_armed.get_rect(x=800, y=371)
            else:
                aam_armed = self.font_mid.render('', True, RED)
                aam_armed_rect = aam_armed.get_rect(x=800, y=371)


            for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                    weapon_menu = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                weapon_menu = False
            if keys[pygame.K_1]:
                if self.level >=2:
                    self.player.rocket_ammo = 30
                #   self.player.atgm_ammo = 0
                #   self.player.aam_ammo = 0
            if keys[pygame.K_2]:
                if self.level >= 3:
                #   self.player.rocket_ammo = 0
                    self.player.atgm_ammo = 4
                    self.player.aam_ammo = 0
            if keys[pygame.K_3]:
                if self.level >= 4:
                #   self.player.rocket_ammo = 0
                    self.player.atgm_ammo = 0
                    self.player.aam_ammo = 4

            

            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(self.rocket_img, (100, 100))
            self.screen.blit(self.atgm_img, (100, 225))
            self.screen.blit(self.aam_img, (100, 350))
            self.screen.blit(title, title_rect)
            self.screen.blit(exit_txt, exit_txt_rect)
            
            
            
            

            if self.level == 2:
                self.screen.blit(rockets_text, rockets_text_rect)
                self.screen.blit(rockets_text_2, rockets_text_2_rect)
                self.screen.blit(rockets_armed, rockets_armed_rect)

            if self.level == 3:
                self.screen.blit(rockets_text, rockets_text_rect)
                self.screen.blit(rockets_text_2, rockets_text_2_rect)
                self.screen.blit(rockets_armed, rockets_armed_rect)
                self.screen.blit(atgm_text, atgm_text_rect)
                self.screen.blit(atgm_text_2, atgm_text_2_rect)
                self.screen.blit(atgm_armed, atgm_armed_rect)

            if self.level >= 4:
                self.screen.blit(rockets_text, rockets_text_rect)
                self.screen.blit(rockets_text_2, rockets_text_2_rect)
                self.screen.blit(rockets_armed, rockets_armed_rect)
                self.screen.blit(atgm_text, atgm_text_rect)
                self.screen.blit(atgm_text_2, atgm_text_2_rect)
                self.screen.blit(atgm_armed, atgm_armed_rect)
                self.screen.blit(aam_text, aam_text_rect)
                self.screen.blit(aam_text_2, aam_text_2_rect)
                self.screen.blit(aam_armed, aam_armed_rect)


            self.clock.tick(FPS)

            pygame.display.update()

    def controls_menu(self):
        controls_menu = True

        title = self.font.render('Controls.', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, 50))

        rockets_text = self.font_mid.render('Movement:-', True, BLACK)
        rockets_text_rect = rockets_text.get_rect(x=200, y=111)
        rockets_text_2 = self.font_mid.render('Use W,A,S,D or arrow keys to move.', True, BLACK)
        rockets_text_2_rect = rockets_text_2.get_rect(x=200, y=131)

        atgm_text = self.font_mid.render('Flares:-', True, BLACK)
        atgm_text_rect = atgm_text.get_rect(x=200, y=236)
        atgm_text_2 = self.font_mid.render('Press F for flares, to counter SAM threats.', True, BLACK)
        atgm_text_2_rect = atgm_text_2.get_rect(x=200, y=256)

        aam_text = self.font_mid.render('Weapons:-', True, BLACK)
        aam_text_rect = aam_text.get_rect(x=200, y=361)
        aam_text_2 = self.font_mid.render('SPACE - Cannon, H - Unguided Rockets, G - Guided Missile', True, BLACK)
        aam_text_2_rect = aam_text_2.get_rect(x=200, y=381)

        exit_txt = self.font.render('Press B to exit.', True, BLACK)
        exit_txt_rect = exit_txt.get_rect(x=WIN_WIDTH-200, y=WIN_HEIGHT-50)

        while controls_menu:

            for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                    controls_menu = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                controls_menu = False
            

            self.screen.blit(self.menu_bg, (0, 0))
            
            self.screen.blit(title, title_rect)
            self.screen.blit(exit_txt, exit_txt_rect)
            
            self.screen.blit(rockets_text, rockets_text_rect)
            self.screen.blit(rockets_text_2, rockets_text_2_rect)
            
            self.screen.blit(atgm_text, atgm_text_rect)
            self.screen.blit(atgm_text_2, atgm_text_2_rect)
            
            self.screen.blit(aam_text, aam_text_rect)
            self.screen.blit(aam_text_2, aam_text_2_rect)
            


            self.clock.tick(FPS)

            pygame.display.update()



g = Game()
g.intro_screen()
g.new_lv1()
while g.running:
    g.main()
    

    g.game_over()

pygame.quit()
sys.exit()


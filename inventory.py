import pygame
import random
from config import *
import sys

class ItemStats():
    def __init__(self, name, image, hit_points, attack_strength, is_melee_weapon, is_ranged_weapon, is_food, is_key):

        self.hit_points = hit_points
        
        self.attack_strength = attack_strength
        self.is_melee_weapon = is_melee_weapon
        self.is_ranged_weapon = is_ranged_weapon
        self.is_food = is_food
        self.is_key = is_key
        self.image = image

        self.name = name

    def item_stats(self):
        item = {
                'Name': self.name,
                'Hit Points': self.hit_points,
                'Attack Strength' : self.attack_strength,
                'Is Melee Weapon' : self.is_melee_weapon,
                'Is ranged Weaopn' : self.is_ranged_weapon,
                'Is Food' : self.is_food,
                'Is Key' : self.is_key
            }
        return item


weapon_list = [
    ItemStats('Axe - Basic', pygame.image.load('img/axebasic.png'), 0, 20, True, False, False, False),
    ItemStats('Crossbow', pygame.image.load('img/crossbow.png'), 0, 30, False, True, False, False),
    ItemStats('Axe - Honed', pygame.image.load('img/axebasic.png'), 0, 35, True, False, False, False),
    ItemStats('Longbow', pygame.image.load('img/longbow.png'), 0, 40, False, True, False, False)
]

item_list = [
    ItemStats('Mushroom', pygame.image.load('img/mushroomsingle.png'), 0, 0, False, False, False, False),
    ItemStats('Logs', pygame.image.load('img/logs1.png'), 0, 0, False, False, False, False),
    ItemStats('Mushtew', pygame.image.load('img/cookedmushroom.png'), 0, 0, False, False, True, False),
    ItemStats('Apple', pygame.image.load('img/apple.png'), 0, 0, False, False, True, False)
]



class Inventory():
    def __init__(self):
        self.new_item = None
        self.sel_item = None
        self.inv = [ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False),
                    ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False),
                    ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False),
                    ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False),
                    ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False)
                    ]

    def events(self):
        pass

    def add_item(self, new_item):
        self.new_item = new_item
        
        if self.inv[0].name == 'EMPTY':
            self.inv.insert(0, self.new_item)
        else:
            if self.inv[1].name == 'EMPTY':
                self.inv.insert(1, self.new_item)
            else:
                if self.inv[2].name == 'EMPTY':
                    self.inv.insert(2, self.new_item)
                else:
                    if self.inv[3].name == 'EMPTY':
                        self.inv.insert(3, self.new_item)
                    else:
                        if self.inv[4].name == 'EMPTY':
                            self.inv.insert(4, self.new_item)
                        else:
                            try:
                                if len(self.inv) >= 5:
                                    self.inv.pop(4)
                                    self.inv.insert(4, self.new_item)
                            except IndexError:
                                pass
            
        

    def drop_item(self, item):
        self.sel_item = item
        
        self.inv.remove(self.sel_item)

    def use_item(self, item):
        pass


class WeaponSlot():
    def __init__(self):
        self.new_item = None
        self.sel_item = None
        self.inv = [ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False)
                    
                    ]

    def events(self):
        pass

    def add_item(self, new_item):
        self.new_item = new_item
        try:
            if len(self.inv) >= 1:
                self.inv.pop()
        except IndexError:
            pass
        self.inv.append(self.new_item)

    def drop_item(self, item):
        self.sel_item = item
        self.inv.remove(self.sel_item)


class Couldron():
    def __init__(self):
        self.new_item = None
        self.sel_item = None
        self.inv = [ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False),
                    ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False)                    
                    ]

    def events(self):
        pass

    def add_item(self, new_item):
        self.new_item = new_item
        
        if self.inv[0].name == 'EMPTY':
            self.inv.insert(0, self.new_item)
        elif self.inv[1].name == 'EMPTY':
            self.inv.insert(1, self.new_item)
        else:
            try:
                if len(self.inv) >= 2:
                    self.inv.pop(1)
                    self.inv.insert(1, self.new_item)
            except IndexError:
                pass

    def drop_item(self, item):
        self.sel_item = item
        self.inv.remove(self.sel_item)


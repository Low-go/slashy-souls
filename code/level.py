#level class for sho for sho


import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from debug import debug
from random import choice

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()    #method used for managing sprites
        self.obstacle_sprites = pygame.sprite.Group()   # you put all connected sprites in here. And when needed may update them all at once, or do other operations

        #sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
             'boundary': import_csv_layout('../map/map_Border.csv'),
             'grass': import_csv_layout("E:\zeldaPython\map\map_grass.csv"),
             'object': import_csv_layout("E:\zeldaPython\map\map_objects.csv")
        }
        graphics = {
            'grass': import_folder("E:\zeldaPython\graphics\import_folders\grass"),
            'objects': import_folder("E:\zeldaPython\graphics\import_folders\objects")
        }

        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):  # row var just has what is in world map
                 for col_index, col in enumerate(row):    # but row index keeps ttrack of index number through enumerate
                     if col != '-1':
                         x = col_index * TILESIZE
                         y = row_index * TILESIZE
                         if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                         if style == 'grass':
                             random_grass = choice(graphics['grass'])
                             Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'grass',random_grass)

                         if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'object',surf) # need to fix tiled ids


        #         if col == 'x':
        #             Tile((x, y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #            self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
        self.player = Player((1500,2000), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):   # remember this is how python does inheritance
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating bottom portion of map
        self.floor_surface = pygame.image.load("../map/testmap.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_post = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_post)

    #we need to order sprites. So that when we apply depth it wont seem off
    # depending on which ones were created first or not
    #sprites drawn on top should be those with a higher y position

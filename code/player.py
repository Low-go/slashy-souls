import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load( "../graphics/ZZZ_will_use/darkninja.png").convert_alpha()  # there is no file in here. come back and replace
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # test graphics
        self.import_player_assets()

        #movment
        self.direction = pygame.math.Vector2()  # started with an x and y of 0. altering them positivlye or negativley will influence our direction
        self.speed = 5

        self.attacking = False  #combat timer attributes
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites


    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right':[],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            path = character_path + animation
            self.animations[animation] = import_folder(path)
        print (self.animations)

    #move
    def input(self):
        keys = pygame.key.get_pressed()  # pygame method for up and down

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        #fight
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("ATTACK")



        #mana
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("MAGIC")

    def move(self, speed):
        if self.direction.magnitude() != 0:  # vector of 0 cannot be normalized
            self.direction = self.direction.normalize()


        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):  # checking rectangle of the sprite with the rectangle of the player
                    if self.direction.x > 0:  # player is facing/moving the right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right



        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)


    def cooldown(self):
        current_time = pygame.time.get_ticks() #will be counting whole game

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

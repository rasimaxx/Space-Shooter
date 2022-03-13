import imghdr
from select import select
from tkinter import Y
from turtle import width
import pygame
import os
import time
import random
pygame.font.init() 

# Setup Display
WIDTH, HEIGHT = 700, 800
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# Load Enemy ship
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))

# Load Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

# Load Lasers
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

# Load Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return  0 <= self.y <= height

    def collision(self, obj):
        return collide(self, obj)  

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))

    # Redefine the new width 
    def get_width(self):
        return self.ship_img.get_width()
    # Redefine the new height
    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.max_health = health
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # Create a mask

class Enemy(Ship):
    COLOR_MAP = {
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "red": (RED_SPACE_SHIP, RED_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img) # Create a mask
    
    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2, (offset_x, offset_y)) != None
        
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("arial",50)
    lost_font = pygame.font.SysFont("arial",60)

    player_vel = 5  # Player velocity
    player = Player(300,650)
    lost = False

    enemy_vel = 1
    enemies = []
    wave_length = 5

    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BACKGROUND,(0,0)) # Top Left corner from the screen (0,0)
        # draw text
        level_label = main_font.render(f"Level: {level}",1,(255,255,0))
        lives_label = main_font.render(f"Lives: {lives}",1,(255,255,255))

        WINDOW.blit(level_label,(10,10)) # Top Left corner
        WINDOW.blit(lives_label, (WIDTH-lives_label.get_width()-10,10)) # Top Right corner

        player.draw(WINDOW)

        for enemy in enemies:
            enemy.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("You Lost!!",1,(255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["blue","green","red"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Create buttons to move the ship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height()  < HEIGHT:
            player.y += player_vel
        

        # Create enemies move and increment the lives
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -=1
                enemies.remove(enemy)


main()
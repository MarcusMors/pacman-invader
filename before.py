import pygame
import random
import math
from pygame import mixer
import os
import sys
"""GIFImage by yo"""
from PIL import Image
from pygame.locals import *
import time
pygame.init()
from time import sleep
pygame.font.init()
# Space Invaders
WIDTH, HEIGHT = 1280 , 660 
# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "nave2.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
RAPID_FIRE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "thunder.png")), (50,50))
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH // 2, HEIGHT))
class powerup:
    def __init__(self, x, y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def collision(self, obj):
        return collide(self, obj)
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
        return not(self.y <= height and self.y >= 0)

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
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Playersp(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            laserdx = self.x-self.ship_img.get_width()//2 -7
            laserdy = self.y-self.ship_img.get_height()
            self.y+self.ship_img.get_height()//2
            laser = Laser(laserdx,laserdy , self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class GIFImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False
        self.rect = pygame.rect.Rect((32,32), Image.open(filename).size)

    def get_rect(self):
        return pygame.rect.Rect((32,32), self.image.size)

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0,0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()

        screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames)-1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)
    def fastforward(self):
        self.seek(self.length()-1)

    def get_height(self):
        return self.image.size[1]
    def get_width(self):
        return self.image.size[0]
    def get_size(self):
        return self.image.size
    def length(self):
        return len(self.frames)
    def reverse(self):
        self.reversed = not self.reversed
    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        return new
class Playerpc(object):
    def __init__(self,posx = 20,posy=20):
        self.rect = pygame.Rect(posx, posy, 20,20)
    def move(self, dx, dy):
        # Move each axis separately.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)    
    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], b_p, b_p)
class Point(object):
    def __init__(self, pos):
        points.append(self)
        self.circ = pygame.Rect((pos[0]+b_p/2), (pos[1]+b_p/2), 4, 4)

class Playerpoint(object):
    def __init__(self,posx = 20,posy=20):
        self.rect = pygame.Rect(posx, posy, 20,20)
    def move(self, dx, dy):
        # Move each axis separately.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)   
    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


def image_music_display():
    global pac, ghost, bala
    pac = pygame.image.load('data/basic_pacman.png')
    ghost = pygame.image.load('data/basic_fantasma.png')
    bala = pygame.image.load('data/bala.png')
    icon = pac
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Pacman invader')
    os.environ["SDL_ViDEO_CENTERED"] = "1"

def colours():
    global white, col_map, black, colour_b1
    white = (255,255,255)
    col_map = (0,0,200)
    black = (0,0,0)
    colour_b1 = (40,95,141)

def colision():
    global Playerpc, player, clock, walls ,ghosty,ghostyPink, points, level
    clock = pygame.time.Clock()
    walls = [] # List to hold the walls
    points = []
    player = Playerpoint() # Create the player
    level =[
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X           XX    XX           X',
    'X XXXX XXXX XX XX XX XXXX XXXX X',
    'X XXXX XXXX XX XX XX XXXX XXXX X',
    'X XX           XX           XX X',
    'X XX XXXXXX XX XX XX XXXXXX XX X',
    'X    X---XX XX XX XX XX---X    X',
    'X XX X---   XX    XX   ---X XX X',
    'X XX X---XXXXX    XXXXX---X XX X',
    'X XX XXXXXXXXX    XXXXXXXXX XX X',
    'I              XX              F',
    'X XXXX XXXXXXX XX XXXXXXX XXXX X',
    'X XXXX XXXXXXX XX XXXXXXX XXXX X',
    'X      XXX            XXX      X',
    'XXXXXX XXX XXXX--XXXX XXX XXXXXX',
    'XXXXXX XXX X--------X XXX XXXXXX',
    'I          X--E--W--X          F',
    'XXXXXX XXX X--------X XXX XXXXXX',
    'XXXXXX XXX XXXXXXXXXX XXX XXXXXX',
    'X      XXX            XXX      X',
    'X XXXX XXX XXXXXXXXXX XXX XXXX X',
    'X ---X XXX XXXXXXXXXX XXX X--- X',
    'X ---X         XX         X--- X',
    'X ---X XXXXXXX XX XXXXXXX X--- X',
    'X XXXX XXXXXXX XX XXXXXXX XXXX X',
    'X          XXX    XXX          X',
    'X XXXXXXXX XXX XX XXX XXXXXXXX X',
    'X XXXXXXXX XXX XX XXX XXXXXXXX X',
    'X      XXX     XX     XXX      X',
    'X XXXX XXX XXXXXXXXXX XXX XXXX X',
    'X XXXX XXX XXXXXXXXXX XXX XXXX X',
    'X                              X',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
    x = y = 0
    for row in level:
        for col in row:
            if col == "X":
                Wall((x, y))
            if col == "E":
                ghosty = Playerpc(x,y)
            if col == "W":
                ghostyPink = Playerpc(x,y)
            if col == "I":
                horizontalInical.append([x,y])
            if col == "F":
                horizontalFinal.append([x,y])
            if col == " ":
                Point((x,y))
            x += b_p
        y += b_p
        x = 0

def init():
    global screen,size, horizontal, vertical, b_p, width_mid, lives,horizontalInical,horizontalFinal, score
    pygame.init()
    score = 0
    horizontalInical=[]
    horizontalFinal=[]
    b_p = 20
    lives = 3
    size = horizontal , vertical= 64*b_p, 33*b_p     
    screen = pygame.display.set_mode((size))
    width_mid = 3//2
    image_music_display()
    colours()
    colision()

def buttons(b_x, b_y, b_with, b_height, b_A_color, b_I_color, text, surface,color_font_A, color_font_I, direct=None):
    x, y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    b_font = pygame.font.Font('data/game_over.ttf', b_with//3)

    button = pygame.Rect(int(b_x), int(b_y), int(b_with), int(b_height))
    if button.collidepoint(x,y):
        pygame.draw.rect(surface, b_A_color, button) 
        b_text = b_font.render(text,True,color_font_A)
        
        if click[0] == 1 and direct != None:
            direct()

    else:
        pygame.draw.rect(surface, b_I_color, button) 
        b_text = b_font.render(text,True,color_font_I)
    
    surface.blit(b_text,(int(b_x) + b_with//2 - b_text.get_rect().width//2, int(b_y) + b_height//2 - b_text.get_rect().height//2))               

    return button

def entity_collicion():
    if player.rect.colliderect(ghosty.rect) or player.rect.colliderect(ghostyPink.rect):
        global lives
        player.rect.x = 20
        player.rect.y = 20
        lives -= 1
        if lives == 0:
            main_menu()
    for point in points:
        if player.rect.colliderect(point.circ):
            idx_y = player.move_single_axis.rect.y//20 -1
            idx_x = player.move_single_axis.rect.x//20 -1
            new = []
            new = level[idx_y].split()
            if new[idx_x] == ' ':
                new[idx_x] = "-"
                final = ''
                for char in new:
                    final = final + char
                level[idx_y] = final

def transport_player(p1,p2,horizontal=True):
    sumax = 5 if horizontal else 0
    sumay = 0 if horizontal else 5
    if player.rect.x == p1[0]-sumax and player.rect.y==p1[1]+sumay:
        player.rect.x = p2[0]
        player.rect.y = p2[1]
    if player.rect.x == p2[0]+sumax and player.rect.y==p2[1]-sumay:
        player.rect.x = p1[0]
        player.rect.y = p1[1]
def get_pressed(key):
    if key[pygame.K_w]:
        player.move( 0,-5)
    if key[pygame.K_s]:
        player.move( 0, 5)
    if key[pygame.K_a]:
        player.move(-5, 0)
    if key[pygame.K_d]:
        player.move( 5, 0)

def Interface_menu():   
        fuente = pygame.font.Font('data/game_over.ttf', 300)
        Title_G = fuente.render("Pacman Invader", True, (255,255,255))
        screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 10))

        pos_x = horizontal/2 - 150
        pos_y = Title_G.get_rect().height + 30
        rest =  vertical - pos_y

        b_start = buttons(pos_x,pos_y + rest-(rest/5*5), 300, 50, colour_b1, white, "Start", screen, white, black, game)
        b_options = buttons(pos_x,pos_y + rest-(rest/5*4), 300, 50, colour_b1, white, "Options", screen, white, black, Options)
        b_shop = buttons(pos_x,pos_y + rest-(rest/5*3), 300, 50, colour_b1, white, "Shop", screen, white, black, Shop)
        b_credits = buttons(pos_x, pos_y + rest-(rest/5*2), 300, 50, colour_b1, white, "Credits", screen, white, black,Credits)
        b_exit = buttons(pos_x, pos_y + rest-(rest/5*1), 300, 50, colour_b1, white, "Exit", screen, white, black,Exit)

def col_bg_process():
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)
def pacman_process():
    ghost_move(ghosty)
    ghost_move(ghostyPink)
    for wall in walls:
        pygame.draw.rect(screen, (40,95,141), wall.rect)
    for point in points:
        pygame.draw.rect(screen, (233,189,21), point.circ)

def main_menu():
    mixer.music.stop()
    mixer.music.load("sonidos/snd_title_song.ogg")
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)
    
    init()
    on = True
    while on:
        col_bg_process()
        Interface_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()
    pygame.quit()

def game():
    ### Space Invaders
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 2

    player_vel = 5
    laserplay_vel = 5
    laserenem_vel = 5

    playersp = Playersp(WIDTH//2 + WIDTH//4 - 10, 600)
    rapidfire = powerup(125,125,RAPID_FIRE)
    powu=1

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    loca_x = 20
    loca_y = 20
    
    def redraw_window():
        screen.blit(BG, (WIDTH//2 ,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        screen.blit(lives_label, (WIDTH//2+10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        playersp.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            screen.blit(lost_label, (WIDTH // 2 + lost_label.get_width(), HEIGHT //2))

        pygame.display.update()
    ###
    pacmanplayer = GIFImage('data/pacman.gif')
    fantasmita = GIFImage('data/fantasmaRojo.gif')
    fantasmitaPink = GIFImage('data/fantasmaRosado.gif')
    mixer.music.stop()
    mixer.music.load("sonidos/msc_song.ogg")
    mixer.music.play(-1)
    mixer.music.set_volume(0.1)
    #miscelanea
    def pos_pac(x,y):
        screen.blit(pac,(x,y))
    def pos_ghost(x,y):
        screen.blit(ghost,(x,y))
    ghost_cont = 0
    ghost_cont_limit = random.randint(5,10)
    ghost_mov = random.randint(0,1)

    on = True
    while on:
        ###Space Invaders
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or playersp.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                on = False
                mixer.music.stop()
                mixer.music.load("sonidos/snd_title_song.ogg")
                mixer.music.play(-1)
                mixer.music.set_volume(0.3)
            else:
                continue

        if len(enemies) == 0:
            level += 1
            playersp.COOLDOWN = 30
            player_vel = 5
            laserplay_vel = 5
            wave_length += 5
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(WIDTH // 2 + 50, WIDTH - 50), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and playersp.x - player_vel > WIDTH//2: # left
            playersp.x -= player_vel
        if keys[pygame.K_RIGHT] and playersp.x + player_vel + playersp.get_width() < WIDTH : # right
            playersp.x += player_vel
        if keys[pygame.K_UP] and playersp.y - player_vel > 0: # up
            playersp.y -= player_vel
        if keys[pygame.K_DOWN] and playersp.y + player_vel + playersp.get_height() + 15 < HEIGHT: # down
            playersp.y += player_vel
        if keys[pygame.K_SPACE]:
            playersp.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laserenem_vel, playersp)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, playersp):
                playersp.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        playersp.move_lasers(-laserplay_vel, enemies)
        ###
        screen.blit(BG, (0 ,0))
        pacman_process()
        entity_collicion()
        for i in range(0,len(horizontalInical)):
            transport_player(horizontalInical[i],horizontalFinal[i])
        get_pressed(keys) # qué tecla se está aprentando?

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                mixer.music.load("sonidos/snd_title_song.ogg")
                mixer.music.play(-1)
                mixer.music.set_volume(0.3)
                on = False
        pacmanplayer.render(screen,(player.rect.x,player.rect.y))
        fantasmita.render(screen,(ghosty.rect.x,ghosty.rect.y))
        fantasmitaPink.render(screen,(ghostyPink.rect.x,ghostyPink.rect.y))
        pygame.mouse.set_visible(False)
        if powu == 1 and level > 0 and level < 4:
            rapidfire.draw(screen)
            if rapidfire.x +50 == player.rect.x and player.rect.y<rapidfire.y+18 and player.rect.y>rapidfire.y-18:
                del(rapidfire)
                powu = 0
                playersp.COOLDOWN = 10
                player_vel = 10
                laserplay_vel = 15 
        elif level == 4:
            del(rapidfire)
            powu = 0 
        pygame.display.update()

def Options():
    on = True
    while on:
        screen.fill((0,0,0))
        pygame.mouse.set_visible(True)
        fuente = pygame.font.Font('data/game_over.ttf', 300)
        Title_G = fuente.render("Options", True, (255,255,255))
        screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 50))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()

def Shop():
    on = True
    while on:
        screen.fill((0,0,0))
        pygame.mouse.set_visible(True)
        fuente = pygame.font.Font('data/game_over.ttf', 300)
        Title_G = fuente.render("Shop", True, (255,255,255))
        screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 50))
        #menu_title("Shop")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()

def Credits():
    on = True
    while on:
        screen.fill((0,0,0))
        pygame.mouse.set_visible(True)
        fuente = pygame.font.Font('data/game_over.ttf', 300)
        Title_G = fuente.render("Credits", True, (255,255,255))
        screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 50))
        #menu_title("Credits")        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()

def Exit():
    on = True
    while on:
        screen.fill((0,0,0))
        pygame.mouse.set_visible(True)
        fuente = pygame.font.Font('data/game_over.ttf', 300)
        Title_G = fuente.render("Exit", True, (255,255,255))
        screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 50))
        
        b_yes = buttons(horizontal//3, Title_G.get_rect().height + 120, 200, 50, colour_b1, white,"Yes",screen, white, black)
        b_no = buttons(horizontal//3 + 220, Title_G.get_rect().height + 120, 200, 50, colour_b1, white,"No",screen, white, black)
        
        x, y = pygame.mouse.get_pos()
        if b_yes.collidepoint(x,y):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()
        if b_no.collidepoint(x,y):
            if pygame.mouse.get_pressed()[0] == 1:
                sleep(.15)
                on = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()


def menu_title(title):
    screen.fill((0,0,0))
    pygame.mouse.set_visible(True)
    fuente = pygame.font.Font('data/game_over.ttf', 300)
    Title_G = fuente.render(title, True, (255,255,255))
    screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 50))
def ghost_move(ghost):
    ghost_movement = random.randint(0,3)
    ghost_counter = 0
    ghost_counter_limit = random.randint(5,10)
    if ghost_movement == 0 and ghost_counter <= ghost_counter_limit:
        ghost.move( 0, 2)
        ghost_counter += 1
    elif ghost_movement == 1 and ghost_counter <= ghost_counter_limit:
        ghost.move(-2, 0)
        ghost_counter += 1
    elif ghost_movement == 2 and ghost_counter <= ghost_counter_limit:
        ghost.move( 2, 0)
        ghost_counter += 1
    elif ghost_movement == 3 and ghost_counter <= ghost_counter_limit:
        ghost.move( 0,-2)
        ghost_counter += 1
    else:
        ghost_counter = 0
        ghost_counter_limit = random.randint(5,10)
        ghost_movement = random.randint(0,3)
main_menu()




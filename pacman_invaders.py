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
class Player(object):
    def __init__(self,posx = 20,posy=20):
        self.rect = pygame.Rect(posx, posy, 20,20)
    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
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
    global col_bg, white, col_map, black, colour_b1
    col_bg = (180,20,60)
    white = (255,255,255)
    col_map = (0,0,200)
    black = (0,0,0)
    colour_b1 = (40,95,141)

def colision():
    global Player, player, clock, walls ,ghosty,ghostyPink
    clock = pygame.time.Clock()
    walls = [] # List to hold the walls
    player = Player() # Create the player
    level =[
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X           XX    XX           X',
    'X XXXX XXXX XX XX XX XXXX XXXX X',
    'X XXXX XXXX XX XX XX XXXX XXXX X',
    'X XX           XX           XX X',
    'X XX XXXXXX XX XX XX XXXXXX XX X',
    'X    X   XX XX XX XX XX   X    X',
    'X XX X      XX    XX      X XX X',
    'X XX X   XXXXX    XXXXX   X XX X',
    'X XX XXXXXXXXX    XXXXXXXXX XX X',
    'I              XX              F',
    'X XXXX XXXXXXX XX XXXXXXX XXXX X',
    'X XXXX XXXXXXX XX XXXXXXX XXXX X',
    'X      XXX            XXX      X',
    'XXXXXX XXX XXXX  XXXX XXX XXXXXX',
    'XXXXXX XXX X        X XXX XXXXXX',
    'I          X   E W  X          F',
    'XXXXXX XXX X        X XXX XXXXXX',
    'XXXXXX XXX XXXXXXXXXX XXX XXXXXX',
    'X      XXX            XXX      X',
    'X XXXX XXX XXXXXXXXXX XXX XXXX X',
    'X    X XXX XXXXXXXXXX XXX X    X',
    'X    X         XX         X    X',
    'X    X XXXXXXX XX XXXXXXX X    X',
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
                ghosty = Player(x,y)
            if col == "W":
                ghostyPink = Player(x,y)
            if col == "I":
                horizontalInical.append([x,y])
            if col == "F":
                horizontalFinal.append([x,y])
            x += b_p
        y += b_p
        x = 0

def init():
    global screen,size, horizontal, vertical, b_p, width_mid, lives,horizontalInical,horizontalFinal
    pygame.init()
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

def buttons(b_x, b_y, b_with, b_height, b_color, text, surface,color_font):

    button = pygame.Rect(int(b_x), int(b_y), int(b_with), int(b_height))
    pygame.draw.rect(surface, b_color, button) #b_color (40, 95, 141)
            
    b_font = pygame.font.Font('data/game_over.ttf', b_with//3)

    b_text = b_font.render(text,True,color_font)
    surface.blit(b_text,(int(b_x) + b_with//2 - b_text.get_rect().width//2, int(b_y) + b_height//2 - b_text.get_rect().height//2))
    
    return  button

def entity_collicion():
    if player.rect.colliderect(ghosty.rect) or player.rect.colliderect(ghostyPink.rect):
        global lives
        player.rect.x = 20
        player.rect.y = 20
        lives -= 1
        if lives == 0:
            main_menu()

def transport_player(p1,p2,horizontal=True):
    sumax = 2 if horizontal else 0
    sumay = 0 if horizontal else 2
    if player.rect.x == p1[0]-sumax and player.rect.y==p1[1]+sumay:
        player.rect.x = p2[0]
        player.rect.y = p2[1]
    if player.rect.x == p2[0]+sumax and player.rect.y==p2[1]-sumay:
        player.rect.x = p1[0]
        player.rect.y = p1[1]

def get_pressed(key):
    if key[pygame.K_w]:
        player.move( 0,-2)
    if key[pygame.K_s]:
        player.move( 0, 2)
    if key[pygame.K_a]:
        player.move(-2, 0)
    if key[pygame.K_d]:
        player.move( 2, 0)

def buttons_menu():
    fuente = pygame.font.Font('data/game_over.ttf', 300)
    Title_G = fuente.render("Pacman Invader", True, (255,255,255))
    screen.blit(Title_G, (horizontal//2 - Title_G.get_rect().width//2, 10))
    pos_x = horizontal/2 - 150
    pos_y = Title_G.get_rect().height + 30
    rest =  vertical - pos_y
    x, y = pygame.mouse.get_pos()
    if pos_x + 300 > x > pos_x and pos_y + rest-(rest/5*5) + 50 > y > pos_y + rest-(rest/5*5):
        b_start = buttons(pos_x,pos_y + rest-(rest/5*5), 300, 50, colour_b1, "Start", screen, white)
    else:
        b_start = buttons(pos_x,pos_y + rest-(rest/5*5), 300, 50, white, "Start", screen, black)
    
    if pos_x + 300 > x > pos_x and pos_y + rest-(rest/5*4) + 50 > y > pos_y + rest-(rest/5*4):
       b_options = buttons(pos_x,pos_y + rest-(rest/5*4), 300, 50, colour_b1, "Options", screen, white)
    else:
        b_options = buttons(pos_x,pos_y + rest-(rest/5*4), 300, 50, white, "Options", screen, black)
    
    if pos_x + 300 > x > pos_x and pos_y + rest-(rest/5*3) + 50 > y > pos_y + rest-(rest/5*3):
        b_shop = buttons(pos_x,pos_y + rest-(rest/5*3), 300, 50, colour_b1, "Shop", screen, white)
    else:
        b_shop = buttons(pos_x,pos_y + rest-(rest/5*3), 300, 50, white, "Shop", screen, black)

    if pos_x + 300 > x > pos_x and pos_y + rest-(rest/5*2) + 50 > y > pos_y + rest-(rest/5*2):
        b_credits = buttons(pos_x, pos_y + rest-(rest/5*2), 300, 50, colour_b1, "Credits", screen, white)
    else:
        b_credits = buttons(pos_x, pos_y + rest-(rest/5*2), 300, 50, white, "Credits", screen, black)
    
    if pos_x + 300 > x > pos_x and pos_y + rest-(rest/5*1) + 50 > y > pos_y + rest-(rest/5*1):
        b_exit = buttons(pos_x, pos_y + rest-(rest/5*1), 300, 50, colour_b1, "Exit", screen, white)
    else:
        b_exit = buttons(pos_x, pos_y + rest-(rest/5*1), 300, 50, white, "Exit", screen, black)
    if b_start.collidepoint(x,y):
        if pygame.mouse.get_pressed()[0] == 1:
            game()
    if b_options.collidepoint(x,y):
        if pygame.mouse.get_pressed()[0] == 1:
            Options()
    if b_shop.collidepoint(x,y):
        if pygame.mouse.get_pressed()[0] == 1:
            Shop()
    if b_credits.collidepoint(x,y):
        if pygame.mouse.get_pressed()[0] == 1:
            Credits()
    if b_exit.collidepoint(x,y):
        if pygame.mouse.get_pressed()[0] == 1:
            on = Exit()

def col_bg_process():
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)
def pacman_process():
    ghost_move(ghosty)
    ghost_move(ghostyPink)
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

def main_menu():
    mixer.music.stop()
    mixer.music.load("sonidos/snd_title_song.ogg")
    mixer.music.play(-1)
    init()
    on = True
    while on:
        col_bg_process()
        buttons_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()
    pygame.quit()

def game():
    pacmanplayer = GIFImage('data/pacman.gif')
    fantasmita = GIFImage('data/fantasmaRojo.gif')
    fantasmitaPink = GIFImage('data/fantasmaRosado.gif')
    mixer.music.stop()
    mixer.music.load("sonidos/msc_song.ogg")
    mixer.music.play(-1)
    #miscelanea

    def hubo_colision(x1,x2,y1,y2,hitbox):
        distancia = math.sqrt(math.pow(x1 - x2,2)+math.pow(y1 - y2,2))
        return True if distancia <hitbox else False
    pacman_cambiox=0
    pacman_cambioy=0
    def pos_pac(x,y):
        screen.blit(pac,(x,y))
    
    nav_cambiox=0
    nav_cambioy=0
    nav = pygame.image.load('data/nave2.png')
    navx,navy = size[0]//4 + size[0 ]//2 -(nav.get_size()[0]//2) , size[1] - 2*(nav.get_size()[1])
    def pos_nav(x,y):
        screen.blit(nav,(x,y))
    ghost_cambiox=0
    ghost_cambioy=0
    num_marcs = 5
    marc_juego = []
    marc_p_i_L= []
    marc_p_i_A= []
    marc_t_cambio_L = []
    marc_t_cambio_A = []
    for i in range(num_marcs):
        marc_juego.append(pygame.image.load('data/marc1.png'))
        marc_p_i_L.append(random.randint(size[0]//2,size[0]-marc_juego[i].get_size()[0]))
        marc_p_i_A.append(random.randint(0,size[1]//3))
        marc_t_cambio_L.append(1)
        marc_t_cambio_A.append(10)
    def colocar_marc(x,y,i):
        screen.blit(marc_juego[i],(x,y))
    def pos_ghost(x,y):
        screen.blit(ghost,(x,y))
    balax= navx
    balay= navy
    bala_cambioy = 3
    bala_estado = "Listo" #disparado
    #ghost
    ghost_cont = 0
    ghost_cont_limit = random.randint(5,10)
    ghost_mov = random.randint(0,1)

    on = True
    while on:
        screen.fill(col_bg)
        pygame.draw.line(screen,white,[(horizontal//2),0],[(horizontal//2),vertical],width_mid)
        pacman_process()
        entity_collicion()
        clock.tick(360)
        for i in range(0,len(horizontalInical)):
            transport_player(horizontalInical[i],horizontalFinal[i])
        key = pygame.key.get_pressed()
        get_pressed(key) # qué tecla se está aprentando?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                mixer.music.load("sonidos/snd_title_song.ogg")
                mixer.music.play(-1)
                on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman_cambiox+=1
                if event.key == pygame.K_LEFT:
                    pacman_cambiox-=1
                if event.key == pygame.K_UP:
                    pacman_cambioy-=1
                if event.key == pygame.K_DOWN:
                    pacman_cambioy+=1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pacman_cambiox=0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pacman_cambioy=0


        navx,navy = pygame.mouse.get_pos()[0]-nav.get_size()[0]//2,pygame.mouse.get_pos()[1]-nav.get_size()[0]//2
        if navx >= size[0] - nav.get_size()[0]:
            navx = size[0] - nav.get_size()[0]
        elif navx <=size[0]//2: 
            navx=size[0]//2
        if navy >= size[1]- nav.get_size()[1]:
            navy = size[1] - nav.get_size()[1]
        elif navy <=0:
            navy = 0
        for i in range(num_marcs):
            marc_p_i_L[i] += marc_t_cambio_L[i]
            if marc_p_i_L[i] <=size[0]//2:
                marc_t_cambio_L[i] = 1.3
                marc_p_i_A[i] += marc_t_cambio_A[i]
            elif marc_p_i_L[i] >= size[0] - marc_juego[i].get_size()[0]:
                marc_t_cambio_L[i] = -1.3
                marc_p_i_A[i] += marc_t_cambio_A[i]
            centro = math.sqrt(math.pow(marc_juego[0].get_size()[0]//2 - 0 ,2)+math.pow(marc_juego[0].get_size()[1]//2 - 0,2))
            colision = hubo_colision(marc_p_i_L[i]+marc_juego[i].get_size()[0]//2,balax+bala.get_size()[0]//2,marc_p_i_A[i]+marc_juego[i].get_size()[1]//2,balay,centro)
            if colision:
                bala_estado = "Listo"
                balay= navy
                marc_p_i_L[i]= random.randint(size[0]//2,size[0]-marc_juego[i].get_size()[0])
                marc_p_i_A[i]= random.randint(0,size[1]//3)
            colocar_marc(marc_p_i_L[i],marc_p_i_A[i],i)
        pos_nav(navx,navy)
        if pygame.mouse.get_pressed()[0]:
            if bala_estado == "Listo":
                sonido_bala = mixer.Sound("Sonidos/snd_chomp.ogg")  
                sonido_bala.play()
                balax= navx+(nav.get_size()[0]//2 - bala.get_size()[0]//2)
                balay= navy+(nav.get_size()[0]//2 - bala.get_size()[0]//2)
                bala_estado = "Disparado"
                screen.blit(bala,(balax,balay))
        if balay <=0:
            balay =navy
            bala_estado = "Listo"
        if bala_estado == "Disparado":
            bala_estado = "Disparado"
            screen.blit(bala,(balax,balay))
            balay-=bala_cambioy
    
        pacmanplayer.render(screen,(player.rect.x,player.rect.y))
        fantasmita.render(screen,(ghosty.rect.x,ghosty.rect.y))
        fantasmitaPink.render(screen,(ghostyPink.rect.x,ghostyPink.rect.y))
        pygame.mouse.set_visible(False)
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
        
        b_yes = buttons(horizontal//3, Title_G.get_rect().height + 120, 200, 50, colour_b1,"Yes",screen, white)
        b_no = buttons(horizontal//3 + 220, Title_G.get_rect().height + 120, 200, 50, colour_b1,"No",screen, white)
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
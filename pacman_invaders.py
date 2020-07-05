import pygame
import random

pygame.init()

size = horizontal , vertical= 1280, 720 
screen = pygame.display.set_mode((size))
pac = pygame.image.load('data/basic_pacman.png')
ghost = pygame.image.load('data/basic_fantasma.png')
#miscelanea
icon = pac
pygame.display.set_icon(icon)
pygame.display.set_caption('Pacman invader')
background = (0,0,0)
on = True
pacx,pacy = size[0]//4 - (pac.get_size()[0]//2) , size[1]//2 - (pac.get_size()[1]//2)
ghostx,ghosty = size[0]//4 - (ghost.get_size()[0]//2), size[1] - (pac.get_size()[1])
colour_mid = (255,255,255)
width_mid = 3//2

pacman_cambiox=0
pacman_cambioy=0
def pos_pac(x,y):
    screen.blit(pac,(x,y))
nav_cambiox=0
nav_cambioy=0
def pos_nav(x,y):
    screen.blit(nav,(x,y))
ghost_cambiox=0
ghost_cambioy=0
def pos_ghost(x,y):
    screen.blit(ghost,(x,y))

nav = pygame.image.load('data/nave2.png')
navx,navy = size[0]//4 + size[0]//2 -(nav.get_size()[0]//2) , size[1] - 2*(nav.get_size()[1])
#ghost
ghost_cont = 0
ghost_cont_limit = random.randint(5,10)
ghost_mov = random.randint(0,1)
#ghost

while on:
    screen.fill(background)
    pygame.draw.line(screen,colour_mid,[(horizontal//2),0],[(horizontal//2),vertical],width_mid)
    #fantasma
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
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
            
    #pygame.key.set_repeat() #delay,intervalo
    if pacx >= size[0]//2 - pac.get_size()[0]:
        pacx = size[0]//2 - pac.get_size()[0]
    elif pacx <=0:
        pacx=0 
    if pacy >= size[1]- pac.get_size()[0]:
        pacy = size[1] - pac.get_size()[0]
    elif pacy <=0:
        pacy = 0
    
    if ghost_mov == 0 and ghost_cont <= ghost_cont_limit:
        ghost_cambiox = random.randint(-1,1)
        ghost_cont += 1
    elif ghost_mov == 1 and ghost_cont <= ghost_cont_limit:
        ghost_cambioy = random.randint(-1,1)
        ghost_cont += 1
    else:
        ghost_cont = 0
        ghost_cont_limit = random.randint(5,10)
        ghost_mov = random.randint(0,1)
    pacx +=pacman_cambiox
    pacy +=pacman_cambioy
    
    ghostx+=ghost_cambiox
    ghosty+=ghost_cambioy
    if ghostx >= size[0]//2 - ghost.get_size()[0]:
        ghostx = size[0]//2 - ghost.get_size()[0]
    elif ghostx <=0:
        ghostx=0 
    if ghosty >= size[1]- ghost.get_size()[0]:
        ghosty = size[1] - ghost.get_size()[0]
    elif ghosty <=0:
        ghosty = 0

    navx,navy = pygame.mouse.get_pos()[0]-nav.get_size()[0]//2,pygame.mouse.get_pos()[1]-nav.get_size()[0]//2
    if navx >= size[0] - nav.get_size()[0]:
        navx = size[0] - nav.get_size()[0]
    elif navx <=size[0]//2: 
        navx=size[0]//2
    if navy >= size[1]- nav.get_size()[1]:
        navy = size[1] - nav.get_size()[1]
    elif navy <=0:
        navy = 0
    
    pos_nav(navx,navy)
    pos_pac(pacx,pacy)
    pos_ghost(ghostx,ghosty)
    pygame.mouse.set_visible(False)
    pygame.display.update()
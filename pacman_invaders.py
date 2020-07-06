import pygame
import random
import math
from pygame import mixer
pygame.init()

size = horizontal , vertical= 1280, 660     
screen = pygame.display.set_mode((size))

mixer.music.load("Sonidos/snd_title_song.ogg")
mixer.music.play(-1)
mapa = pygame.image.load('data/map_lines.png')
pac = pygame.image.load('data/basic_pacman.png')
ghost = pygame.image.load('data/basic_fantasma.png')
bala = pygame.image.load('data/bala.png')
icon = pac
pygame.display.set_icon(icon)
pygame.display.set_caption('Pacman invader')
background = (180,20,60)
colour_mid = (255,255,255)
colour_map = (0,0,200)
width_mid = 3//2
def main_menu():
    on = True
    while on:
        screen.fill((0,0,0))
        pygame.mouse.set_visible(True)
        b_start = pygame.Rect(horizontal//2 - 150, vertical//(4), 300, 50) 
        pygame.draw.rect(screen, (40, 95, 141), b_start)
        x, y = pygame.mouse.get_pos()
        if b_start.collidepoint(x,y):
            if pygame.mouse.get_pressed()[0] == 1:
                game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.update()

def game():
    #miscelanea
    pacx,pacy = size[0]//4 - (pac.get_size()[0]//2) , size[1]//2 - (pac.get_size()[1]//2)
    ghostx,ghosty = size[0]//4 - (ghost.get_size()[0]//2), size[1] - (pac.get_size()[1])

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
    num_marcs = 80
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
    bala_cambioy = 2
    bala_estado = "Listo" #disparado

    #ghost
    ghost_cont = 0
    ghost_cont_limit = random.randint(5,10)
    ghost_mov = random.randint(0,1)

    on = True
    while on:
        screen.fill(background)
        pygame.draw.line(screen,colour_mid,[(horizontal//2),0],[(horizontal//2),vertical],width_mid)
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
                
        #pacman location
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
        pos_pac(pacx,pacy)
        pos_ghost(ghostx,ghosty)
        screen.blit(mapa,[0,0])
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
    

        pygame.mouse.set_visible(False)
        pygame.display.update()

main_menu()
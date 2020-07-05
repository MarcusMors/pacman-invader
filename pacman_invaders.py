import pygame
pygame.init()

def pos_pac(x,y):
    ventana.blit()

size = ancho , largo= 1280, 720 
screen = pygame.display.set_mode((size))
speed = [1,1]
pac = pygame.image.load("data/basic_pacman.png")
pacrect = pac.get_rect()
#miscelanea
icon = pac
pygame.display.set_icon(icon)
pygame.display.set_caption('Pacman invader')
background = (120,15,40)
on = True
startup_position_y = size[0]//2 - (pac.get_size()[0]//2)
startup_position_x = size[1]//2 - (pac.get_size()[1]//2)
startup_position = x,y = size[0]//2 - (pac.get_size()[0]//2) , size[1]//2 - (pac.get_size()[1]//2)
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            on = False 
    pacrect = pacrect.move(speed)
    if pacrect.left < 0 or pacrect.right > ancho:
        speed[0] = -speed[0]
    if pacrect.top < 0 or pacrect.bottom > largo:
        speed[1] = -speed[1]
    screen.fill(background)
    screen.blit(pac,(x,y))
    pygame.display.flip()

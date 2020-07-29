import pygame
import time
import random
from os import system
from functions import writeLog, text_objects, limparTela

print('Welcome, player! Before playing, please inform some data.')
name = input('Name: ')
email = input('Email: ')
writeLog(name, email)
system(limparTela())

pygame.init()

#### variaveis globais ####
screen_width = 1280
screen_height = 650
gameDisplay = pygame.display.set_mode( (screen_width, screen_height) )
pygame.display.set_caption('PROJECT: SOLO')
icone = pygame.image.load('stars/solo.png')
pygame.display.set_icon(icone)
explosion_sound = pygame.mixer.Sound('stars/explosao.wav')
explosion_sound.set_volume(0.5)
blast_sound = pygame.mixer.Sound('stars/blaster.wav')
blast_sound.set_volume(0.5)
hit_sound = pygame.mixer.Sound('stars/hit.wav')
hit_sound.set_volume(0.1)
victory_sound = pygame.mixer.Sound('stars/victory.wav')
victory_sound.set_volume(1)
death_sound = pygame.mixer.Sound('stars/death.wav')
death_sound.set_volume(1)
music = pygame.mixer.Sound('stars/backsound.wav')
music.set_volume(0.3)

clock = pygame.time.Clock()
# RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (170, 0, 0)
blue = (50, 180, 250)
yellow = (230, 230, 30)
falcon = pygame.image.load('stars/ship.png')
falcon_width = 180
falcon_height = 70

blaster = pygame.image.load('stars/laser.png')
blast_width = 100
blast_height = 15

back = pygame.image.load('stars/block.png')


### funcoes globais ###

def showFalcon(x, y):
    gameDisplay.blit(falcon, (x, y))

def showBlast(x, y):
    gameDisplay.blit(blaster, (x, y))

def message_display(text, color, font):
    pygame.mixer.Sound.stop(music)
    largeText = pygame.font.Font('freesansbold.ttf', font)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (screen_width/2, screen_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(6)
    game_loop()

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosion_sound)
    pygame.mixer.Sound.play(death_sound)
    message_display('YOU DIED', red, 115)

def writeScore(contador):
    font = pygame.font.SysFont(None, 45)
    text = font.render('Dodged: ' + str(contador), True, white)
    gameDisplay.blit(text, (900, 30))

def shieldDisplay(shield):
    font = pygame.font.SysFont(None, 45)
    if shield > 0:
        text = font.render(f'Shield energy: {shield:.0f}', True, blue)
    else:
        text = font.render('Shield energy: 0', True, blue)
    gameDisplay.blit(text, (900, 70))

# loop do jogo

def game_loop():
    pygame.mixer.Sound.play(music)
    pygame.mixer.Sound.play(blast_sound)

    falcon_X = 0
    falcon_Y = 325
    moveY = 0
    moveX = 0
    blast_speed = 7
    blast_X = 1050
    blast_Y = random.randrange(0, screen_height)
    dodges = 0
    shield = 100
    damage = 1

    while True:
        # inicio - interacao do usuario
        # event.get do pygame devolve uma lista de eventos da janela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                # fecha tudo!
                quit()
            if evento.type  == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    moveY = -10
                elif evento.key == pygame.K_DOWN:
                    moveY = 10
                if evento.key == pygame.K_LEFT:
                    moveX = -10
                elif evento.key == pygame.K_RIGHT:
                    moveX = 10
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    moveY = 0
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    moveX = 0
        falcon_Y += moveY
        falcon_X += moveX
        # fim - interacao com o usuario

        # alterando a cor do fundo de tela
        gameDisplay.fill(black)
        gameDisplay.blit(back, (0, 0))

        showFalcon(falcon_X, falcon_Y)

        showBlast(blast_X, blast_Y)
        blast_X -= blast_speed    

        showBlast(blast_X, blast_Y)
        blast_X -= blast_speed   

        if blast_X < 0:
            pygame.mixer.Sound.play(blast_sound)            
            blast_X = screen_width + blast_width
            blast_speed += 1
            blast_Y = random.randrange(0, screen_height)
            dodges += 1
            damage += dodges/10
        
        writeScore(dodges)
        shieldDisplay(shield)

        if falcon_Y > screen_height - falcon_height:
            falcon_Y = screen_height - falcon_height
        elif falcon_Y < 0:
            falcon_Y = 0
        if falcon_X > screen_width - falcon_width:
            falcon_X = screen_width - falcon_width
        elif falcon_X < 0:
            falcon_X = 0
        
        if falcon_X + 140 > blast_X and blast_X > falcon_X:
            if falcon_Y < blast_Y < falcon_Y + falcon_height:
                if shield > 0:
                    shield -= damage
                    pygame.mixer.Sound.play(hit_sound)
                else:
                    dead()

        if dodges == 35:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(victory_sound)
            message_display('Han Solo escaped! Victory!', yellow, 90)

        pygame.display.update()
        clock.tick(60)

game_loop()
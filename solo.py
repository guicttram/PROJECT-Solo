import pygame
import time
import random

pygame.init()

#### variaveis globais ####
screen_width = 1280
screen_height = 650
gameDisplay = pygame.display.set_mode( (screen_width, screen_height) )
pygame.display.set_caption('PROJECT: SOLO')
icone = pygame.image.load('stars/solo.png')
pygame.display.set_icon(icone)
explosion_sound = pygame.mixer.Sound('stars/explosao.wav')
missile_sound = pygame.mixer.Sound('stars/blaster.wav')



clock = pygame.time.Clock()
# RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (170, 0, 0)
ironMan = pygame.image.load('stars/ship.png')
iron_width = 270
iron_height = 100

missile = pygame.image.load('stars/laser.png')
missile_width = 200
missile_height = 40

back = pygame.image.load('stars/block.png')


### funcoes globais ###

def showIron(x, y):
    gameDisplay.blit(ironMan, (x, y))

def showMissile(x, y):
    gameDisplay.blit(missile, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (screen_width/2, screen_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(3)
    game_loop()

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosion_sound)
    message_display('YOU DIED')

def writeScore(contador):
    font = pygame.font.SysFont(None, 45)
    text = font.render('Desvios: ' + str(contador), True, white)
    gameDisplay.blit(text, (950, 30))

# loop do jogo

def game_loop():
    pygame.mixer.music.load('stars/backsound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.Sound.play(missile_sound)

    iron_X = 0
    iron_Y = 325
    moveY = 0
    missile_speed = 7
    missile_X = 1050
    missile_Y = random.randrange(0, screen_height)
    dodges = 0

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
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    moveY = 0
        iron_Y += moveY
        # fim - interacao com o usuario

        # alterando a cor do fundo de tela
        gameDisplay.fill(black)
        gameDisplay.blit(back, (0, 0))

        showIron(iron_X, iron_Y)

        showMissile(missile_X, missile_Y)
        missile_X -= missile_speed       

        if missile_X < 0:
            pygame.mixer.Sound.play(missile_sound)            
            missile_X = screen_width + missile_width
            missile_speed += 1
            missile_Y = random.randrange(0, screen_height)
            dodges += 1
        
        writeScore(dodges)

        if iron_Y > screen_height - iron_height:
            iron_Y = screen_height - iron_height
        elif iron_Y < 0:
            iron_Y = 0
        
        if iron_X + 150 > missile_X:
            if iron_Y < missile_Y and iron_Y + iron_height > missile_Y or missile_Y + missile_height > iron_Y and missile_Y + missile_height < iron_Y + iron_height:
                dead()
            
        pygame.display.update()
        clock.tick(60)

game_loop()

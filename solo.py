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
blast_sound = pygame.mixer.Sound('stars/blaster.wav')



clock = pygame.time.Clock()
# RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (170, 0, 0)
falcon = pygame.image.load('stars/ship.png')
falcon_width = 270
falcon_height = 100

blaster = pygame.image.load('stars/laser.png')
blast_width = 200
blast_height = 40

back = pygame.image.load('stars/block.png')


### funcoes globais ###

def showFalcon(x, y):
    gameDisplay.blit(falcon, (x, y))

def showBlast(x, y):
    gameDisplay.blit(blaster, (x, y))

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
    pygame.mixer.Sound.play(blast_sound)

    falcon_X = 0
    falcon_Y = 325
    moveY = 0
    moveX = 0
    blast_speed = 7
    blast_X = 1050
    blast_Y = random.randrange(0, screen_height)
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

        if blast_X < 0:
            pygame.mixer.Sound.play(blast_sound)            
            blast_X = screen_width + blast_width
            blast_speed += 1
            blast_Y = random.randrange(0, screen_height)
            dodges += 1
        
        writeScore(dodges)

        if falcon_Y > screen_height - falcon_height:
            falcon_Y = screen_height - falcon_height
        elif falcon_Y < 0:
            falcon_Y = 0
        if falcon_X > screen_width - falcon_width:
            falcon_X = screen_width - falcon_width
        elif falcon_X < 0:
            falcon_X = 0
        
        if falcon_X + 150 > blast_X:
            if falcon_Y < blast_Y and falcon_Y + falcon_height > blast_Y or blast_Y + blast_height > falcon_Y and blast_Y + blast_height < falcon_Y + falcon_height:
                dead()
            
        pygame.display.update()
        clock.tick(60)

game_loop()

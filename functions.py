def writeLog(name, email):
    log = open('log.txt', 'a')
    log.write(f'Nome do jogador: {name}\nEmail: {email}\n')
    log.write('\n')
    log.close()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

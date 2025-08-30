import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Queda do Guardião")
clock = pygame.time.Clock()
running = True

class Personagem:

    def __init__(self, velocityX =0, velocityY = 0, grounde = True, posicaoY = 500, posicaoX = 100):
        self.posicaoY = posicaoY
        self.posicaoX = posicaoX
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.grounde = grounde
        self.colisao = pygame.Rect(self.posicaoX,self.posicaoY, 50, 50)

jogador = Personagem()
class Controles:
    
    def __init__(self, right, left, jump, lower, jogador):
        self.right = right
        self.left = left
        self.jump = jump
        self.lower = lower
        self.jogador = jogador

    def comandos(self, event.key):
        if event.key == self.right:
            self.jogador.posicaoX += 5
        else:
            self.jogador.posicaoX = 0
        if event.key == self.left:
            self.jogador.posicaoX -= 5
        else:
            self.jogador.posicaoX = 0
        if event.key == self.jump:
            self.jogador.velocityY -= 15
        else:
            self.jogador.velocityY = 0
        if event.key == self.lower and self.jogador.grounde == True:
            self.jogador.colisao.height = 15
        else:
            self.jogador.colisao.height = 0
 
controles = Controles(pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, pygame.K_DOWN)

while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), jogador.colisao)

    for event in pygame.event.get():

        if event.type == KEYDOWN: controles.comandos(event.key)
        
        jogador.posicaoX += jogador.velocityX

        # Evento para fechar o jogo
        if event.type == QUIT:
            pygame.quit()
            exit()

    clock.tick(60)
    pygame.display.update()

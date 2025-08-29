import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Queda do Guardião")
clock = pygame.time.Clock()
running = True

class Personagem:

    def __init__(self, posicaoY = 500, posicaoX = 100):
        self.posicaoY = posicaoY
        self.posicaoX = posicaoX
        self.colisao = pygame.Rect(self.posicaoX,self.posicaoY, 50, 50)

jogador = Personagem()
class Controles:
    
    def __init__(self, right, left, jump, lower, jogador):
        self.right = right
        self.left = left
        self.jump = jump
        self.lower = lower
        self.jogador = jogador

    def comandos(self, event.key, personagem):
        event.key == self.right
        event.key == self.left
        event.key == self.jump
        event.key == self.lower
 
controles = Controles(pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE, pygame.K_DOWN)

while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), jogador.colisao)

    for event in pygame.event.get():
    
        controles.comandos(event.key, jogador)

        if event.type == KEYDOWN: controles.comandos(event.key, jogador)

        # Evento para fechar o jogo
        if event.type == QUIT:
            pygame.quit()
            exit()

    clock.tick(60)
    pygame.display.update()
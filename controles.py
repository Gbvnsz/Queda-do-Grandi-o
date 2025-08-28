import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Queda do Guardião")
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():

        # Evento para fechar o jogo
        if event.type == quit:
            pygame.quit()
            exit()
        pygame.display.update()
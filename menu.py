# menu.py
import pygame
from pygame.locals import *
from sys import exit

LARGURA, ALTURA = 800, 600

def safe_load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception:
        surf = pygame.Surface(size if size else (LARGURA, ALTURA))
        surf.fill((20, 20, 30))
        return surf

def carregar_fonte(nome=None, tamanho=48):
    try:
        return pygame.font.SysFont(nome, tamanho)
    except Exception:
        return pygame.font.Font(None, tamanho)

class Titulo:
    def __init__(self, texto, y=120, cor=(255,255,255)):
        self.texto = texto
        self.cor = cor
        self.fonte = carregar_fonte("bahnschrift", 64)
        self.y = y

    def draw(self, tela):
        surf = self.fonte.render(self.texto, True, self.cor)
        rect = surf.get_rect(center=(LARGURA // 2, self.y))
        # sombra leve
        sombra = self.fonte.render(self.texto, True, (0,0,0))
        tela.blit(sombra, sombra.get_rect(center=(rect.centerx+2, rect.centery+2)))
        tela.blit(surf, rect)

class Botao:
    def __init__(self, texto, center, largura=260, altura=56, disabled=False, badge=None):
        self.texto = texto
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.rect.center = center
        self.fonte = carregar_fonte("bahnschrift", 32)
        self.hover = False
        self.disabled = disabled
        self.badge = badge  

        self.cor_base = (40, 40, 60)
        self.cor_hover = (70, 70, 110)
        self.cor_borda = (230, 230, 255)
        self.cor_texto = (255, 255, 255)

    def draw(self, tela):
        cor = self.cor_base
        if not self.disabled and self.hover:
            cor = self.cor_hover
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)
        pygame.draw.rect(tela, self.cor_borda, self.rect, width=2, border_radius=12)
        txt_color = (200,200,200) if self.disabled else self.cor_texto
        txt = self.fonte.render(self.texto, True, txt_color)
        tela.blit(txt, txt.get_rect(center=self.rect.center))
        if self.badge:
            fonte_badge = carregar_fonte("bahnschrift", 16)
            bsurf = fonte_badge.render(self.badge, True, (255,255,255))
            pad = 8
            brect = bsurf.get_rect()
            badge_rect = pygame.Rect(0,0,brect.w+pad*2,brect.h+pad)
            badge_rect.midleft = (self.rect.right - 10, self.rect.top + 14)
            pygame.draw.rect(tela, (180, 120, 40), badge_rect, border_radius=8)
            pygame.draw.rect(tela, (255, 220, 160), badge_rect, width=2, border_radius=8)
            tela.blit(bsurf, bsurf.get_rect(center=badge_rect.center))

    def set_hover(self, mouse_pos):
        if not self.disabled:
            self.hover = self.rect.collidepoint(mouse_pos)
        else:
            self.hover = False

    def clicado(self, mouse_pos):
        return (not self.disabled) and self.rect.collidepoint(mouse_pos)

class MenuBotoes:
    def __init__(self, opcoes):
        self.botoes = []
        base_y = 260
        gap = 80
        for i, opt in enumerate(opcoes):
            center = (LARGURA // 2, base_y + i * gap)
            self.botoes.append(
                Botao(opt["label"], center, disabled=opt.get("disabled", False), badge=opt.get("badge"))
            )
        self.idx_selecionado = 0
        for i, b in enumerate(self.botoes):
            if not b.disabled:
                self.idx_selecionado = i
                b.hover = True
                break

    def atualizar_hover_mouse(self, mouse_pos):
        for i, b in enumerate(self.botoes):
            b.set_hover(mouse_pos)
            if b.hover:
                self.idx_selecionado = i

    def mover_selecao(self, direcao):
        if not self.botoes: return
        n = len(self.botoes)
        novo = self.idx_selecionado
        for _ in range(n):
            novo = (novo + direcao) % n
            if not self.botoes[novo].disabled:
                break
        self.idx_selecionado = novo
        for i, b in enumerate(self.botoes):
            b.hover = (i == self.idx_selecionado and not b.disabled)

    def draw(self, tela):
        for b in self.botoes:
            b.draw(tela)

    def opcao_atual(self):
        return self.botoes[self.idx_selecionado]

    def click(self, mouse_pos):
        for b in self.botoes:
            if b.clicado(mouse_pos):
                return b.texto
        return None

def desenhar_stats_topo(tela, score=None, tempo_segundos=None):
    if score is None and tempo_segundos is None:
        return
    fonte = carregar_fonte("bahnschrift", 24)
    partes = []
    if tempo_segundos is not None:
        partes.append(f"Tempo: {int(tempo_segundos)}s")
    if score is not None:
        partes.append(f"Score: {int(score)}")
    txt = "   |   ".join(partes)
    surf = fonte.render(txt, True, (255,255,255))
    rect = surf.get_rect(topright=(LARGURA-12, 12))
    sombra = fonte.render(txt, True, (0,0,0))
    sombra_rect = sombra.get_rect(topright=(LARGURA-10, 14))
    tela.blit(sombra, sombra_rect)
    tela.blit(surf, rect)

def popup_em_breve(tela, clock, mensagem="Disponível futuramente", duracao_ms=1200):
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    fonte = carregar_fonte("bahnschrift", 32)
    txt = fonte.render(mensagem, True, (255,255,255))
    box_w, box_h = txt.get_width()+60, txt.get_height()+40
    box = pygame.Rect(0,0,box_w, box_h)
    box.center = (LARGURA//2, ALTURA//2)
    pygame.draw.rect(overlay, (30,30,50,230), box, border_radius=16)
    pygame.draw.rect(overlay, (200,200,255,255), box, width=2, border_radius=16)
    overlay.blit(txt, txt.get_rect(center=box.center))
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duracao_ms:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit(); exit()
        tela.blit(overlay, (0,0))
        pygame.display.update()
        clock.tick(60)

def run_menu(score=None, tempo_segundos=None):
    pygame.init()
    tela = pygame.display.set_mode((LARGURA,ALTURA))
    pygame.display.set_caption("Jogo de Nave — Menu")
    clock = pygame.time.Clock()

    bg_path = r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\sprints\Background.jpg"
    background = safe_load_image(bg_path,(LARGURA,ALTURA))

    titulo = Titulo("JOGO DE NAVE")

    opcoes = [
        {"label": "Jogar",              "disabled": False, "badge": None},
        {"label": "Instruções",         "disabled": False, "badge": None},
        {"label": "Naves (Em breve)",   "disabled": True,  "badge": "EM BREVE"},
        {"label": "Sair",               "disabled": False, "badge": None},
    ]
    menu = MenuBotoes(opcoes)

    fonte_info = carregar_fonte("bahnschrift", 18)
    info = fonte_info.render("Use ↑/↓ e Enter — ou clique com o mouse", True, (220,220,220))
    info_rect = info.get_rect(center=(LARGURA//2, ALTURA-60))
    fonte_creditos = carregar_fonte("bahnschrift", 18)
    creditos = fonte_creditos.render("Feito por Gabriel Souza", True, (180,180,180))
    creditos_rect = creditos.get_rect(center=(LARGURA//2, ALTURA-30))

    rodando, escolha = True, None

    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit(); exit()
            if e.type == KEYDOWN:
                if e.key in (K_UP, K_w):
                    menu.mover_selecao(-1)
                elif e.key in (K_DOWN, K_s):
                    menu.mover_selecao(+1)
                elif e.key in (K_RETURN, K_KP_ENTER):
                    botao = menu.opcao_atual()
                    if botao.disabled:
                        popup_em_breve(tela, clock)
                    else:
                        escolha = botao.texto
                        rodando = False
                elif e.key == K_ESCAPE:
                    escolha = "Sair"
                    rodando = False
            if e.type == MOUSEMOTION:
                menu.atualizar_hover_mouse(mouse_pos)
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                for b in menu.botoes:
                    if b.rect.collidepoint(mouse_pos):
                        if b.disabled:
                            popup_em_breve(tela, clock)
                        else:
                            escolha = b.texto
                            rodando = False
                        break

        # desenhar
        tela.blit(background, (0, 0))
        titulo.draw(tela)
        menu.draw(tela)
        desenhar_stats_topo(tela, score=score, tempo_segundos=tempo_segundos)
        tela.blit(info, info_rect)
        tela.blit(creditos, creditos_rect)

        pygame.display.update()
        clock.tick(60)

    return escolha

if __name__=="__main__":
    print("Opção escolhida:", run_menu(score=140, tempo_segundos=57))

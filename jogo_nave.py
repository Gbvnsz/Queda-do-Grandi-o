import pygame
from pygame.locals import *
from sys import exit
import random

def main(duracao_partida_ms=120_000):

    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jogo de Nave")
    clock = pygame.time.Clock()
    running = True

    vida_jogador = 100
    score = 0
    duracao_partida_ms = 120_000  # 60s
    inicio_partida_ms = pygame.time.get_ticks()
    fonte = pygame.font.SysFont(None, 30)

    MUSIC_END = pygame.USEREVENT + 1
    _playlist = []
    _playlist_idx = 0

    # Tentar carregar sprites; se falhar, usar retângulos temporários
    try:
        file_paths = [
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\sprints\Jogador.png",
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\sprints\Inimigo.png",
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\sprints\Tiro.jpg",
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\sprints\BackGroundMenu.jpg"
        ]
        for path in file_paths:
            print(f"Carregando: {path}")
        nave = pygame.image.load(file_paths[0]).convert_alpha()
        nave = pygame.transform.scale(nave, (56, 56))
        inimigo = pygame.image.load(file_paths[1]).convert_alpha()
        inimigo = pygame.transform.scale(inimigo, (48, 48))
        tiro_nave = pygame.image.load(file_paths[2]).convert_alpha()
        tiro_nave = pygame.transform.scale(tiro_nave, (4, 10))
        tiro_inimigo = pygame.image.load(file_paths[2]).convert_alpha()  
        tiro_inimigo = pygame.transform.scale(tiro_inimigo, (4, 10))
        background = pygame.image.load(file_paths[3]).convert()
        background_scaled = pygame.transform.scale(background, (800, 600))
    except FileNotFoundError as e:
        print(f"Arquivos não encontrados: {e}. Usando retângulos temporários.")
        nave = pygame.Surface((40, 40))
        nave.fill((255, 0, 0))
        inimigo = pygame.Surface((30, 30))
        inimigo.fill((0, 0, 255))
        tiro_nave = pygame.Surface((4, 10))
        tiro_nave.fill((0, 255, 0))
        tiro_inimigo = pygame.Surface((4, 10))
        tiro_inimigo.fill((255, 0, 255))
        background = pygame.Surface((800, 600))
        background.fill((0, 0, 0))
        background_scaled = background

    # Posição inicial da nave
    nave_rect = nave.get_rect(center=(400, 550))

    # Listas de elementos
    tiros_nave = []
    tiros_inimigo = []
    inimigos = [inimigo.get_rect(topleft=(x, -30)) for x in range(0, 800, 100)]  

    # Configurações
    velocidade_nave = 5
    velocidade_tiro = 10
    velocidade_inimigo = 3
    contador_tiro_inimigo = 0
    tempo_ultimo_tiro = 0
    delay_tiro_nave = random.randint(50, 70)  
    class TiroNave:
        def __init__(self, x, y):
            self.rect = tiro_nave.get_rect(center=(x, y))

        def mover(self):
            self.rect.y -= velocidade_tiro
            return self.rect.bottom >= 0
    class TiroInimigo:
        def __init__(self, x, y):
            self.rect = tiro_inimigo.get_rect(center=(x, y))

        def mover(self):
            self.rect.y += velocidade_tiro
            return self.rect.top <= 600

    def desenhar_hud(tempo_restante_ms, vida, score):
        segundos = max(0, tempo_restante_ms // 1000)
        texto = f"Tempo: {segundos}s   Vida: {vida}   Score: {score}"
        surf = fonte.render(texto, True, (255, 255, 255))
        screen.blit(surf, (10, 10))

    def novo_inimigo():
        return inimigo.get_rect(topleft=(random.randint(0, 770), -30))

    def musicas():
        global _playlist, _playlist_idx
        _playlist = [
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\audios\Mercury.wav",
            r"C:\Users\Pichau\Documents\Códigos\Faculdade\Jogo 2D\audios\BossMain.wav",
        ]
        _playlist_idx = 0
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.set_endevent(MUSIC_END)
            pygame.mixer.music.load(_playlist[_playlist_idx])
            pygame.mixer.music.set_volume(0.7)   
            pygame.mixer.music.play()            
        except Exception as e:
            print("Erro ao iniciar músicas:", e)

    musicas()

    while running:

        agora_ms = pygame.time.get_ticks()
        tempo_passado_ms = agora_ms - inicio_partida_ms
        tempo_restante_ms = duracao_partida_ms - tempo_passado_ms
        if tempo_restante_ms <= 0 or vida_jogador <= 0:
            # Mostra tela final rápida
            screen.blit(background_scaled, (0, 0))
            msg = "Tempo esgotado!" if tempo_restante_ms <= 0 else "Você ficou sem vida!"
            texto_fim = fonte.render(f"{msg}  Score final: {score}", True, (255, 255, 255))
            screen.blit(texto_fim, (200, 280))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        # Desenhar background
        screen.blit(background_scaled, (0, 0))

        # Movimento da nave
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= velocidade_nave
        if keys[K_RIGHT] and nave_rect.right < 800:
            nave_rect.x += velocidade_nave
        if keys[K_UP] and nave_rect.top > 0:
            nave_rect.y -= velocidade_nave
        if keys[K_DOWN] and nave_rect.bottom < 600:
            nave_rect.y += velocidade_nave

        tempo_atual_frames = agora_ms // (1000 // 60)  
        if keys[K_SPACE] and (tempo_atual_frames - tempo_ultimo_tiro >= delay_tiro_nave):
            tiros_nave.append(TiroNave(nave_rect.centerx, nave_rect.top))
            tempo_ultimo_tiro = tempo_atual_frames
            delay_tiro_nave = random.randint(50, 70)  

        # Disparar tiro dos inimigos
        contador_tiro_inimigo += 1
        if contador_tiro_inimigo >= 60:  
            for inimigo_rect in inimigos:
                if random.random() < 0.3:  
                    tiros_inimigo.append(TiroInimigo(inimigo_rect.centerx, inimigo_rect.bottom))
            contador_tiro_inimigo = 0

        # Atualizar tiros da nave
        for tiro in tiros_nave[:]:
            if not tiro.mover():
                tiros_nave.remove(tiro)

        # Atualizar tiros dos inimigos
        for tiro in tiros_inimigo[:]:
            if not tiro.mover():
                tiros_inimigo.remove(tiro)

        # Atualizar inimigos (descem e reciclam)
        for inimigo_rect in inimigos[:]:
            inimigo_rect.y += velocidade_inimigo
            if inimigo_rect.top > 600:
                inimigos.remove(inimigo_rect)
                inimigos.append(novo_inimigo())

        # Colisão entre tiros da nave e inimigos (+20 score e repõe inimigo)
        for tiro in tiros_nave[:]:
            acertou = False
            for inimigo_rect in inimigos[:]:
                if tiro.rect.colliderect(inimigo_rect):
                    tiros_nave.remove(tiro)
                    inimigos.remove(inimigo_rect)
                    score += 20
                    # repõe novo inimigo para continuar aparecendo até o fim do tempo
                    inimigos.append(novo_inimigo())
                    acertou = True
                    break
            if acertou:
                continue

        # Colisão entre tiros dos inimigos e nave (-20 vida)
        for tiro in tiros_inimigo[:]:
            if tiro.rect.colliderect(nave_rect):
                tiros_inimigo.remove(tiro)
                vida_jogador = max(0, vida_jogador - 20)

        # Desenhar nave, tiros e inimigos
        screen.blit(nave, nave_rect)
        for tiro in tiros_nave:
            screen.blit(tiro_nave, tiro.rect)
        for tiro in tiros_inimigo:
            screen.blit(tiro_inimigo, tiro.rect)
        for inimigo_rect in inimigos:
            screen.blit(inimigo, inimigo_rect)

        desenhar_hud(tempo_restante_ms, vida_jogador, score)

        # Processar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MUSIC_END:
                _playlist_idx = (_playlist_idx + 1) % len(_playlist)
                try:
                    pygame.mixer.music.load(_playlist[_playlist_idx])
                    pygame.mixer.music.play()
                except Exception as e:
                    print("Erro ao trocar música:", e)


        pygame.display.update()
        clock.tick(60)
        
    tempo_jogado_s = max(0, (pygame.time.get_ticks() - inicio_partida_ms) // 1000)
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

    pygame.quit()
    return score, tempo_jogado_s

if __name__ == "__main__":
    s, t = main()
    print(f"[JOGO] SCORE={s}")
    print(f"[JOGO] TEMPO={t}")
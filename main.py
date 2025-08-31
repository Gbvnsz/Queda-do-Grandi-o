# main.py
import subprocess
import sys
import re
import pygame 
from menu import run_menu

def rodar_jogo_e_capturar():
    cmd = [sys.executable, "jogo_nave.py"]
    res = subprocess.run(cmd, text=True, capture_output=True)
    stdout = res.stdout or ""
    m_score = re.search(r"\[JOGO\]\s*SCORE=(\d+)", stdout)
    m_tempo = re.search(r"\[JOGO\]\s*TEMPO=(\d+)", stdout)
    score = int(m_score.group(1)) if m_score else None
    tempo = int(m_tempo.group(1)) if m_tempo else None
    return score, tempo

def parar_musica_menu():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.fadeout(500)  
            pygame.mixer.music.stop()
    except Exception:
        pass

def main():
    ultimo_score = None
    ultimo_tempo = None
    while True:
        escolha = run_menu(score=ultimo_score, tempo_segundos=ultimo_tempo)

        if escolha == "Jogar":
            parar_musica_menu()                  
            score, tempo = rodar_jogo_e_capturar()
            if score is not None: ultimo_score = score
            if tempo is not None: ultimo_tempo = tempo

        elif escolha == "Opções":
            continue

        elif escolha == "Sair":
            parar_musica_menu()                  
            break
        else:
            break

if __name__ == "__main__":
    main()

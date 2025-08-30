# main.py
import subprocess
import sys
import re
from menu import run_menu

def rodar_jogo_e_capturar():

    cmd = [sys.executable, "jogo_nave.py"]  
    try:
        res = subprocess.run(cmd, text=True, capture_output=True)
        stdout = res.stdout or ""
        m_score = re.search(r"\[JOGO\]\s*SCORE=(\d+)", stdout)
        m_tempo = re.search(r"\[JOGO\]\s*TEMPO=(\d+)", stdout)
        score = int(m_score.group(1)) if m_score else None
        tempo = int(m_tempo.group(1)) if m_tempo else None
        return score, tempo
    except Exception as e:
        print("Erro ao executar o jogo:", e)
        return None, None

def main():
    ultimo_score = None
    ultimo_tempo = None
    while True:
        escolha = run_menu(score=ultimo_score, tempo_segundos=ultimo_tempo)

        if escolha == "Jogar":
            score, tempo = rodar_jogo_e_capturar()
            if score is not None: ultimo_score = score
            if tempo is not None: ultimo_tempo = tempo

        elif escolha == "Instruções":
            continue

        else:
            break

if __name__ == "__main__":
    main()

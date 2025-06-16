import itertools
import random
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Parâmetros globais
N = 25  # universo [1..25]
B = 15  # tamanho dos blocos SB15
K = 14  # tamanho dos subconjuntos a serem cobertos (k = 11)

# -------------------------------
# Funções auxiliares
# -------------------------------

def gerar_todos_subconjuntos_k():
    """Gera todos os subconjuntos de tamanho k do universo [1..N]"""
    return list(itertools.combinations(range(1, N+1), K))

def gerar_blocos_amostrados(tamanho=50000):
    """Gera uma amostra aleatória de blocos de tamanho B"""
    return [tuple(sorted(random.sample(range(1, N+1), B))) for _ in range(tamanho)]

def subconjuntos_de_um_bloco(bloco):
    """Retorna todos os subconjuntos de tamanho K de um bloco B"""
    return list(itertools.combinations(bloco, K))

# -------------------------------
# Algoritmo Greedy com Amostragem
# -------------------------------

def greedy_com_amostragem(max_iter=10000, amostra_por_iter=50000):
    start = time.time()

    universo = set(gerar_todos_subconjuntos_k())
    total_a_cobrir = len(universo)
    print(f"Total de subconjuntos k={K} a cobrir: {total_a_cobrir}")

    cobertos = set()
    blocos_escolhidos = []
    iteracao = 0

    while len(cobertos) < total_a_cobrir and iteracao < max_iter:
        iteracao += 1
        melhor_bloco = None
        melhor_ganho = 0

        amostra = gerar_blocos_amostrados(amostra_por_iter)

        for bloco in amostra:
            subks = subconjuntos_de_um_bloco(bloco)
            ganho = sum(1 for s in subks if s not in cobertos)
            if ganho > melhor_ganho:
                melhor_ganho = ganho
                melhor_bloco = bloco

        if melhor_bloco is None:
            print("Não há mais blocos útis. Encerrando antecipadamente.")
            break

        blocos_escolhidos.append(melhor_bloco)
        for s in subconjuntos_de_um_bloco(melhor_bloco):
            cobertos.add(s)

        print(f"Iteração {iteracao}: {len(cobertos)} / {total_a_cobrir} cobertos - {len(blocos_escolhidos)} blocos")

    tempo_exec = time.time() - start
    return blocos_escolhidos, tempo_exec

# -------------------------------
# Redução Local
# -------------------------------

def reducao_local(blocos, universo_k):
    cobertos = set()
    for bloco in blocos:
        for s in subconjuntos_de_um_bloco(bloco):
            cobertos.add(s)

    blocos_atuais = blocos.copy()
    random.shuffle(blocos_atuais)
    i = 0

    while i < len(blocos_atuais):
        candidato = blocos_atuais[i]
        cobertos_tmp = cobertos.copy()
        for s in subconjuntos_de_um_bloco(candidato):
            cobertos_tmp.discard(s)

        ainda_cobre_tudo = all(any(s in subconjuntos_de_um_bloco(b) for b in blocos_atuais if b != candidato) for s in subconjuntos_de_um_bloco(candidato))

        if ainda_cobre_tudo:
            blocos_atuais.remove(candidato)
            cobertos = cobertos_tmp
            i = 0  # recomeça busca
        else:
            i += 1

    return blocos_atuais

# -------------------------------
# Gráfico para estimativa dos demais Ks
# -------------------------------

def plotar_estimativa(dados_experimentais):
    ks = sorted(dados_experimentais.keys())
    blocos = [dados_experimentais[k] for k in ks]

    # Ajuste polinomial
    z = np.polyfit(ks, blocos, deg=2)
    p = np.poly1d(z)

    # Estimativas
    ks_futuros = [12, 13, 14]
    estimados = [int(p(k)) for k in ks_futuros]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(ks, blocos, 'o-', label='Resultado experimental')
    plt.plot(ks_futuros, estimados, 'x--', label='Estimativa (extrapolação)')
    for k, y in zip(ks_futuros, estimados):
        plt.text(k, y+200, f"{y}", ha='center')

    plt.xlabel('Valor de k')
    plt.ylabel('Quantidade de blocos SB15_k')
    plt.title('Estimativa por curva de tendência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return dict(zip(ks_futuros, estimados))

# -------------------------------
# Execução principal
# -------------------------------
if __name__ == "__main__":
    blocos_iniciais, tempo_exec = greedy_com_amostragem()
    print(f"Tempo total (greedy): {tempo_exec:.2f} segundos")

    print("Aplicando redução local...")
    universo_k = set(gerar_todos_subconjuntos_k())
    blocos_reduzidos = reducao_local(blocos_iniciais, universo_k)

    print(f"Total final de blocos SB15_{K} após redução: {len(blocos_reduzidos)}")

    # Simula dados fictícios de k = 12,13,14 com base nesse resultado
    dados_k = {11: len(blocos_reduzidos)}
    estimados = plotar_estimativa(dados_k)

    print("\nEstimativas de blocos SB15_k:")
    for k, val in estimados.items():
        print(f"k = {k}: {val} blocos (R$ {val * 3:.2f})")

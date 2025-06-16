import itertools
import random
import time

N = 25
B = 15
K = 11

def gerar_todos_subconjuntos_k():
    return list(itertools.combinations(range(1, N+1), K))

def gerar_blocos_amostrados(tamanho=50000):
    return [tuple(sorted(random.sample(range(1, N+1), B))) for _ in range(tamanho)]

def subconjuntos_de_um_bloco(bloco):
    return list(itertools.combinations(bloco, K))

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

def reducao_local(blocos):
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
            i = 0
        else:
            i += 1
    return blocos_atuais

if __name__ == "__main__":
    blocos_iniciais, tempo_exec = greedy_com_amostragem()
    print(f"Tempo total (greedy): {tempo_exec:.2f} segundos")
    print("Aplicando redução local...")
    blocos_reduzidos = reducao_local(blocos_iniciais)
    print(f"Total final de blocos SB15_{K} após redução: {len(blocos_reduzidos)}")
    custo = len(blocos_reduzidos) * 3.0
    print(f"Custo financeiro para jogar SB15_{K}: R$ {custo:.2f}") 
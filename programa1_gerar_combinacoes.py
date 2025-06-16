import itertools

N = 25  # universo [1..25]

# Função para calcular combinações
def contar_combinacoes(n, k):
    return len(list(itertools.combinations(range(1, n+1), k)))

if __name__ == "__main__":
    s15 = contar_combinacoes(N, 15)
    s14 = contar_combinacoes(N, 14)
    s13 = contar_combinacoes(N, 13)
    s12 = contar_combinacoes(N, 12)
    s11 = contar_combinacoes(N, 11)

    print(f"(a) S15: {s15} combinações de 15 números distintos")
    print(f"(b) S14: {s14} combinações de 14 números distintos")
    print(f"(c) S13: {s13} combinações de 13 números distintos")
    print(f"(d) S12: {s12} combinações de 12 números distintos")
    print(f"(e) S11: {s11} combinações de 11 números distintos") 
import heapq
from collections import defaultdict


class NoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def gerar_codigos(raiz, codigo_atual, codigos):
    if raiz is not None:
        if raiz.char is not None:
            codigos[raiz.char] = codigo_atual
        else:
            gerar_codigos(raiz.left, codigo_atual + "0", codigos)
            gerar_codigos(raiz.right, codigo_atual + "1", codigos)


def construir_arvore(texto):
    if not texto:
        return None, {}

    frequencias = defaultdict(int)
    for char in texto:
        frequencias[char] += 1

    heap = [NoHuffman(c, f) for c, f in frequencias.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        raiz = heapq.heappop(heap)
        return raiz, {raiz.char: "0"}

    while len(heap) > 1:
        no1 = heapq.heappop(heap)
        no2 = heapq.heappop(heap)
        novo_no = NoHuffman(None, no1.freq + no2.freq)
        novo_no.left = no1
        novo_no.right = no2
        heapq.heappush(heap, novo_no)

    raiz = heapq.heappop(heap)
    codigos = {}
    gerar_codigos(raiz, "", codigos)
    return raiz, codigos

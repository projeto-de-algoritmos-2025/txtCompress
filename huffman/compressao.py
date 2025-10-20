def comprimir(texto, codigos):
    return ''.join(codigos[c] for c in texto)


def descomprimir(bits, tabela_codigos):
    inverso = {v: k for k, v in tabela_codigos.items()}
    resultado = []
    buffer = ""
    for bit in bits:
        buffer += bit
        if buffer in inverso:
            resultado.append(inverso[buffer])
            buffer = ""
    return ''.join(resultado)

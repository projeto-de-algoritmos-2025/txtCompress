import json


def bits_para_bytes(bits):
    b = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8].ljust(8, '0')
        b.append(int(byte, 2))
    return bytes(b)


def bytes_para_bits(b):
    return ''.join(f'{byte:08b}' for byte in b)


def salvar_huf(tabela_codigos, bits):
    tabela_bytes = json.dumps(tabela_codigos).encode('utf-8')
    tamanho_tabela = len(tabela_bytes).to_bytes(4, 'big')
    bits_bytes = bits_para_bytes(bits)
    return tamanho_tabela + tabela_bytes + bits_bytes


def ler_huf(conteudo_bytes):
    tamanho_tabela = int.from_bytes(conteudo_bytes[:4], 'big')
    tabela_bytes = conteudo_bytes[4:4 + tamanho_tabela]
    bits_bytes = conteudo_bytes[4 + tamanho_tabela:]
    tabela_codigos = json.loads(tabela_bytes.decode('utf-8'))
    bits = bytes_para_bits(bits_bytes)
    return tabela_codigos, bits

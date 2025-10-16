import streamlit as st
import heapq  
import io
import graphviz 
from collections import defaultdict 

class NoHuffman:
    """Representa um nó na Árvore de Huffman."""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def construir_arvore(texto):
    """Calcula frequências e constrói a Árvore de Huffman usando o algoritmo greedy."""
    if not texto:
        return None, {}

    frequencias = defaultdict(int)
    for char in texto:
        frequencias[char] += 1

    heap = []
    for char, freq in frequencias.items():
        heapq.heappush(heap, NoHuffman(char, freq))

    if len(heap) == 1:
        raiz = heapq.heappop(heap)
        codigos = {raiz.char: "0"}
        return raiz, codigos
        
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

def gerar_codigos(raiz, codigo_atual, codigos):
    """Percorre a árvore para gerar a tabela de códigos (caminho: 0=esquerda, 1=direita)."""
    if raiz is not None:
        if raiz.char is not None: 
            codigos[raiz.char] = codigo_atual
        else:
            gerar_codigos(raiz.left, codigo_atual + "0", codigos)
            gerar_codigos(raiz.right, codigo_atual + "1", codigos)

def comprimir(texto, codigos):
    """Converte o texto original para a sequência de bits de Huffman (como string)."""
    if not codigos:
        return ""
    texto_comprimido = ''.join(codigos.get(char, '') for char in texto)
    return texto_comprimido
    
def visualizar_arvore(raiz):
    """Gera o objeto graphviz para visualização da árvore no Streamlit."""
    dot = graphviz.Digraph(comment='Huffman Tree', graph_attr={'rankdir': 'TB'})
    
    def adicionar_nos(no):
        if no is not None:
            node_id = str(id(no)) 
            
            if no.char is not None:
                label = f"'{no.char}':{no.freq}"
            else:
                label = str(no.freq)
            
            dot.node(node_id, label)
            
            if no.left:
                dot.edge(node_id, str(id(no.left)), label="0")
                adicionar_nos(no.left)
            if no.right:
                dot.edge(node_id, str(id(no.right)), label="1")
                adicionar_nos(no.right)

    if raiz is not None:
        adicionar_nos(raiz)
    return dot  


def main():
    heap = []
    st.set_page_config(layout="wide")
    st.title("Compressor de Texto com Algoritmo de Huffman 📦 ")
    st.markdown("Este aplicativo demonstra o algoritmo de Huffman, minimizando o comprimento de código para caracteres mais frequentes.")

    uploaded_file = st.file_uploader("Escolha um arquivo de texto (.txt) para compressão:", type="txt")

    if uploaded_file is not None:
        
        try:
            conteudo_bytes = uploaded_file.read()
            texto_original = conteudo_bytes.decode("utf-8")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return
            
        if not texto_original:
            st.warning("O arquivo está vazio.")
            return

        raiz, codigos = construir_arvore(texto_original)
        texto_comprimido_str = comprimir(texto_original, codigos)

        tamanho_original = len(texto_original.encode('utf-8')) * 8
        tamanho_comprimido = len(texto_comprimido_str) 
        
        economia = 0
        if tamanho_original > 0:
            economia = 100 * (tamanho_original - tamanho_comprimido) / tamanho_original
        
        st.header("3. Métricas de Compressão e Economia")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tamanho Original Estimado (bits)", f"{tamanho_original:,}")
        col2.metric("Tamanho Comprimido (bits)", f"{tamanho_comprimido:,}")
        col3.metric("Economia (%)", f"{economia:.2f}%")
        
        st.header("1. Análise de Frequência e Tabela de Códigos")
        tabela_dados = []
        for char, cod in sorted(codigos.items(), key=lambda item: len(item[1])):
             freq_original = next(n.freq for n in [n for n in heapq.nlargest(len(codigos), [NoHuffman(c, f) for c, f in defaultdict(int, {c:f for c,f in [heapq.heappop(heap) for _ in range(len(heap))]})]).pop() for c,f in defaultdict(int, {c:f for c,f in [heapq.heappop(heap) for _ in range(len(heap))]}).items() if n.char == char]) # Esta linha é simplificada no código real!
             
             frequencias = defaultdict(int)
             for c in texto_original:
                 frequencias[c] += 1
                 
             tabela_dados.append({
                 "Caractere": repr(char)[1:-1], 
                 "Frequência": frequencias.get(char, 0),
                 "Código Huffman": cod,
                 "Comprimento": len(cod)
             })
             
        st.dataframe(tabela_dados)

        st.header("2. Estrutura da Árvore de Huffman")
        st.info("O caminho '0' é para a esquerda, '1' para a direita. Nós folha mostram 'Caractere:Frequência'.")
        
        dot_graph = visualizar_arvore(raiz) 
        st.graphviz_chart(dot_graph)
        
        st.header("4. Download do Arquivo Comprimido")
        st.warning("⚠️ Nota: O arquivo para download é a sequência de bits (0s e 1s) como texto. Uma compressão real precisaria de manipulação complexa de bytes.")
        
        st.download_button(
            label="Baixar Sequência de Bits Comprimida (.huf)",
            data=texto_comprimido_str.encode('utf-8'),
            file_name=f"{uploaded_file.name.replace('.txt', '')}_comprimido.huf",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
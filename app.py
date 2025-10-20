import streamlit as st
from collections import defaultdict
from huffman.arvore import construir_arvore
from huffman.compressao import comprimir, descomprimir
from huffman.io_utils import bits_para_bytes, salvar_huf, ler_huf
from huffman.visualizacao import visualizar_arvore


def main():
    st.set_page_config(layout="wide")
    st.title("Compressor/Descompressor Huffman")
    st.markdown("Aplicação para compressão e descompressão de texto baseada no algoritmo de Huffman.")

    aba = st.radio("Escolha a operação:", ["Comprimir", "Descomprimir"])

    # ----------------- COMPRIMIR -----------------
    if aba == "Comprimir":
        uploaded_file = st.file_uploader("Escolha um arquivo de texto (.txt):", type="txt")
        if uploaded_file:
            texto = uploaded_file.read().decode("utf-8")
            if not texto:
                st.warning("Arquivo vazio!")
                return

            raiz, codigos = construir_arvore(texto)
            bits = comprimir(texto, codigos)

            tamanho_original = len(texto.encode('utf-8')) * 8
            tamanho_comprimido_bytes = len(bits_para_bytes(bits))
            tamanho_comprimido_bits = tamanho_comprimido_bytes * 8
            economia = 100 * (tamanho_original - tamanho_comprimido_bits) / tamanho_original

            st.header("Métricas")
            col1, col2, col3 = st.columns(3)
            col1.metric("Original (bits)", f"{tamanho_original:,}")
            col2.metric("Comprimido (bits)", f"{tamanho_comprimido_bits:,}")
            col3.metric("Economia (%)", f"{economia:.2f}%")

            # Tabela de códigos
            st.header("Tabela de Códigos Huffman")
            frequencias = defaultdict(int)
            for c in texto:
                frequencias[c] += 1
            tabela_dados = [
                {"Caractere": repr(c)[1:-1], "Frequência": frequencias[c], "Código": cod, "Comprimento": len(cod)}
                for c, cod in sorted(codigos.items(), key=lambda x: len(x[1]))
            ]
            st.table(tabela_dados)

            # Árvore
            st.header("Árvore de Huffman")
            st.graphviz_chart(visualizar_arvore(raiz))

            # Download .huf
            st.header("Download .huf")
            huf_bytes = salvar_huf(codigos, bits)
            st.download_button(
                "Baixar arquivo comprimido (.huf)",
                data=huf_bytes,
                file_name=f"{uploaded_file.name.replace('.txt','')}_comprimido.huf",
                mime="application/octet-stream"
            )

    # ----------------- DESCOMPRIMIR -----------------
    else:
        uploaded_huf = st.file_uploader("Escolha o arquivo comprimido (.huf):", type="huf")
        if uploaded_huf:
            conteudo_bytes = uploaded_huf.read()
            tabela_codigos, bits = ler_huf(conteudo_bytes)
            texto_descomprimido = descomprimir(bits, tabela_codigos)

            st.header("Texto Descomprimido")
            st.text_area("Resultado:", texto_descomprimido, height=300)
            st.success("Descompressão concluída!")


if __name__ == "__main__":
    main()

import graphviz


def visualizar_arvore(raiz):
    dot = graphviz.Digraph(comment='Huffman Tree', graph_attr={'rankdir': 'TB'})

    def adicionar_nos(no):
        if no is not None:
            node_id = str(id(no))
            label = f"'{no.char}':{no.freq}" if no.char is not None else str(no.freq)
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

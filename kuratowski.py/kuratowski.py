import networkx as nx

def is_subdivision_of_k5_or_k33(G):
    def is_subdivision_of_k5(H):
        return nx.is_isomorphic(H, nx.complete_graph(5))

    def is_subdivision_of_k33(H):
        return nx.is_isomorphic(H, nx.complete_bipartite_graph(3, 3))

    def check_subgraphs(G, check_function):
        for component in nx.connected_components(G):
            subgraph = G.subgraph(component)
            if check_function(subgraph):
                return True
        return False

    for component in nx.connected_components(G):
        subgraph = G.subgraph(component)
        if is_subdivision_of_k5(subgraph) or is_subdivision_of_k33(subgraph):
            return True
    return False

def check_planarity_kuratowski(G):
    # Check if the graph contains a subdivision of K5 or K33
    if is_subdivision_of_k5_or_k33(G):
        return False
    else:
        return True

# Exemplo de uso
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3), (1, 4)])

is_planar = check_planarity_kuratowski(G)
print("O grafo é planar?", is_planar)
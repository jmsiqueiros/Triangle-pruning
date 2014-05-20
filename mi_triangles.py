import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pprint



G = nx.Graph()

G.add_edges_from([(1,2,{'w': 20}),
                  (2,3,{'w': 21}),
                  (3,1,{'w': 33}),
                  (3,4,{'w': 10}),
                  (4,5,{'w': 11}),
                  (5,3,{'w': 2}),
                  (5,1,{'w': 2}),
                  (5,2,{'w': 22}),
              ])



def get_triangles_nodes(G):
    # detect triangles
    triangles_e = get_triangles_edges(G)

    triangles_n = []
    for t in triangles_e:
        # extract all nodes from all triangles
        all_nodes = []
        for e in t:
            all_nodes.append(e[0])
            all_nodes.append(e[1])
        # remove duplicates to end up with 3
        triangles_n.append(tuple(set(all_nodes)))

    return triangles_n


def get_triangles_edges(G):
    # detect triangles
    triangles_e = []
    for trio in itertools.combinations(G.nodes(), 3):
        edges = []
        for e in itertools.combinations(trio, 2):
            edge = G.get_edge_data(*e)
            if edge:
                edges.append(e)

        if len(edges)==3:
            triangles_e.append(edges)

    return triangles_e


def choose_weak_triangle(triangles):
    weights = {}
    for t in triangles:
        # discard triangles with all same weights
        if len(set([G.get_edge_data(*edge)['w'] for edge in t])) != 1:
            weights[tuple(t)] = min([G.get_edge_data(*edge)['w'] for edge in t])

    # return the triangle that contains smallest edge
    if weights:
        return [key for key, value in sorted(weights.iteritems(), key=lambda(k,v): (v,k))][0]
    else:
        return None





def prune(G):
    weak =  choose_weak_triangle(get_triangles_edges(G))
    while weak:
        pprint.pprint(get_triangles_edges(G))
        edges = {}
        for edge in weak:
            edges[tuple(edge)] = G.get_edge_data(*edge)['w']
                
        weak_edge = [key for key, value in sorted(edges.iteritems(), key=lambda(k,v): (v,k))][0]
        G.remove_edge(*weak_edge)
        weak =  choose_weak_triangle(get_triangles_edges(G))



fig = plt.figure()
fig.subplots_adjust(left=0.2, wspace=0.6)
pos = nx.circular_layout(G)


graph1 = fig.add_subplot(121)
graph1.plot(nx.draw(G,
        pos=pos,
        node_size  = [G.degree(n) for n in G.nodes()],
        width      = [G.get_edge_data(*e)['w'] for e in G.edges()],
        edge_color = [G.get_edge_data(*e)['w'] for e in G.edges()] ))

prune(G)

graph2 = fig.add_subplot(122)
graph2.plot(nx.draw(G,
        pos=pos,
        node_size  = [G.degree(n) for n in G.nodes()],
        width      = [G.get_edge_data(*e)['w'] for e in G.edges()],
        edge_color = [G.get_edge_data(*e)['w'] for e in G.edges()] ))
plt.show()


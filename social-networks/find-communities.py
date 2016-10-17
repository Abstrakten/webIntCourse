import networkx as nx
from numpy.linalg import eig
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 

color_map = {
        0:'y',
        1:'r',
        2:'b',
        3:'k',
        4:'m',
        5:'c',
        6:'g',
        7:'yellow',
        8:'brown',
            } 

# Laplacian method
def find_communities(G):
    L = nx.laplacian_matrix(G).todense()
    eig_values, eig_matrix = eig(L)
    
    # find second minimum in eigen values
    second_min_idx, second_min = sorted(enumerate(eig_values), key=lambda x: x[1])[1]

    print(second_min)
    print(second_min_idx)

    # find the correct coloumn
    target_coloumn = eig_matrix.transpose()[second_min_idx].transpose()
    for x in target_coloumn:
        x = x.real
    print(target_coloumn.shape)
    
    # pair graph node with eigen vector value
    paired_target_coloumn = zip(G.nodes(), target_coloumn)
    # for x,y in (paired_target_coloumn):
    #     print(x, y)


    k = 4
    # cluster using knn
    km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)

    km.fit(target_coloumn)

    
    communities = {}
    for node, cluster in zip(G.nodes(), km.labels_):
        #print(color_map[cluster])
        G.node[node]['cluster'] = cluster
        lst = communities.get(cluster, [])
        lst.append(node)
        communities[cluster] = lst
        #print(cluster)

    return communities


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

with open("friendships.txt") as inFile:
    lines = inFile.read().split("\n")

    data_rows = [x for x in chunks(lines, 5)]
    
    # populate graph
    G = nx.Graph()

    for row in data_rows:
        name = row[0].split()[1]
        friends = row[1].split("\t")[1:]
        # summary
        # review

        for friend in friends:
            G.add_edge(name, friend)

    communities = find_communities(G)
    print(communities)
    nx.draw_spring(G, node_color=[color_map[G.node[node]['cluster']] for node in G])
    plt.show()
    

import json
import networkx as nx
from networkx.readwrite import json_graph
import http_server
import random

def SEN_dense_gnm_random_graph(n1,m1,n2,m2,n3,m3,pa,pb):
    """Creates a SEN model with an actor network of n1 elements, with a neighbourhood connectivity of p1, a user network of n2 elements, with a neighbourhood connectivity of p2, and a ecological network of n3 elements with a neighbourhood connectivity of p3. The probability of connections between the actor network and the user netwrok, and between the user network and the ecological network, are respectively passed through pa and pb"""

    # Actor network
    A = nx.dense_gnm_random_graph(n1, m1)
    A.graph['Network']='Actors'
    # Adding id
    for i in range(len(A)):
        A.node[i]['num'] = i+1
    # Subnetwork
    for i in range(len(A)):
        A.node[i]['subnetwork'] = 1
    # Adding random class (office dwellers/field people)
    p_class_bureau = 0.75
    for i in range(len(A)):
        if random.random() <= p_class_bureau:
            A.node[i]['group'] = 0
        else:
            A.node[i]['group'] = 0
    # Adding randow weight
#    for n,nbrs in A.adjacency_iter():
#        for nbr,eattr in nbrs.items():
#            A[n][nbr]['weight'] = int(random.random()*8)


    # User network
    U = nx.dense_gnm_random_graph(n2, m2)
    U.graph['Network']='Actors'
    # Adding id
    for i in range(len(U)):
        U.node[i]['num'] = i+1001
    # Subnetwork
    for i in range(len(U)):
        U.node[i]['subnetwork'] = 2
    # Adding random class (office dwellers/field people)
    for i in range(len(U)):
        rnd=random.random()
        if rnd <= .2:
            U.node[i]['group'] = 1
        if rnd > .2 and rnd <= .4:
            U.node[i]['group'] = 1
        if rnd > .4 and rnd <= .6:
            U.node[i]['group'] = 1
        if rnd > .6 and rnd <= .8:
            U.node[i]['group'] = 1
        if rnd > .8:
            U.node[i]['group'] = 1
    # Adding randow weight
#    for n,nbrs in U.adjacency_iter():
#        for nbr,eattr in nbrs.items():
#            U[n][nbr]['weight'] = int(random.random()*8)

    # Ecological network
    E = nx.dense_gnm_random_graph(n3, m3)
    E.graph['Network']='Actors'
    # Adding id
    for i in range(len(E)):
        E.node[i]['num'] = i+10001
    # Subnetwork
    for i in range(len(E)):
        E.node[i]['subnetwork'] = 3
    # Adding class
    for i in range(len(E)):
            E.node[i]['group'] = 2
    # Adding weight
#    for n,nbrs in E.adjacency_iter():
#        for nbr,eattr in nbrs.items():
#            E[n][nbr]['weight'] = 5

    # joint the three subnetworks
    G = nx.disjoint_union_all([A,U,E])

    # link some actors to some users
    for i in range(0, len(G)):
        for j in range(0, len(G)):
            if i != j:
                if G.node[i]['subnetwork'] == 1 and G.node[j]['subnetwork'] == 2:
                    #if G.node[i]['group'] == 1 and G.node[j]['group'] == 2:
                    if random.random() < pa:
                        G.add_edge(i,j)

    # link some users to some patches
    for i in range(0, len(G)):
        G.node[i]['degreeold'] = G.degree(i)

    for i in range(0, len(G)):
        for j in range(0, len(G)):
            if i != j:
                #print str(j) + " " + str(G.degree(j))
                if G.node[i]['subnetwork'] == 2 and G.node[j]['subnetwork'] == 3 and G.degree(j) - G.node[j]['degreeold'] < 4:
                    if G.degree(j) - G.node[j]['degreeold'] < 4:
                        if random.random() < pb:
                            G.add_edge(i,j)
                            
    #remove lone nodes
    for i in range(0, len(G)):
        if G.degree(i) == 0:
            G.remove_node(i)
        

    # write json formatted data
    d = json_graph.node_link_data(G)
    json.dump(d, open('/Users/Rodolphe/Dropbox/Public/d3/examples/force/force.json','w'))

    nx.write_graphml(G, "graph.graphml")
    
    return G

G=SEN_dense_gnm_random_graph(50,100,5,3,100,100,.01,.02)
#print nx.average_degree_connectivity(G)
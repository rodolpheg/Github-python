# Mesurer les consequences, en terme de resilience dans les trois sous-reseaux, du retrait progressif des acteurs.

import csv
import networkx as nx
import matplotlib.pyplot as plt
import random
import SEN_dense_gnm_random_graph, savegraph, sen
import numpy

na = 50 # nombre d'acteurs
nu = 50 # nombre d'utilisateurs
nb = 50 # nombre de bosquets

prob = 1

x = []
y = []
z = []

results = []
apl = []

for l in range(100):

    G=SEN_dense_gnm_random_graph.SEN_dense_gnm_random_graph(na,100+l,nu,100,nb,100,.01,.01)


    d = 0
    dep = 0



    for i in range(na):
        
        print "l=" + str(l) + ", i=" + str(i)
        
    #    Mesurer le compromis connectivite/modularite dans le sous-reseaux des acteurs
        

    #    longueur moyenne des chemins entre les acteurs et les bosquets
        for j in range(dep, len(G)-1):
            for k in range(dep, len(G)-1):
                if j != k:
                    #print str(j) + "-" + str(k)
                    
                    try:
                        if G.node[j]['subnetwork'] == 1 and G.node[k]['subnetwork'] == 3:
                            if nx.has_path(G, j, k) == True:
                                p = nx.shortest_path_length(G, j, k)
                                apl.append(p)
                        break
                    except KeyError:
                        print "Probleme " + str(prob)
                        prob += 1
                    
#                    if G.node[j]['subnetwork'] == 1 and G.node[k]['subnetwork'] == 3:
#                        if nx.has_path(G, j, k) == True:
#                            p = nx.shortest_path_length(G, j, k)
#                            apl.append(p)

        results.append([numpy.mean(apl)])
        x.append([i])
        z.append([numpy.mean(apl)])



    #    Ces acteurs sont-ils importants dans le reseaux des acteurs ? (eigenvalue)
        
    #    Enfin, les habitats importants sont-ils connectes a des acteurs importants ?

        #results.append([G.number_of_nodes(),G.number_of_edges()])
        
    #    Retirer un noeud
        G.remove_node(dep)
        dep += 1

    y.append(l)

print results
        
with open('Results.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(results)

plt.plot(results)
plt.ylabel('average path')
plt.show()

fig = plt.figure(2)
ax = fig.gca(projection='3d')

ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
import networkx as nx
import numpy as np
import json
from typing import Dict
import matplotlib.pyplot as plt
from collections import Counter


def nakljucni_MIS(G, P):
    I = []            #Nastajajoca neodvisna mnozica
    V = list(G.nodes)
    for i in V:        # V tej mnozici izberemo vozlisca, ki jih dodamo neodvisni mnozici. P je permutacija naravnih stevil do vkljucno len(V). Vozlisce dodamo I, ce ima najmanjso vrednost med sosedi.,tako tudi preprecimo ponavljanje vozlisc v mnozici.
        A = []      
        A.append(P[i])
        if list(G.neighbors(i)) != []:
            for j in list(G.neighbors(i)):
                A.append(P[j])
        if P[i] == min(A):
            I.append(i)
    N = [] 
    for i in I:
        N += G.neighbors(i)
    V1 = I + N
    V1 = list(dict.fromkeys(V1)) # V1 je mnozica, ki jo bomo odstranili iz grafa in je sestavljena iz vozlisc iz I, ter njihovih sosedov
    if I == []:
        return []
    else:
        G1 = G.copy()
        G1.remove_nodes_from(V1)
        return list(I + nakljucni_MIS(G1, P))

def tightness(graf, mnozica, v): #Dolocimo "tightness" vozlisca v, v mnozici X, tj. za vsakega soseda vozlisca v, v mnozici graf\X, tightness(v) povecamo za 1
    t = 0
    for w in graf.neighbors(v):
        if w in mnozica:
            t += 1
        else:
            pass
    return t

def lokalno_iskanje(G, I): #Parametra graf v networkx formatu, neodvisna množica I (gre za Python list)
    V = list(G.nodes)
    for v in I:
        L = [] #Gradimo mnozice potencialnih kandidatov za dodajanje v neodvisno mnozico
        for w in G.neighbors(v):
            if G.neighbors(v) != []:
                if tightness(G, I, w) == 1:
                    L.append(w)
                else:
                    pass
            else:
                pass
        if len(L) >= 2:
            for v1 in L:
                for w1 in L:
                    if w1 not in G.neighbors(v1):
                        I.remove(v)
                        I_lokalno = I + [v1, w1]
                        return lokalno_iskanje(G, I_lokalno)
        else:
            return I 

def lokalno_iskanje1(G, I): #Parametra graf v networkx formatu, neodvisna množica I (gre za Python list)
    V = list(G.nodes)
    for v in I:
        L = [] #Gradimo mnozice potencialnih kandidatov za dodajanje v neodvisno mnozico
        for w in G.neighbors(v):
            if G.neighbors(v) != []:
                if tightness(G, I, w) == 1:
                    L.append(w)
                else:
                    pass
            else:
                pass
        while len(L) >= 2:
            for v1 in L:
                L.remove(v1)
                for w1 in L:
                    if w1 not in G.neighbors(v1):
                        I.remove(v)
                        I = I + [v1, w1]
                        break
                    elif w1 in G.neighbors(v1):
                        pass
                if w1 not in G.neighbors(v1):
                    break
            if w1 not in G.neighbors(v1):
                break
    return I
        
                    
                        


def erdos_renyi(n,p,m):
    A = []
    for i in range(m):
        G = nx.erdos_renyi_graph(n,p)
        G_slovar = nx.to_dict_of_lists(G)
        A += [G_slovar]
    return A






#-----------------------------------------


#A = []
#for i in range(1000):
#    P = list(np.random.permutation(len(H.nodes)))
#    I = nakljucni_MIS(H, P)
#    I_1 = lokalno_iskanje(H, I )
#    A.append(len(I_1) - len(I))
#print(A)
#print(len(A))


A = []
B = []
C = []
D = []
grafi=erdos_renyi(50,0.3,100)
for dict in grafi:
    graf = nx.from_dict_of_lists(dict)
    P = list(np.random.permutation(len(graf.nodes)))
    I = nakljucni_MIS(graf, P)
    I_1 = lokalno_iskanje(graf, I)
    I_2 = lokalno_iskanje1(graf, I)
    A.append(len(I_1) - len(I))
    B.append(len(I_2) - len(I))
    C.append(I_2)
    D.append(I_1)

print(B)

for i in C:    
    print(Counter(i))
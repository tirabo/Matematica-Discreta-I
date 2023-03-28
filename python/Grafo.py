# Clase Grafo
# Por cuestiones de  eficiencia un grafo se define con una lista de adyacencia G =[a0,a1,...] (los ai son listas)
#  1) los vertices son 0,1,...,len(G)-1
#  2) ai lista de vertices adyacentes a i.
#  3) j in ai sii i in aj
#  4) ai no tiene elementos repetidos (0 <= i <= len(G)-1).
# Una definición más formal de la clase Grafo se encuentra en AyP

class Grafo: 
    def __init__(self, list_ady = []):
        # pre: list_ady =[a0,a1,...,ak] (los ai son listas)
        #       1) los vertices son 0,1,..., k = len(list_ady) -1
        #       2) ai lista de vertices adyacentes a i (un elemento j in ai cumple j != i y 0 <= j <= k).

        assert type(list_ady) == list , 'el argumento debe ser una lista.'
        assert all(type(x) == list for x in list_ady) and all(all(0 <= j < len(list_ady) for j in x) for x in list_ady), 'el argumento debe ser una lista de listas'

        self.__lst_ady = []
        for i in range(len(list_ady)): # elimina duplicados
            self.__lst_ady.append(list(set(list_ady[i])))
            if i in self.__lst_ady[i]: # elimina i de la lista de adyacencia de i
                self.__lst_ady[i].remove(i)
        
        for i in range(len(self.__lst_ady)): # hace que  j in ai sii i in aj
            for j in self.__lst_ady[i]:
                if i not in self.__lst_ady[j]:
                    self.__lst_ady[j].append(i)
            self.__lst_ady[i].sort()
    
    def vertices(self):
        # post:  devuelve la lista de vértices del grafo
        return [i for i in range(len(self.__lst_ady))]
    
    def aristas(self):
        # post:  devuelve la lista de aristas del grafo. Cada arista es una 2-lista
        aristas_set = set()
        for i in range(len(self.__lst_ady)):
            for j in self.__lst_ady[i]:
                if i < j:
                    aristas_set.add((i,j))
        return [list(a) for  a  in aristas_set]

    def __str__(self):
        return str((self.vertices(), self.aristas())) # imprime el conjunto de vértices y el conjunto de aristas del grafo
    
    def adyacentes(self, vertice): 
        # pre: vertice es un vértice del grafo
        # post: devuelve el conjunto de vertices adyacentes a vertice
        return self.__lst_ady[vertice]
    
    def agregar_vertice(self, new_vert):
        # post: agrega un vértice, si el vértice ya estaba no cambia nada
        self.__lst_ady.append([]) # aumento en 1 la cantidad de vértices (pasa a ser el ultimo vértice)
    
    def quitar_arista(self, e):
        # post: quita arista {x, y} (si está). En  caso contrario no hace nada.
        # pre: e == (x, y) arista
        assert type(e) == list and len(e) == 2, 'el argumento debe ser una 2-lista' 
        if e[0] in self.__lst_ady[e[1]]:
            self.__lst_ady[e[1]].remove(e[0])
            self.__lst_ady[e[0]].remove(e[1])
    
    def agregar_arista(self, e):
        # pre: e == [x, y] 
        # post: si x, y son vértices del grafo, agrega arista e = [x, y] (si no está).
        #       En  caso contrario no hace nada.
        assert type(e) == list and len(e) == 2 and e[0] != e[1], 'el argumento debe ser una 2-lista de dos elementos distintos'  
        if e[0] not in self.__lst_ady[e[1]]:
            self.__lst_ady[e[1]].append(e[0]).sort()
            self.__lst_ady[e[0]].append(e[1]).sort()
    
    def copiar(self):
        # post: devuelve una copia del grafo
        return Grafo(self.__lst_ady)


"""
    INICIO: Algoritmo de Hierholzer
"""

def recorrido_max(L, v_ini): 
    # pre: L grafo, v_ini vértice de L
    # post: devuelve un recorrido maximal que comienza en v_ini
    # mod: se quitan de L las aristas utilizadas
    sub_caminata = [v_ini]  # sub caminata
    p0 = v_ini
    while len(L.adyacentes(p0)) > 0:  
        p1 = L.adyacentes(p0)[0] # p1 primer adyacente a p0 
        sub_caminata.append(p1) # agrega p1 a caminata
        L.quitar_arista([p0,p1]) # quita arista {p0, p1}
        p0 = p1 
    return sub_caminata


def caminata_circuito_euleriano(G):
    # pre: G grafo con todos los vértices de valencia par o dos impares
    # post: cuando termina 'caminata' es una lista de vértices que es
    #       una caminata o circuito euleriano.
    Libres = G.copiar() # sub grafo de aristas no utilizadas
    vertices = Libres.vertices()
    
    v_ini = vertices[0]
    i, lon  = 0, len(vertices)
    n_imp = 0 # cantidad vértices de valencia impar
    for vertice in vertices:
        if len(Libres.adyacentes(vertice)) % 2 == 1:
            v_ini = vertice
            n_imp += 1
    # v_ini es el primer vértice si son todos pares o el último vértice impar
    assert len(n_imp) == 2 or len(n_imp) == 0,'hay más de dos vértices de valencia impar'
    caminata = recorrido_max(Libres, v_ini) # recorrido maximal desde v = v_ini
    while len(Libres.aristas()) > 0:
        for vertice in caminata:
            if len(Libres.adyacentes(vertice)) > 0:
                v = vertice # v es un vértice de la caminata con aristas libres
        i = caminata.index(v) # el índice de v en la caminata
        caminata  =  caminata[:i] + recorrido_max(Libres, v) + caminata[i+1:]
        # intercala recorrido maximal en v, Libres queda con las
        # aristas no utilizadas en cam
    return caminata


"""
    FIN: Algoritmo de Hierholzer
"""


def main():
    # Grafos de prueba
    
    # Grafo 0 (el gran tour)
    # G0 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5)})
    # print(G0)
    # print(recorrido_euleriano_max(G0, 0))
    lista_ady_0= [[1,2,4,5],[0,2,4,5],[0,1,3,5],[2,4],[0,1,3,5],[0,1,2,4]]
    G0 = Grafo(lista_ady_0)
    print(caminata_circuito_euleriano(G0))
    # resultado : [0, 1, 2, 0, 4, 1, 5, 2, 3, 4, 5, 0]

    # Grafo 1
    # G1 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    #print(G1)
    #print(recorrido_euleriano_max(G1, 0),'\n')
    lista_ady_1 = [[3,4,5,6], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [0,5]]
    G1 = Grafo(lista_ady_1)
    print(caminata_circuito_euleriano(G1))
    # resultado : [0, 3, 4, 0, 5, 2, 1, 4, 5, 6, 0]

    # Grafo 2 (cíclico)
    # G2 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)})
    # print(G2)
    # print(recorrido_euleriano_max(G2, 0),'\n')
    #lista_ady [[1,5],[0, 2],[1,3],[2,4],[3,5],[4,0]]

    # Grafo 3 
    # G3 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 2), (0, 4), (0, 5), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)})
    # print(G3)
    # print(recorrido_euleriano_max(G3, 0))
    # print(recorrido_euleriano_max(G3, 1),'\n')
    lista_ady_3 = [[2, 4, 5], [3, 5], [0, 3, 4, 5], [1, 2, 4], [0, 2, 3, 5], [0, 1, 2, 4]]
    G3 = Grafo(lista_ady_3)
    print(caminata_circuito_euleriano(G3))
    # resultado : [3, 1, 5, 0, 2, 3, 4, 2, 5, 4, 0]

    # Grafo 4
    # G4 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    # print(recorrido_euleriano_max(G4, 0))
    #lista_ady [[3,4,5], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [5]]
    
    # Grafo 6 (dos valencias impares)
    # G6 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
    #print(G6)
    #print(caminata_euleriana(G6, 0))

    # Grafo 7 (todas valencias pares)
    # G7 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (0, 11), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
    # print(G7)
    #print(recorrido_euleriano_max(G7,0))
    # G7.agregar_vertice()
    # print(G7)
    # G7.agregar_arista([12, 0])
    # print(G7)
    # print(caminata_euleriana(G7, 0))
    # print(isinstance(G7, Grafo)  )

    #print(coloracion_vertices(G1))
    #print(coloracion_vertices(G7))



    # Pesos en G1
    # pesos_G1 =  {(0, 3):5, (0, 4):0, (0, 5):0, (0, 6):0, (1, 2):10, (1, 4):0, (2, 5):0, (3, 4):0, (4, 5):0, (5, 6):0}

    # print(kruskal(G1, pesos_G1))
    # print(prim(G1, pesos_G1))


    return 0
# RUN

if __name__ == '__main__':
    main()

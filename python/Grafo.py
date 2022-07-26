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
        return [i for i in range(self.__lst_ady)]
    
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

def circuito_euleriano(G, v = 0): #Algoritmo de Hierholzer
    # pre: G grafo con todos los vértices de valencia par, v vértice.
    #      Si no se ingresa v toma el valor 0
    # post: devuelve 'circuito' una lista de vertices que forma un circuito
    #       euleriano. El  circuito empieza en 0.
    circuito = [v]  # inicio de la caminata
    libres = copiar_grafo(G) # aristas no utilizadas
    while  nro_aristas(libres) > 0:
        sub_cam = []   
        h = 0
        while libres[h] == [] or h not in circuito:
            h = h + 1
        # h = vértice en circuito donde libre[h] != [] (hay aristas libres)
        pos = circuito.index(h) # posición de la 1º ocurrencia de h
        p0 = h
        p1 = libres[h][0] 
        while p1 != h: # mientras no se vuelva al origen
            sub_cam.append(p1)  # agrega p1 a sub_cam 
            libres[p0].remove(p1)
            libres[p1].remove(p0) # quitar arista p0, p1 
            p0 = p1 
            p1 = libres[p0][0]
        libres[p0].remove(h)
        libres[h].remove(p0) # quitar arista p0, p1 
        # print( circuito[: pos +1], sub_cam, circuito[pos :]) 
        circuito = circuito[: pos + 1] +  sub_cam + circuito[pos :]
        # print('Circuito:',circuito) 
        # print('Libres;',libres)
    return circuito   

# print(circuito_euleriano(G,3))

    
def caminata_euleriana_desde_a(G, v, w): 
    # pre: graph grafo donde v y w son vértices impares y todos demás pares
    # post: devuelve  la lista de vertices de la caminata euleriana
    #       La caminata empieza en v y termmina en w.
    caminata = []
    H = copiar_grafo(G) # hace una copia de G
    if w in G[v]: # si [v,w] es arista en G
        quitar_arista(H, [v, w]) # quita la arista [v, w]
        cmnt = circuito_euleriano(H, v)
        caminata = cmnt.append(w)
    else: # si [v,w] no es arista en G
        agregar_arista(H, [v, w]) # agrega la arista [v, w]
        cmnt = circuito_euleriano(H, w)
        k = -1
        for i in range(1,len(cmnt)):
            if cmnt[i - 1] == w and cmnt[i] == v:
                k = i
            if k > 0:
                caminata.append(cmnt[i])
        for i in range(1,k):
            caminata.append(cmnt[i])
    return caminata

def caminata_euleriana(G): 
    # pre: G grafo.
    # post: devuelve un par. La primera coordenada es True si hay camina euleriana y False en otro caso.
    #       La segunda coordenada es [] si no hay c e y es la lista de vertices de la caminata si existe  c e
    #       La caminata empieza desde un vertice arbitrario (0 en el caso par).
    existe, caminata = False, []
    impares = []
    for i in range(len(G)):
        if len(G[i]) % 2 == 1: # si la valencia es impar
            impares.append(i)
    if len(impares) == 0: # todas las valencias pares
        existe = True
        caminata = circuito_euleriano(G)
    elif len(impares) == 2: # dos valencias impares
        existe = True
        vini, vfin = impares[0], impares[1]
        caminata = caminata_euleriana_desde_a(G, vini, vfin)
    return existe, caminata

# print(caminata_euleriana(G))

"""
    FIN: Algoritmo de Hierholzer
"""


def main():
    # Grafos de prueba
    
    # Grafo 0 (el gran tour)
    G0 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5)})
    # print(G0)
    # print(recorrido_euleriano_max(G0, 0))
    # lista ady= [[1,2,4,5],[0,2,4,5],[0,1,3,5],[2,4],[0,1,3,5],[0,1,2,4]]

    # Grafo 1
    G1 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    #print(G1)
    #print(recorrido_euleriano_max(G1, 0),'\n')
    #lista_ady [[3,4,5,6], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [0,5]]

    # Grafo 2 (cíclico)
    G2 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)})
    # print(G2)
    # print(recorrido_euleriano_max(G2, 0),'\n')
    #lista_ady [[1,5],[0, 2],[1,3],[2,4],[3,5],[4,0]]

    # Grafo 3 
    G3 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 2), (0, 4), (0, 5), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)})
    # print(G3)
    # print(recorrido_euleriano_max(G3, 0))
    # print(recorrido_euleriano_max(G3, 1),'\n')
    #lista_ady [[2, 4, 5], [3, 5], [0, 3, 4, 5], [1, 2, 4], [0, 2, 3, 5], [0, 1, 2, 4]]

    # Grafo 4
    G4 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    # print(recorrido_euleriano_max(G4, 0))
    #lista_ady [[3,4,5], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [5]]
    
    # Grafo 6 (dos valencias impares)
    G6 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
    #print(G6)
    #print(caminata_euleriana(G6, 0))

    # Grafo 7 (todas valencias pares)
    G7 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (0, 11), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
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
    pesos_G1 =  {(0, 3):5, (0, 4):0, (0, 5):0, (0, 6):0, (1, 2):10, (1, 4):0, (2, 5):0, (3, 4):0, (4, 5):0, (5, 6):0}

    print(kruskal(G1, pesos_G1))
    print(prim(G1, pesos_G1))


    return 0
# RUN

if __name__ == '__main__':
    main()

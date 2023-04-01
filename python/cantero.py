from itertools import product


"""
EL PROBLEMA ORIGINAL ES EL SIGUIENTE:
Plantines en los canteros circulares
Se está arreglando la plaza principal de la ciudad. Leandro, el jardinero, ha calculado que para bordear cada uno de los canteros circulares necesita 6 plantines. Él dispone de 4 clases de plantines y quiere colocarlos de manera que no haya dos plantines de la misma clase en forma consecutiva.
¿De cuántas maneras puede bordear los plantines los canteros circulares? 

"""

"""
Se colocan 6 plantines en un cantero circular
1) Hay 4 clases de plantines (0, 1, 2, 3)
2) No puede haber 2 plantines consecutivos de la misma clase
¿De cuantas formas se puede hacer? (las rotaciones son equivalentes)

o,  equivalentemente,

Se quieren pintar los vértices de un polígono de 6 lados con 4 colores sin que haya dos vértices consecutivos pintados del mismo color.
¿De cuántas formas se puede hacer?
Dos casos:
1) las rotaciones no son equivalentes;
2) las rotaciones son equivalentes. 
Solución (fuerza bruta): 1) 732; 2) 130. 
"""



def pintar_poligono_fb(ver = 6, col = 4):
    # ver : entero >=2 
    # col : cantidad de colores >= 2
    # post: devuelve la cantidad de formas de pintar los vértices de un polígono de ver lados con col colores sin que haya dos vértices consecutivos pintados del mismo color. El par que devuelve es en la primera coordenada sin equivalencia de rotaciones y la segunda con equivalencia con rotaciones.
    # solución fuerza bruta: se calculan todas las posibilidades y se eliminan las que no sirven 
    cls = list(range(col))
    cls_repetidos = [cls]*ver
    plt1 = list(product(*cls_repetidos))
    r0 = [list(w) for w in plt1]
    # r0 son todos los coloreos posibles, sin restricciones, sin equivalencia de rotaciones (es cls**n)
    r1 = []
    for u in r0:
        sirve = True
        for i in range(ver - 1):
            if u[i] == u[i + 1]:
                sirve = False
        if u[ver - 1] == u[0]:
            sirve = False
        if sirve:
            r1.append(u)
    # r1 son todos los coloreos posibles donde no puede haber dos colores iguales contiguos.
    # No hay equivalencia por rotaciones
    r2 = []
    raux = []
    for u in r1:
        sirve = True
        if u in raux:
            sirve = False
        else:
            for i in range(ver):  # agrega todas las rotaciones de u a raux
                raux.append(u[i:] + u[:i])
        if sirve:
            r2.append(u)
    # r2 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
    return len(r1), len(r2)


# A partir de aquí como se resuelve 1). 


def pintar_linea_rec(ver, i, col):
    # pre: ver cantidad de puntos de la linea >= 2, col cantidad de colores, 0 <= i < col
    # post:  devuelve la cantidad de formas de pintar la linea de ver puntos con 
    #       col colores tal que:
    #       1) comienza con color 0
    #       2) no hay dos puntos consecutivos pintados del mismo color
    #       3) termina en el color i

    # Se  hará recursión sobre n >= 2
    ret = 0
    if ver == 2:
        if i == 0:
            ret = 0
        else:
            ret = 1
    else:
        if i == 0:
            ret = (col - 1) * pintar_linea_rec(ver - 1, 1, col)
        else:
            ret = pintar_linea_rec(ver - 1, 0, col) + (col - 2) * pintar_linea_rec(ver - 1, 1, col)
    return ret


def pintar_linea_pd(ver, i, col):
    # pre: col cantidad de colores, ver cantidad de puntos de la linea >= 2, 0 <= i < c
    # post:  devuelve la cantidad de formas de pintar la linea de n puntos con 
    #       col colores tal que: 
    #       1) comienza con color 0
    #       2) no hay dos puntos consecutivos pintados del mismo color
    #       3) termina en el color i

    # Se hace con programación dinámica (o funciones con memoria)
    ret = 0
    
    # Primera forma: ocupa más espacio pero es más fácil de entender
    # matriz = [[0, 0]] * ver
    # matriz[1] = [0, 1]
    # for k in range(2, ver):
    #     matriz[k] = [(col -1) * matriz[k - 1][1], matriz[k - 1][0] + (col -2) * matriz[k - 1][1]]
    # if i == 0:
    #     ret = matriz[ver - 1][0]
    # else:
    #     ret = matriz[ver - 1][1]
    # return ret
    
    # Segunda forma: mínimo espacio, mínimo procesamiento
    mpd = [[0, 1], [0,0]] 
    for k in range(2, ver):
        mpd[1] = [(col -1) * mpd[0][1], mpd[0][0] + (col - 2) * mpd[0][1]]
        mpd[0] = mpd[1]
    if i == 0:
        ret = mpd[1][0]
    else:
        ret = mpd[1][1]
    return ret


def pintar_poligono_rec(ver = 6, col = 4):
    # ver : cantidad de plantines en el cantero
    # col : cantidad de clases de plantines
    # solución recursiva: se calcula la cantidad de formas de pintar una linea 
    #     de ver + 1  puntos con col colores tal que comienza  y  termina en 0 
    #     y no hay dos puntos consecutivos pintados del mismo color,
    ret = pintar_linea_rec(ver + 1, 0, col) # recursivo
    # Identificando el primer y último vértice se resuelve el problema de los n plantines cuando el primer vértice es 0. 
    # 
    # Hay que multiplicar por la cantidad de colores para no tener restricciones en el primer vértice.
    return ret * col

def pintar_poligono_pd(ver = 6, col = 4):
    # ver : cantidad de plantines en el cantero
    # col : cantidad de clases de plantines
    ret = pintar_linea_pd(ver + 1, 0, col) # programación dinámica
    # Identificando el primer y último vértice se resuelve el problema de los polígonos de ver lados cuando el primer vértice es 0. 
    # 
    # Hay que multiplicar por la cantidad de colores para no tener restricciones en el primer vértice.
    return ret * col


def pintar_linea_casos(ver, i, col):
    # pre: col cantidad de colores >= 2, ver cantidad de puntos de la linea >= 2, 
    #       0 <= i < col
    # post:  devuelve las formas de pintar la linea de ver puntos con 
    #       col colores tal que: 
    #       1) comienza con color 0
    #       2) no hay dos puntos consecutivos pintados del mismo color
    #       3) termina en el color i
    #       Lo  que devuelve es una lista de listas, donde cada lista es una 
    #       forma de pintar la linea (cada lista empieza en 0 y termina en i)

    mpd, ret = [], []
    for j in range(1, col):  # todos los casos de longitud 2
        mpd.append ([0, j])

    for k in range(2, ver):
        aux_casos = []
        for caso in mpd:
            for c in range(col):
                if caso[-1] != c:
                    aux_casos.append(caso + [c])
        mpd = aux_casos
    # mpd ahora son todos los casos de longitud ver pueden terminar en caulquier vértice
    # hay que filtrar los que terminan en i
    for caso in mpd:
        if caso[-1] == i:
            ret.append(caso)
    return ret


def pintar_poligono_formas(ver = 6, col = 4):
    # pre: ver, col >= 2
    # post: devuelve todas las posibles formas de pintar un polígono de ver lados 
    #       con col colores sin que haya dos vértices consecutivos pintados 
    #       del mismo color.
    # 
    # solución recursiva: se calcula la cantidad de formas de pintar una linea 
    #     de ver + 1  puntos con col colores tal que comienza  y  termina en 0 
    #     y no hay dos puntos consecutivos pintados del mismo color,
    ret = pintar_linea_casos(ver + 1, 0, col) # programación dinámica
    # Identificando el primer y último vértice se resuelve el problema de los polígonos de ver lados cuando el primer vértice es 0. 
    # 
    # Hay que multiplicar por la cantidad de colores para no tener restricciones en el primer vértice.
    return ret * col

def main():
    ver, col = 6, 4
    print('Fuerza bruta. Vértices:', ver, 'colores:',col,'->',pintar_poligono_fb(ver, col))
    # Fuerza bruta no funciona para ver o col grandes, por ejemplo para ver, col = 10, 4 se demora varios minutos en calcular.

    ver, col = 20, 4
    print('Recursión. Vértices:', ver, 'colores:', col,'->' , pintar_poligono_rec(ver, col))
    # Recursión se demora mucho para números grandes. Por ejemplo para ver, col = 50, 4 se demora varios minutos en calcular.

    ver, col = 1000, 80
    print('Progamación dinámica. Vértices:', ver, 'colores:', col,'->' , pintar_poligono_pd(ver, col))
    # Programación dinámica funciona para ver o col grandes

    ver, col = 10, 4
    print('Formas. Vértices:', ver, 'colores:', col,'->' , len(pintar_poligono_formas(ver, col)))
    # Esto se complica para ver grandes (guarda en memoria todas las formas). Por ejemplo para ver, col = 20, 4 se demora varios minutos en calcular.


if __name__ == "__main__":
    main()




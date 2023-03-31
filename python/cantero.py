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
Solución (fuerza bruta): 1) 730; 2) 130. 
"""



def acomodar_plantines(cantero = 6, cls_plantines= 4):
    # cantero : cantidad de plantines en el cantero
    # cls_plantines : cantidad de clases de plantines
    # solución fuerza bruta: se calculan todas las posibilidades y se eliminan las que no sirven 
    cls = list(range(cls_plantines))
    cls_repetidos = [cls]*cantero
    plt1 = list(product(*cls_repetidos))
    r0 = [list(w) for w in plt1]
    # r0 son todos los canteros posibles, sin restricciones, sin equivalencia de rotaciones (es cls**cantero)
    r1 = []
    for u in r0:
        sirve = True
        for i in range(cantero - 1):
            if u[i] == u[i + 1]:
                sirve = False
        if u[cantero - 1] == u[0]:
            sirve = False
        if sirve:
            r1.append(u)
    # r1 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
    # No hay equivalencia por rotaciones
    r2 = []
    raux = []
    for u in r1:
        sirve = True
        if u in raux:
            sirve = False
        else:
            for i in range(cantero):  # agrega todas las rotaciones de u a raux
                x = []
                for j in range(cantero):
                    x.append(u[(i + j) % cantero])
                if x not in raux:
                    raux.append(x)
        if sirve:
            r2.append(u)
    # r2 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
    # Hay equivalencia por rotaciones
    # for u in r2:
    #     print u
    return len(r1), len(r2)

# cantero = 4
# for cls_plantines in range(1, cantero + 1 ):
#     print('vértices:', cantero, 'colores:',cls_plantines,acomodar_plantines(cantero, cls_plantines))


# A partir de aquí como se resuelve 1). 

def pintar_linea_rec(c, n, i):
    # pre: n cantidad de puntos de la linea >= 2, c cantidad de colores, 0 <= i < c
    # post:  devuelve la cantidad de formas de pintar la linea de n puntos con 
    #       c colores tal que:
    #       1) comienza con color 0
    #       2) no hay dos puntos consecutivos pintados del mismo color
    #       3) termina en el color i

    # Se  hará recursión sobre n >= 2
    ret = 0
    if n == 2:
        if i == 0:
            ret = 0
        else:
            ret = 1
    else:
        if i == 0:
            ret = 3 * pintar_linea(c, n - 1, 1)
        else:
            ret = pintar_linea(c, n - 1, 0) + 2 * pintar_linea(c, n - 1, 1)
    return ret

def pintar_linea_pd(c, n, i):
    # pre: n cantidad de puntos de la linea >= 2, c cantidad de colores, 0 <= i < c
    # post:  devuelve la cantidad de formas de pintar la linea de n puntos con 
    #       c colores tal que:
    #       1) comienza con color 0
    #       2) no hay dos puntos consecutivos pintados del mismo color
    #       3) termina en el color i

    # Se hace con programación dinámica (o funciones con memoria)
    ret = 0
    
    # Primera forma: ocupa más espacio pero es más fácil de entender
    # matriz = [[0, 0]] * n
    # matriz[1] = [0, 1]
    # for k in range(2, n):
    #     matriz[k] = [3 * matriz[k - 1][1], matriz[k - 1][0] + 2 * matriz[k - 1][1]]
    # if i == 0:
    #     ret = matriz[n - 1][0]
    # else:
    #     ret = matriz[n - 1][1]
    # return ret
    
    # Segunda forma: mínimo espacio, mínimo procesamiento
    mpd = [[0, 1], [0,0]] 
    for k in range(2, n):
        mpd[1] = [3 * mpd[0][1], mpd[0][0] + 2 * mpd[0][1]]
        mpd[0] = mpd[1]
    if i == 0:
        ret = mpd[1][0]
    else:
        ret = mpd[1][1]
    return ret


def acomodar_plantines_2(n = 6, c = 4):
    # n : cantidad de plantines en el cantero
    # c : cantidad de clases de plantines
    # solución recursiva: se calcula la cantidad de formas de pintar una linea 
    #     de n + 1  puntos con c colores tal que comienza  y  termina en 0 
    #     y no hay dos puntos consecutivos pintados del mismo color,
    # ret = pintar_linea_rec(c, n + 1, 0) # recursivo
    ret = pintar_linea_pd(c, n + 1, 0) # programación dinámica
    # Identificando el primer y último vértice se resuelve el problema de los n plantines cuando el primer vértice es 0. Ha que multiplicar por la cantidad de colores para no tener restricciones en el primer vértice.
    return ret * c


ver, col = 6, 4
print('vértices:', ver, 'colores:', col,'\n' ,acomodar_plantines(ver, col)[0])

ver, col = 6, 4
print('vértices:', ver, 'colores:', col,'\n' ,acomodar_plantines_2(ver, col))



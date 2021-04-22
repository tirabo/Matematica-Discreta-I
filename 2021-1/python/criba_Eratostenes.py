
# criba de Eratóstenes

def criba(n: int) -> list[int]:
    # pre: n > 0
    criba = [2]*(n+1) # lista de 2's de longitud n + 1 
    for i in range(1, n + 1, 2):
        criba[i] = i # en los lugares impares se pone criba[i] = i
    i = 3
    while i*i <= n : # se itera desde 3 a i <= sqrt(n)
        if criba[i] == i: # i es primo
            for j in range(i*i, n + 1, i): # j desde i^2 a sqrt(n) saltando de a i
                if criba[j] == j:
                    criba[j] = i # si j no es divisible por un primo < i, se pone i
        i = i + 1
    return criba # post:  criba[i] = menor factor primo de i (i >1)

def criba_primos(n: int) -> list[int]:
    # pre: n número natural
    # post: se obtiene ''primos'' la lista de números primos hasta n usando
    #       la criba de Eratóstenes
    primos = [] # lista vacía
    tachados = [] # lista de números tachados 
    for i in range(2, n+1):
        if i not in tachados:
            primos.append(i) # agregar i a primos
            k = 2
            while k * i <= n:
                tachados.append(k * i) # agrega k*i a tachados
                k = k + 1
    return primos

def primos_hasta(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve primos, una lista de primos  <= n
    criba_n = criba(n)
    primos = [2]
    for i in range(3, n + 1, 2):
        if criba_n[i] == i:
            primos.append(i)
    return primos

def desc_prima(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve descomposición prima de n como una lista de primos <= n
    primos = []
    k = n
    while k > 1:
        p = criba(k)[-1] # el menor primo que divide a k
        primos.append(p)
        k = k // p
    return primos

def criba_clasica(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve la lista de primos <= n usando el método de la criba de Eratóstenes
    primos = []
    todos = list(range(n+1))
    todos[0], todos[1] = 0, 0
    j = 2
    while  j <= n:
        if todos[j] != 0:
            primos.append(j)
            k = 1
            while j + j*k <= n:
                todos[j + j*k] = 0
                k = k + 1
        j = j + 1
    return primos




def main():
    # print(criba(25))
    # print(len(criba(10**8))) # esto ya toma mucho tiempo 
    # print(len(primos_hasta(102400)))
    # print(len(criba_primos(102400)))
    # print(desc_prima(1024))
    n = 997
    print(len(primos_hasta(n))) # Eficiente
    print(primos_hasta(n))
    # print(len(criba_primos(n))) # No eficiente
    print('')
    print(len(criba_clasica(n))) # Eficiente, consume memoria (arreglo de longitud n)
    print(criba_clasica(n))


if __name__ == "__main__":
    main()

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
    primos = []
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

print(criba(25))
# print(len(criba(10**8))) # esto ya toma mucho tiempo 
print(len(primos_hasta(1024000)))
print(len(criba_primos(1024000)))
# print(desc_prima(1024))


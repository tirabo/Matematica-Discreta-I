
# criba de Eratóstenes

def criba_w(n): # de Wikipedia. El mejor. 
    a = [True]*(n+1)
    for i in range(2, int(n**0.5) + 1):
        if a[i] == True:
            for j in range(i**2, n+1, i ):
                a[j] = False
    return [i for i in range(2,n+1) if a[i] == True]

def criba_primos(n: int) -> list[int]: # el algoritmo del apunte
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



def desc_prima(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve descomposición prima de n como una lista de primos <= n
    primos = []
    k = n
    while k > 1:
        p = criba_w(k)[-1] # el mayor primo que divide a k
        primos.append(p)
        k = k // p
    return primos






def main():
    # print(criba(25))
    # print(len(criba_w(10**8))) 
    # print(len(criba_w(102400)))
    # print(desc_prima(1024))
    n = 997
    print(len(criba_w(n))) # Eficiente
    print(criba_w(n))
    # print(len(criba_primos(n))) # No eficiente
    print('')
    print(len(criba_clasica(n))) # Eficiente, consume memoria (arreglo de longitud n)
    print(criba_clasica(n))


if __name__ == "__main__":
    main()
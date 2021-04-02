import math
import random 
# import sys

# sys.setrecursionlimit(10000)
# print('rec lim', sys.getrecursionlimit())

"""
## Método binario para exponenciacion modular

Ver: https://es.wikipedia.org/wiki/Exponenciaci%C3%B3n_modular

Sean `a, d, n` enteros positivos se desea calcular `a**d % n`
1.  Se calcula la expresión binaria de `d`. 
Si `d` en base 2 es `d_n...d_0`, entonces
        d = \sum_{i=0}^{n} d_i * 2**i
2. Entonces 
        a**d = \prod_{i=0}^{n} a**{d_i * 2**i} 
             = \prod_{i=0}^{n} (a**(2**i))**d_i.
3. Usando lo anterior `c = a**d % n` se calcula recursivamente:
        c = (a**(2**0))**d_0 % m        (caso base)
        c = c * (a**(2**i))**d_i % m    (paso i)
"""

def pot_mod(a: int, d: int, n: int) -> int:
    # pre: a, d >= 0, n > 0
    # post: devuelve a**d % n calculado por el método binario de exponenciacion modular
    assert a >= 0 and d >= 0 and n > 0, 'a, d o n no cumplen  la precondicion'
    em = 1
    cociente, resto = (d // 2), d % 2 
    # d = cociente * 2 + resto => a**d = (a**2)**cociente * a**resto
    a0 = a
    while cociente > 0:
        a0, em  = a0**2 % n, em * a0**resto % n
        resto =  cociente % 2
        cociente = cociente // 2
    em = em * a0**resto % n
    return em

"""
# Pruebas
print(pot_mod(2,4,15)) # 1
print(pot_mod(7, 385, 11)) # 10
print(pot_mod(5,1125899986842625, 100000037 )) # 98770120
"""
def pot_mod_recursivo(a: int, d: int, n: int) -> int:
    pot = 0
    if d == 0:
        pot = 1
    else:
        pot = (pot_mod_recursivo(a**2 % n, d // 2, n) * a**(d % 2) ) % n
    return pot

# print(pot_mod(7, 2, 11)) # 5
# print(pot_mod_recursivo(7, 2, 11)) # 5
# print(pot_mod(7, 385, 11)) # 10
# print(pot_mod_recursivo(7, 385, 11)) # 10
# # a = 5,  d = 25000009 , n =100000037
# print(pot_mod(5,25000009, 100000037 )) # 44612474
# print(pot_mod_recursivo(5,25000009, 100000037 )) # 44612474


def base2(n: int) -> str:
    # post: devuelve n en base 2 (como cadena)
    m, n2 =  n // 2, str(n % 2)
    while m > 0:
        m, n2 = m // 2, str(m % 2) + n2
    return n2



"""
Test  no deterministico  de primalidad de  Miller Rabin 

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#

Input: n > 1, es un entero impar el cual veremos si es probablemente primo.
Output: False si n is compuesto, True si n es probablemente primo

escribir  n - 1 = 2**s * d con mcd(2,d) = 1.

n es fuertemente probablemente primo si 
- `a**d  = 1 (mod n)`
o
- `a**(2**r * d) = -1 (mod n)` para algún r tal  que 0  <= r <= s.

"""

def pot2(n: int) -> tuple[int, int]:
    # pre: n > 0, n impar
    # post: devuelve s, d tal n = 2**s * d + 1,  con d impar.
    assert n > 0 and n % 2 == 1
    u, m = (n -1) % 2, (n - 1) // 2
    s = 0
    while u == 0:
        s = s + 1
        u, m = m % 2, m // 2
    d = (n -1) // 2**s
    return (s, d)


def fpp(n: int, a:int) -> bool:
    # pre: n >2, n impar, 0 < a < n
    assert n > 2 and n % 2 == 1 and 0 < a and a < n
    # post: devuelve True si n es FPP respecto a a. False en caso contrario
    
    # n = 2**s * d  + 1. Calculamos d y s 
    ret = False
    (s, d) = pot2(n)
    if 1 == pot_mod(a, d, n):
        ret = True
    else:
        r = 0
        while r  <= s and ret == False:
            if n - 1 == pot_mod(a, 2**r * d, n):
                ret = True
            r = r +1
    return ret


def test_Miller_Rabin(n: int, k: int) -> bool:
    # post: hace a n el test de  Miller-Rabin  k veces. 
    # Devuelve True si n es fuertemente probablemente primo (si pasa el test k veces)
    # Devuelve False si n no es fuertemente probablemente primo (y por lo tanto compuesto) 
    (s, d) = pot2(n)
    print('Verificando si  %d = 2**%d * %d + 1  es primo' % (n, s, d))
    for _ in range(k):
        a = random.randrange(2, n) # entero al azar entre 2 y n-1
        fpp = False # fuertemente primo en base a  
        if 1 == pot_mod(a, d, n):
            fpp = True
        else:
            r = 0
            while r  <= s and fpp == False:
                if n - 1 == pot_mod(a, 2**r * d, n):
                    fpp = True
                r = r +1
        if fpp == False: # si no pasa la prueba
            return False
    # si pasó las k pruebas
    return True


# Pruebas
# print(test_Miller_Rabin(221,100)) # False
# print(test_Miller_Rabin(351, 10)) # probablemente False
# print(test_Miller_Rabin(10**8+37, 5)) # True
# print(test_Miller_Rabin(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077, 100)) # True
# print(test_Miller_Rabin(323000000000023902000000000442187, 100)) # False (probablemente)


"""
Test deterministico  de primalidad de  Miller Rabin (asume la Hipotesis de Riemman)

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Miller_test

Input: ng > 1, es un entero impar el cual veremos si es primo.
Output: False si ng is compuesto, True si ng es primo

escribir  ng - 1 = 2**s * d con mcd(2,d) = 1.
for a in  range(1 ,min(ng - 1,2 * ln(ng)**2)):
   Si para todo r in [0,s - 1]  -> a**d \not \equiv 1 (mod ng) and a**(2**r * d)\not \equiv - 1 (mod ng)
         return False
return True
"""


def test_Miller_deterministico(n: int) -> bool:
    # post: devuelve True si n es primo y False en caso contrario
    d = (n - 1) // 2
    s = 1
    while d % 2 == 0:
        d = d // 2
        s = s + 1
    # n - 1 = 2**s * d  con mcd(2, d) = 1
    vr = int(min(n - 1, 2 * math.log(n)**2)) + 1
    print( 'Chequeos: ',vr)
    for a in range(2, vr):
        # print ('a', a)
        if a % 1000 == 0:
            print( 'chequeo: ',a)
        compuesto = True # True si es composite, False si no se sabe
        for r in range(s):
            chk1 = pot_mod(a, d, n)  # a**d % n calculado en forma eficiente
            chk2 = pot_mod(chk1, 2**r, n)  # a**(2**r * d) % n calculado en forma eficiente
            # print r, chk1, chk2
            compuesto = compuesto and (chk1 != 1 and chk2 != n - 1)
        if compuesto:
            return False
    return True

def main():
    """
    #n1 = 10**10+79
    n1 = 10**15+37
    #n1 = 43
    #n1 = 45
    print(test_Miller_deterministico(n1))
    
    n1 = 2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077
    n2 = 2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983
    print(test_Miller_deterministico(n1))
    k = 50 # 50 dice 0.99... (30 9's) probabilidad de ser primo
    print(test_Miller_Rabin(n1, k)) 
    """

if __name__ == "__main__":
    main()





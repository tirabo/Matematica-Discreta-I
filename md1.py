

def mcd(a, b):
    # pre: a,b enteros.
    # post: mcd divisor de a,b usando Algoritmo de Euclides. Si ambos son nulos devuelve 0.
    if b < 0:
        b = -b
    while b > 0:
        a, b = b, a % b
    return a

def mcd2(a, b):
    # pre: a,b enteros. b > 0
    # post: devuelve s,t tal que mcd(a,b) = s*a + t*b
    #       Se basa en el  Algoritmo de Euclides. La implementacion:
    #       https://es.wikipedia.org/wiki/Algoritmo_de_Euclides
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 !=0 :
        q = r0 / r1
        s1n = s0 - q * s1
        t1n = t0 - q * t1
        r0, r1 = r1, r0 % r1
        s0, s1 = s1, s1n
        t0, t1 = t1, t1n
    return  s0, t0


def cambiodebase(m, b):
    # pre: m> 0, 1<b
    # post: devuelve una lista que es la expresion de m en base b
    ret = []
    cociente = m
    while cociente > 0:
        resto = cociente % b
        cociente = cociente/b
        ret.insert(0, resto)  # inserta por delante en la lista
    return ret


def phi(natural):
    # pre: natural  entero positivo
    # post: devuelve la phi de Euler
    result = 0
    for k in range(1, natural + 1):
        if mcd(natural, k) == 1:
            result += 1
    return result

"""
Metodo binario para exponencicion modular
Ver: 'Right-to-left binary method' en https://en.wikipedia.org/wiki/Modular_exponentiation
Se desea calular b**e % m
1) Se calcula la expresion binaria de e
Si e en base 2 es a_{n}...a_0, entonces
e = \sum_{i=0}^{n} a_i 2^i
2) Entonces b**e = (b**(2**n))**a_n * ...*(b**(2**0))*a_0
luego se calcula primero
c = (b**(2**0))*a_0 % m y luego se hace
c = c*(b**(2**1))*a_1 % m
y asi sucesivamente
"""


def pot_modulo(base, exponente, modulo):
    # pre: base, exponente, modulo enteros no negativos
    # post: devuelve b**e % m usando el metodo binario
    result = 0
    if modulo > 1:
        bine = cambiodebase(exponente, 2)
        result = 1
        pot2 = base % modulo
        while len(bine) > 0:
            # print bine
            result = result*(pot2**int(bine[-1])) % modulo
            pot2 = pot2**2 % modulo
            bine = bine[:-1]
    return result


primo1 = 2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077
primo2 = 2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983
n = primo1 * primo2
m = (primo1 - 1) * (primo2 - 1)
e = 5
d = mcd2(e,m)[0]

print pot_modulo(6952221076085874809964747211172927529925899121966847505496583100,d,n)


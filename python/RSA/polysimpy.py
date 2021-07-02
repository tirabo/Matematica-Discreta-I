from sympy import *

x = symbols('x')
n = 10**100+37

f = (x + 1)**1000
g = x**2+3*x +1
q, r = div(f, g, x)


print  r
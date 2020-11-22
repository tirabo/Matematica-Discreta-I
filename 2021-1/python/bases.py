def  base(b,n):
	# pre: b es entero tal que 2 <= b <= 16. n es número entero positivo
	# post: Devuelve la representación de n en base b 
	D = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'] # posibles caracteres
	q = n // b
	rep = D[n % b] # n % b = resto de n // b
	while q != 0:
		q, r  = q // b, q % b
		rep = D[r] + rep
	return rep

def numint(b, x):
	# pre: b es entero tal que 2 <= b <= 16. x es una cadena que reprenta un número n en base b
	# post: Devuelve n.
	C = {'0': 0,  '1': 1,'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'A': 10,'B': 11,'C': 12,'D': 13,'E': 14,'F': 15}
	# diccionario  que a cada caracter le asigna el número correspondiente
	num = 0
	k = len(x)
	for i in range(k):
		num = num + C[x[k - i -1]]* b**i
	return num

def cambio(b,c,x):
	# pre:  b y c son enteros tal que 2 <= b, c <= 16. x es una cadena que reprenta un número n en base b
	# post:  devuelve la represantación de n en  base c
	n = numint(b, x)
	return base(c,n)
	
def suma(b, x, y):
	# pre: b es entero tal que 2 <= b <= 16. x, y son cadenas que reprentan números n , m en base b
	# post: devuelve n + m en base b
	n, m = numint(b, x), numint(b, y)
	return base(b, n + m)
	
def mult(b, x, y):
	# pre: b es entero tal que 2 <= b <= 16. x, y son cadenas que reprentan números n , m en base b
	# post: devuelve n * m en base b
	n, m = numint(b, x), numint(b, y)
	return base(b, n * m)
	

### Ejemplos ###

x0, y0, z0 = 16, 19, 28

print('Números: ',x0, y0, z0)

x1, y1, z1 = base(2, x0), base(2, y0), base(5, z0)

print('En base 2, 2, 5: ',x1, y1, z1) 

x2, y2, z2 = numint(2, x1), numint(2, y1), numint(5, z1)

print('De nuevo en base 10: ',x2, y2, z2)

print(x1,'+',y1,'=',suma(2, x1, y1))

print(x1,'*',y1,'=',mult(2, x1, y1))

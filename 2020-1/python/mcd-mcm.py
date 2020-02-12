def mcd(a,b):
	# pre: a y b son números enteros
	# post: obtenemos d = mcd(a,b)
	if a < 0:
		a = -a
	if b < 0:
		b = -b
	if a == 0 and b == 0:
		print('alguno de los dos números debe ser distinto de cero')
		exit(0)
	r = [a,b]
	i = 1 
	while r[i] != 0:
		r.append(r[i-1] % r[i])   # a % b = resto de a // b
		i = i + 1
	d = r[i-1]
	return d
	
def mcm(a,b):
	# pre: a y b son números positivos
	# post: obtenemos  mcm(a,b)
	return a*b // mcd(a,b)
	
def mcd2(a, b):
	# pre: a y b son números positivos
	# post: Obtenemos s y t tal que mcd(a,b) = a * s + b * t.
	# Se devuelve a, b, mcd(a,b), s, t
	if a == 0 and b == 0:
		print('alguno de los dos números debe ser distinto de cero')
		exit(0)
	r = [a, b]
	s = [1, 0]
	t = [0, 1]
	# r[0] = a * s[0] + b * t[0]
	# r[1] = a * s[1] + b * t[1]
	i = 1 
	while r[i] != 0:
		# invariante: r[i] = a * s[i] + b * t[i]
		r.append(0), s.append(0),  t.append(0) # para que esten definidos r[i+1], s[i+1], t[i+1] 
		q, r[i+1] = r[i-1] // r[i], r[i-1] % r[i]
		s[i+1] = s[i-1] - s[i] * q
		t[i+1] = t[i-1] - t[i] * q
		i = i+1
	s, t  = s[i-1], t[i-1]
	return a, b, a * s + b * t, s, t
# Demostración: por  algoritmo de Euclides tenemos
# r[i-1] =  r[i] * q + r[i+1], con q =  r[i-1] // r[i] (*)
# Si tenemos
#  r[i] = a * s[i] + b * t[i]
#  r[i-1] = a * s[i-1] + b * t[i-1]
# Por (*)
# r[i+1] = r[i-1] - r[i] * q
#          = a * s[i-1] + b * t[i-1] - (a * s[i] + b * t[i]) * q
#          = a * (s[i-1] - q * s[i]) + b * (t[i-1] - q * t[i])
# Luego, s[i+1] = s[i-1] - q * s[i], t[i+1] = t[i-1] - q * t[i]
print(mcd2(15,21))

	
	
	
# Ejemplos
print(mcd(-15,21))
print(mcm(15,21))

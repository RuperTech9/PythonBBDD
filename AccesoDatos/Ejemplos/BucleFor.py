print("--------------BUCLE FOR-------------")

for i in [0, 1, 2, 3, 4]:
    print(f"El valor de i es :{i}")

print("--------------BUCLE FOR-------------")

listaNumeros = [0, 1, 2, 3, 4]

for i in listaNumeros:
    print(f"El valor de i es :{i}")

print("--------------BUCLE FOR CON SECUENCIA-------------")

# Podemos incluir range para incluir una secuencia

for i in range(10):
    print(f"El valor de i es :{i}")

# Bucle for con cadenas
print("--------------BUCLE FOR CON CADENAS-------------")
Nombres = ['Benito', 'Floro', 'Rosa', 'Luisa']

for valor in Nombres:
    print(valor)

# Bucle for con cadenas y Range
print("--------------BUCLE FOR CON CADENA Y RANGO-------------")

for valor in range(len(Nombres)):
    print ("Nombre:", Nombres[valor], "posicion:", valor)

print("--------------BUCLE FOR CON SECUENCIA-------------")

for i in range(1, 11):
    print(f"El valor de i es :{i}")

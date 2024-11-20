print("--------------CALCULAR FACTORIAL DE UN NÚMERO------------")

factorial = 1
numero=int(input("Introduzca un número:"))
dato=numero
while numero != 0:
    factorial = factorial * numero
    numero=numero-1

print(f"El factorial de {dato} es {factorial}")

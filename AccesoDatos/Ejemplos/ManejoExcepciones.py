def controlErrores():
    try:
        numero = int(input("Introduce número:"))
        print("Número:",numero)
    except ValueError:
        print ("Error, debes introducir un número")
        controlErrores()
print("Ejemplo 1")
controlErrores()


def controlErrores2():
    try:
        dividendo = int(input("Introduce dividendo:"))
        divisor = int(input("Introduce divisor:"))
        resultado = dividendo / divisor
        print(f"Resultado división: {resultado}")
    except ValueError:
        print("Error, debes introducir un número")
    except ZeroDivisionError:
        print("¡¡¡Error!!!. El divisor no puede ser cero")
    finally:
        print("ENTRA")


print("\nEjemplo 2")
controlErrores2()

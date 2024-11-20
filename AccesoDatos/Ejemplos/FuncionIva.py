def calcularIVA():
    importe = int(input("Precio del producto: "))
    total = importe* 1.21
    print (f"IVA incluido (21%): {total}")
    return

print("\nLLAMANDO A LA FUNCIÓN 1")
calcularIVA()



def calcularIVA2(importe):
    print (f"Precio del producto: {importe}")

    total = importe* 1.21
    print (f"IVA incluido (21%): {total}")
    return

print("\nLLAMANDO A LA FUNCIÓN 2")
importe = int(input("Precio del producto: "))
calcularIVA2(importe)




def calcularIVA3(importe):
    print (f"Precio del producto: {importe}")
    total = importe* 1.21
    return total


print("\nLLAMANDO A LA FUNCIÓN 3")
result=calcularIVA3(1000)
print(f"IVA incluido (21%): {result}")


def calcularIVA(importe):
    total = importe* 1.21
    return importe,total


print("\nLLAMANDO A LA FUNCIÓN 4")
precio,result=calcularIVA(2000)

print(f"Precio del producto: {precio}")
print(f"IVA incluido (21%): {result}")


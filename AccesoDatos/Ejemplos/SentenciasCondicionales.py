print("--------------SENTENCIA IF-------------")

edad= 20
if edad == 20:
    print("TIENES 20 AÑOS")

print("--------------SENTENCIA IF...ELSE-------------")

edad= 20
if edad < 18:
    print("TIENES MENOS DE 18 AÑOS")
else:
    print("TIENES MÁS O IGUAL A 18 AÑOS")


print("--------------SENTENCIA IF...ELIF...ELSE-------------")

nota=8
if nota < 0:
    print("VALOR NEGATIVO")
elif nota<=5:
    print("SUSPENSO")
else:
    print("APROBADO")

import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='ruper', password='A1a2A3a4A5', database='Hospital')
cursor = bd_conexion.cursor()
try:
    cursor.execute("SELECT apellido,oficio,salario FROM emp")

    for ape, ofi, sal in cursor:
        print("Apellido: " + ape)
        print("Oficio: " + ofi)
        print("Salario: " + str(sal))
        print()

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()

import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='ruper', password='A1a2A3a4A5', database='Hospital')
cursor = bd_conexion.cursor()
try:
    miOficio=input("Introduce Oficio Empleado:")
    consulta=("SELECT apellido,oficio,salario FROM emp where oficio=%s")
    cursor.execute(consulta,(miOficio,))
    # Si en un único parámetro tenemos que poner ',' a continuación del valor de la variable

    for ape, ofi, sal in cursor:
         print("Apellido: ", ape)
         print("Oficio: " ,ofi)
         print("Salario: " , str(sal))

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()

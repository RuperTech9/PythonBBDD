
import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='ruper', password='A1a2A3a4A5', database='Hospital')
cursor = bd_conexion.cursor()
ConsultaModificacion = ("Update emp set salario=%s where emp_no=%s")

NumeroEmpleado = input("Número de empleado a modificar:")
NuevoSal= input("Nuevo salario:")

cursor.execute(ConsultaModificacion, (NuevoSal,NumeroEmpleado,))
if cursor.rowcount>0:
    print ("Registro modificado satisfactoriamente")
else:
    print ("Dato no encontrado")

bd_conexion.commit()

cursor.close()
bd_conexion.close()

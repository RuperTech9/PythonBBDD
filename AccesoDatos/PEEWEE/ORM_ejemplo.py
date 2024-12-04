from peewee import *

# Configuración de la base de datos MySQL
mysql_db = MySQLDatabase(
    "ejemplo",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',
    charset='utf8mb4')  # Asegura compatibilidad con caracteres especiales)

class BaseModel(Model):
    class Meta:
        database = mysql_db

class Departamentos(BaseModel):
    dept_no = AutoField(primary_key=True)
    dnombre = CharField()
    loc = CharField()

    class Meta:
        table_name = 'departamentos'

class Empleados(BaseModel):
    emp_no = AutoField(primary_key=True)
    apellido = CharField()
    comision = FloatField()
    dir = IntegerField()
    fecha_alt = DateField()
    oficio = CharField()
    salario = FloatField()
    dept_no = ForeignKeyField(Departamentos,backref='Empleados', column_name='dept_no')

    class Meta:
        table_name = 'empleados'



# Función para agregar un departamento
def agregar_departamento():
    dept_no = input("Introduce el número del departamento: ")
    dnombre = input("Introduce el nombre del departamento: ")
    loc = input("Introduce la localidad del departamento: ")

    # Verificar si el usuario ya existe
    departamento_existente = Departamentos.select().where(Departamentos.dept_no == dept_no).first()
    if departamento_existente:
        print(f"El departamento con número '{dept_no}' ya existe: {departamento_existente.dept_no}.")
    else:
        # Insertar un nuevo usuario en la tabla 'usuario'
        nuevo_departamento = Departamentos.create(
            dept_no=dept_no,
            dnombre=dnombre,
            loc=loc
        )
        print(f"Usuario creado: {nuevo_departamento.dept_no}, {nuevo_departamento.dnombre}, {nuevo_departamento.loc}")

# Función para borrar un usuario
def borrar_departamento():
    dept_no = input("Introduce el email del usuario que deseas borrar: ")
    departamento_existente = Departamentos.select().where(Departamentos.dept_no == dept_no).first()
    if departamento_existente:
        departamento_existente.delete_instance()
        print(f"El departamento con número '{dept_no}' ha sido eliminado.")
    else:
        print(f"No se encontró un departamento con número '{dept_no}'.")

# Función para listar departamentos
def listar_departamentos():
    # Leer datos de la tabla 'dept'
    print("Datos de la tabla 'dept':")
    for departamento in Departamentos.select():
        print(
            "Dept Nº: ", departamento.dept_no,
            "Nombre: ", departamento.dnombre,
            "Localidad: ", departamento.loc
        )

# Función para modificar un departamento
def modificar_departamento():
    dept_no = input("Introduce el número del departamento que deseas modificar: ")
    departamento_existente = Departamentos.select().where(Departamentos.dept_no == dept_no).first()

    if departamento_existente:
        print(f"Departamento encontrado: {departamento_existente.dnombre}, {departamento_existente.loc}")

        nuevo_nombre = input("Introduce el nuevo nombre del departamento (presiona Enter para no cambiar): ")
        nueva_localidad = input("Introduce la nueva localidad del departamento (presiona Enter para no cambiar): ")

        # Actualizar los campos si se proporciona un nuevo valor
        if nuevo_nombre.strip():
            departamento_existente.dnombre = nuevo_nombre
        if nueva_localidad.strip():
            departamento_existente.loc = nueva_localidad

        departamento_existente.save()  # Guardar los cambios
        print(f"El departamento con número '{dept_no}' ha sido actualizado.")
    else:
        print(f"No se encontró un departamento con número '{dept_no}'.")
# ----------------------------------------------------------------------------------------------------------------
# Conectar a la base de datos
mysql_db.connect()

while True:
    print("\n--- Menú Principal ---")
    print("1. Agregar departamentos")
    print("2. Borrar departamentos")
    print("3. Modificar departamentos")
    print("4. Listar departamentos")
    print("5. Salir")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        agregar_departamento()
    elif opcion == "2":
        borrar_departamento()
    elif opcion == "3":
        modificar_departamento()
    elif opcion == "4":
        listar_departamentos()
    elif opcion == "5":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intenta nuevamente.")

mysql_db.close()
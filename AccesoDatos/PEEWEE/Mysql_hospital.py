import peewee
import datetime

# Configuración de la base de datos MySQL
database = peewee.MySQLDatabase(
    "hospital",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',
    charset='utf8mb4'  # Asegura compatibilidad con caracteres especiales
)

# Conexión a la tabla 'dept'
class Departamentos(peewee.Model):
    dept_no = peewee.IntegerField(primary_key=True)
    dnombre = peewee.CharField()
    loc = peewee.CharField()

    class Meta:
        database = database  # Conexión a la base de datos
        db_table = 'dept'  # Nombre de la tabla en la base de datos

# Modelo para la tabla 'usuario'
class Usuario(peewee.Model):
    nombre = peewee.CharField()
    email = peewee.CharField()
    fecha_creacion = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database  # Conexión a la base de datos
        db_table = 'usuario'  # Nombre de la nueva tabla

# Conectar a la base de datos
database.connect()

# Leer datos de la tabla 'dept'
print("Datos de la tabla 'dept':")
for departamento in Departamentos.select():
    print(f"Dept No: {departamento.dept_no}, Nombre: {departamento.dnombre}, Loc: {departamento.loc}")

# Crear la tabla 'usuario' si no existe
database.create_tables([Usuario])
print("La tabla 'usuario' ha sido creada exitosamente.")

# Función para agregar un usuario
def agregar_usuario():
    nombre = input("Introduce el nombre del usuario: ")
    email = input("Introduce el email del usuario: ")

    # Verificar si el usuario ya existe
    usuario_existente = Usuario.select().where(Usuario.email == email).first()
    if usuario_existente:
        print(f"El usuario con el email '{email}' ya existe: {usuario_existente.nombre}, creado el {usuario_existente.fecha_creacion}.")
    else:
        # Insertar un nuevo usuario en la tabla 'usuario'
        nuevo_usuario = Usuario.create(
            nombre=nombre,
            email=email
        )
        print(f"Usuario creado: {nuevo_usuario.nombre}, {nuevo_usuario.email}, {nuevo_usuario.fecha_creacion}")


# Función para borrar un usuario
def borrar_usuario():
    email = input("Introduce el email del usuario que deseas borrar: ")
    usuario_existente = Usuario.select().where(Usuario.email == email).first()
    if usuario_existente:
        usuario_existente.delete_instance()
        print(f"El usuario con el email '{email}' ha sido eliminado.")
    else:
        print(f"No se encontró un usuario con el email '{email}'.")


# Función para modificar un usuario
def modificar_usuario():
    email = input("Introduce el email del usuario que deseas modificar: ")
    usuario_existente = Usuario.select().where(Usuario.email == email).first()
    if usuario_existente:
        print(f"Usuario encontrado: {usuario_existente.nombre}, {usuario_existente.email}.")
        nuevo_nombre = input("Introduce el nuevo nombre (deja vacío para no cambiar): ")
        nuevo_email = input("Introduce el nuevo email (deja vacío para no cambiar): ")

        if nuevo_nombre:
            usuario_existente.nombre = nuevo_nombre
        if nuevo_email:
            usuario_existente.email = nuevo_email

        usuario_existente.save()
        print(f"Usuario actualizado: {usuario_existente.nombre}, {usuario_existente.email}.")
    else:
        print(f"No se encontró un usuario con el email '{email}'.")


# Función para listar usuarios
def listar_usuarios():
    print("\nLista de usuarios:")
    usuarios = Usuario.select()
    if usuarios.exists():
        for usuario in usuarios:
            print(f"Nombre: {usuario.nombre}, Email: {usuario.email}, Fecha de Creación: {usuario.fecha_creacion}")
    else:
        print("No hay usuarios registrados.")

# Función para listar departamentos
def listar_departamentos():
    print("\nLista de departamentos:")
    departamentos = Departamentos.select()
    if departamentos.exists():
        for departamento in departamentos:
            print(f"Dept No: {departamento.dept_no}, Nombre: {departamento.dnombre}, Loc: {departamento.loc}")
    else:
        print("No hay departamentos registrados.")

# Menú principal
while True:
    print("\n--- Menú Principal ---")
    print("1. Agregar usuario")
    print("2. Borrar usuario")
    print("3. Modificar usuario")
    print("4. Listar usuarios")
    print("5. Listar departamentos")
    print("6. Salir")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        agregar_usuario()
    elif opcion == "2":
        borrar_usuario()
    elif opcion == "3":
        modificar_usuario()
    elif opcion == "4":
        listar_usuarios()
    elif opcion == "5":
        listar_departamentos()
    elif opcion == "6":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intenta nuevamente.")

# Cerrar la conexión
database.close()
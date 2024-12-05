import datetime
from _pyrepl.readline import raw_input
import peewee


# Configuración de la base de datos
database = peewee.MySQLDatabase(
    "ejemplo2",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',  # Corregido el nombre del parámetro
    charset='utf8mb4',
)

# Definición del modelo
class Usuario(peewee.Model):
    nombre = peewee.CharField(unique=True)
    email = peewee.CharField(index=True)
    fechaCreacion = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        db_table = 'Usuario'

if __name__ == '__main__':
    # Conexión a la base de datos
    database.connect()

    # Crear la tabla si no existe
    if not Usuario.table_exists():
        Usuario.create_table()

    # Solicitar datos al usuario
    nombre = raw_input("Ingrese un nombre: ")
    email = raw_input("Ingrese un correo electrónico: ")

    # Verificar si el usuario ya existe
    if not Usuario.select().where(Usuario.nombre == nombre).exists():
        new_user = Usuario.create(nombre=nombre, email=email)
        new_user.save()
        print("Usuario registrado exitosamente.")
    else:
        print("El usuario ya se encuentra registrado.")
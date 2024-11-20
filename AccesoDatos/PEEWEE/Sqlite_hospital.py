from peewee import SqliteDatabase, Model, IntegerField, CharField

# Configuración de la base de datos
db = SqliteDatabase('hospital.db')


# Modelo para la tabla DEPT
class Departamentos(Model):
    dept_no = IntegerField(primary_key=True)
    dnombre = CharField()
    loc = CharField()

    class Meta:
        database = db
        table_name = 'DEPT'


# Clase para manejar la conexión y las operaciones con la base de datos
class DatabaseManager:
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.database = db

    def connect(self):
        """Conecta a la base de datos."""
        try:
            self.database.connect()
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def close(self):
        """Cierra la conexión a la base de datos."""
        if not self.database.is_closed():
            self.database.close()
            print("Conexión cerrada.")

    def fetch_departments(self):
        """Obtiene y muestra todos los departamentos."""
        try:
            departamentos = Departamentos.select()
            print("\nDepartamentos:")
            for dept in departamentos:
                print(f"Dept No: {dept.dept_no}, Nombre: {dept.dnombre}, Loc: {dept.loc}")
        except Exception as e:
            print(f"Error al consultar los departamentos: {e}")


# Uso de la clase
if __name__ == "__main__":
    manager = DatabaseManager()  # Crear instancia del gestor de base de datos
    manager.connect()  # Conectar a la base de datos
    manager.fetch_departments()  # Mostrar departamentos
    manager.close()  # Cerrar la conexión

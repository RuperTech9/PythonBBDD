from peewee import *

# Configuración de la base de datos MySQL
mysql_db = MySQLDatabase(
    "hospital",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',
    charset='utf8mb4')

class BaseModel(Model):
    class Meta:
        database = mysql_db

class DEPT(BaseModel):
    dept_no = IntegerField(primary_key=True)  # Clave primaria explícita
    dnombre = CharField()
    loc = CharField()
    class Meta:
        table_name = 'DEPT'

class EMP(BaseModel):
    emp_no = IntegerField(primary_key=True)  # Clave primaria explícita
    apellido = CharField()
    oficio = CharField()
    dir = IntegerField()
    fecha_alt = DateField()
    salario = IntegerField()
    comision = IntegerField()
    dept_no = ForeignKeyField(DEPT, backref='empleado', column_name='dept_no')
    class Meta:
        table_name = 'EMP'

class HOSPITAL(BaseModel):
    hospital_cod = IntegerField(primary_key=True)  # Clave primaria explícita
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    num_cama = IntegerField()
    class Meta:
        table_name = 'HOSPITAL'

class SALA(BaseModel):
    hospital_cod = ForeignKeyField(HOSPITAL, backref='sala', column_name='hospital_cod')
    sala_cod = IntegerField(primary_key=True)  # Clave primaria explícita
    nombre = CharField()
    num_cama = IntegerField()
    class Meta:
        table_name = 'SALA'

class DOCTOR(BaseModel):
    hospital_cod = ForeignKeyField(HOSPITAL, backref='doctor', column_name='hospital_cod')
    doctor_no = IntegerField(primary_key=True)  # Clave primaria explícita
    apellido = CharField()
    especialidad = CharField()
    salario = IntegerField()
    class Meta:
        table_name = 'DOCTOR'

class PLANTILLA(BaseModel):
    hospital_cod = ForeignKeyField(HOSPITAL, backref='plantilla', column_name='hospital_cod')
    sala_cod = ForeignKeyField(SALA, backref='plantilla', column_name='sala_cod')
    empleado_no = IntegerField(primary_key=True)  # Clave primaria explícita
    apellido = CharField()
    funcion = CharField()
    turno = CharField()
    salario = IntegerField()
    class Meta:
        table_name = 'PLANTILLA'

class ENFERMO(BaseModel):
    inscripcion = IntegerField(primary_key=True)  # Clave primaria explícita
    apellido = CharField()
    direccion = CharField()
    fecha_nac = DateField()
    sexo = CharField()
    nss = IntegerField()
    class Meta:
        table_name = 'ENFERMO'

class OCUPACION(BaseModel):
    inscripcion = ForeignKeyField(ENFERMO, backref='ocupacion', column_name='inscripcion')
    hospital_cod = ForeignKeyField(HOSPITAL, backref='ocupacion', column_name='hospital_cod')
    sala_cod = ForeignKeyField(SALA, backref='ocupacion', column_name='sala_cod')
    cama = IntegerField()
    class Meta:
        table_name = 'OCUPACION'
        primary_key = CompositeKey('inscripcion', 'hospital_cod', 'sala_cod')  # Clave compuesta



# ----------------------------------------------------------------------------------------------------------------
# Conectar a la base de datos
mysql_db.connect()

# Consulta para obtener los datos de los proveedores
query = PLANTILLA.select()
print("\n1- Datos de la Plantilla:")
for planti in query:
    print(
        "Código Hospital: ", planti.hospital_cod,
        "Código Sala: ", planti.sala_cod,
        "Número empleado: ", planti.empleado_no,
        "Funcion: ", planti.funcion,
        "Turno: ", planti.turno,
        "Salario: ", planti.salario
    )

mysql_db.close()

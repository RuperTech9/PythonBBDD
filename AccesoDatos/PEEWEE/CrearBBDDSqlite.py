import sqlite3

# Conexión a SQLite (creará el archivo hospital.db si no existe)
conexion = sqlite3.connect('hospital.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear las tablas
cursor.executescript("""
CREATE TABLE IF NOT EXISTS DEPT (
    DEPT_NO INT NOT NULL,
    DNOMBRE VARCHAR(40) NULL,
    LOC VARCHAR(50) NULL
);

CREATE TABLE IF NOT EXISTS EMP (
    EMP_NO INT NOT NULL,
    APELLIDO VARCHAR(40),
    OFICIO VARCHAR(40),
    DIR INT,
    FECHA_ALT DATE,
    SALARIO INT,
    COMISION INT,
    DEPT_NO INT
);

CREATE TABLE IF NOT EXISTS HOSPITAL (
    HOSPITAL_COD INT NOT NULL,
    NOMBRE VARCHAR(40),
    DIRECCION VARCHAR(50),
    TELEFONO VARCHAR(9),
    NUM_CAMA INT
);

CREATE TABLE IF NOT EXISTS SALA (
    HOSPITAL_COD INT NOT NULL,
    SALA_COD INT,
    NOMBRE VARCHAR(40),
    NUM_CAMA INT
);

CREATE TABLE IF NOT EXISTS DOCTOR (
    HOSPITAL_COD INT,
    DOCTOR_NO INT,
    APELLIDO VARCHAR(50),
    ESPECIALIDAD VARCHAR(40),
    SALARIO INT
);

CREATE TABLE IF NOT EXISTS PLANTILLA (
    HOSPITAL_COD INT,
    SALA_COD INT,
    EMPLEADO_NO INT NOT NULL,
    APELLIDO VARCHAR(40),
    FUNCION VARCHAR(30),
    TURNO VARCHAR(1),
    SALARIO INT
);

CREATE TABLE IF NOT EXISTS ENFERMO (
    INSCRIPCION INT NOT NULL,
    APELLIDO VARCHAR(40),
    DIRECCION VARCHAR(50),
    FECHA_NAC DATE,
    SEXO VARCHAR(1),
    NSS INT
);

CREATE TABLE IF NOT EXISTS OCUPACION (
    INSCRIPCION INT NOT NULL,
    HOSPITAL_COD INT NOT NULL,
    SALA_COD INT NOT NULL,
    CAMA INT
);
""")
print("Tablas creadas exitosamente.")

# Insertar datos en las tablas
cursor.executescript("""
INSERT INTO DEPT (DEPT_NO, DNOMBRE, LOC) VALUES
    (10, 'CONTABILIDAD', 'SEVILLA'),
    (20, 'INVESTIGACIÓN', 'MADRID'),
    (30, 'VENTAS', 'BARCELONA'),
    (40, 'PRODUCCIÓN', 'BILBAO');

INSERT INTO HOSPITAL (HOSPITAL_COD, NOMBRE, DIRECCION, TELEFONO, NUM_CAMA) VALUES
    (19, 'provincial', 'o donell 50', '964-4264', 502),
    (18, 'general', 'Atocha s/n', '595-3111', 987),
    (22, 'la paz', 'castellana 1000', '923-5411', 412),
    (45, 'san carlos', 'ciudad universitaria', '597-1500', 845),
    (17, 'ruber', 'juan bravo 49', '914027100', 217);

INSERT INTO SALA (HOSPITAL_COD, SALA_COD, NOMBRE, NUM_CAMA) VALUES
    (19, 3, 'cuidados intensivos', 21),
    (19, 6, 'psiquiatria', 67),
    (18, 3, 'cuidados intensivos', 10),
    (18, 4, 'cardiologia', 53),
    (22, 1, 'recuperacion', 10),
    (22, 6, 'psiquiatria', 118),
    (22, 2, 'maternidad', 34),
    (45, 4, 'cardiologia', 55),
    (45, 1, 'recuperacion', 17),
    (45, 2, 'maternidad', 24),
    (17, 2, 'maternidad', 19),
    (17, 6, 'psiquiatria', 20),
    (17, 3, 'cuidados intensivos', 21);

INSERT INTO PLANTILLA (HOSPITAL_COD, SALA_COD, EMPLEADO_NO, APELLIDO, FUNCION, TURNO, SALARIO) VALUES
    (19, 6, 3754, 'diaz b.', 'ENFERMERO', 'T', 226200),
    (19, 6, 3106, 'hernandez j.', 'ENFERMERO', 'T', 275500),
    (18, 4, 6357, 'karplus w.', 'INTERINO', 'T', 337900),
    (22, 6, 1009, 'higueras d.', 'ENFERMERA', 'T', 200500),
    (22, 6, 8422, 'bocina g.', 'ENFERMERO', 'M', 163800),
    (22, 2, 9901, 'nuñez c.', 'INTERINO', 'M', 221000),
    (22, 1, 6065, 'rivera g.', 'ENFERMERA', 'N', 162600),
    (22, 1, 7379, 'carlos r.', 'ENFERMERA', 'T', 211900),
    (45, 4, 1280, 'amigo r.', 'INTERINO', 'N', 221000),
    (45, 1, 8526, 'frank h.', 'ENFERMERO', 'T', 252200),
    (17, 2, 8519, 'chuko c.', 'ENFERMERO', 'T', 252200),
    (17, 6, 8520, 'palomo c.', 'INTERINO', 'M', 219210),
    (17, 6, 8521, 'cortes v.', 'ENFERMERA', 'N', 221200);
""")
print("Datos insertados exitosamente.")

# Confirmar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()
print("Conexión cerrada.")

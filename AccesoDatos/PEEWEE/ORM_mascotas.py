from peewee import *
from datetime import date

sqlite_db = SqliteDatabase('mascotas.db')

class Persona(Model):
    nombre = CharField()
    fecha_nacimiento = DateField()

    class Meta:
        database = sqlite_db

class Mascota(Model):
    propietario = ForeignKeyField(Persona,backref='mascotas')
    nombre = CharField()
    raza = CharField()

    class Meta:
        database = sqlite_db


# ----------------------------------------------------------------------------------------------------------------------
sqlite_db.connect()

# CREAR TABLAS
sqlite_db.create_tables([Persona, Mascota])

# INSERTAR DATOS
primo_bob = Persona.create(nombre='Bob', fecha_nacimiento=date(1960,1,15))
abuela = Persona.create(nombre='Abuela', fecha_nacimiento=date(1935,3,1))
mascota_bob = Mascota.create(propietario=primo_bob, nombre="Milo", raza='Perro')

# ----------------------------------------------------------------------------------------------------------------------
# Recuperar todas las personas
print("Personas")
for persona in Persona.select():
    print(persona.nombre, persona.fecha_nacimiento)

# Recuperar todas las mascotas de Bob
print("\nMascotas de Bob")
for mascota in Mascota.select().where(Mascota.propietario == primo_bob):
    print(mascota.nombre)

# Obtener todas las mascotas y el nombre de sus dueños
print("\nMascotas y sus dueños")
query = Mascota.select(Mascota, Persona).join(Persona)
for mascota in query:
    print(f"{mascota.nombre} pertenece a {mascota.propietario.nombre}")

# Cambiar el nombre de la abuela
abuela.nombre = 'Abuela L.'
abuela.save()

# Eliminar una mascota
mascota_bob.delete_instance()

# Obtener personas nacidas antes de 1940
print("\nPersonas nacidas antes de 1940")
for persona in Persona.select().where(Persona.fecha_nacimiento < date(1940, 1, 1)):
    print(persona.nombre)

# Contar mascotas por persona
query = (Persona
         .select(Persona, fn.COUNT(Mascota.id).alias('pet_count'))
         .join(Mascota, JOIN.LEFT_OUTER)
         .group_by(Persona))
print("\nMascotas por persona")
for persona in query:
    print(f"{persona.nombre} tiene {persona.pet_count} mascotas")

sqlite_db.close()
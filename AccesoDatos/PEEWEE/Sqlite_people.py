from peewee import *
from datetime import date
from peewee import fn

# Crear o conectarse a una base de datos SQLite
db = SqliteDatabase('people.db')  # Esto crea un archivo 'people.db' en tu sistema

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # Asocia este modelo con la base de datos

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')  # Relación con la tabla 'Person'
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Pet])  # Crea las tablas 'Person' y 'Pet'

# Agregar registros a la tabla 'Person'
uncle_bob = Person.create(name='Bob', birthday=date(1960, 1, 15))
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))

# Agregar registros a la tabla 'Pet'
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')

# Recuperar todas las personas
for person in Person.select():
    print(person.name, person.birthday)

# Recuperar todas las mascotas de Bob
for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)

# Obtener todas las mascotas y el nombre de sus dueños
query = Pet.select(Pet, Person).join(Person)
for pet in query:
    print(f"{pet.name} pertenece a {pet.owner.name}")

# Cambiar el nombre de la abuela
grandma.name = 'Grandma L.'
grandma.save()

# Eliminar una mascota
bob_kitty.delete_instance()

# Obtener personas nacidas antes de 1940
for person in Person.select().where(Person.birthday < date(1940, 1, 1)):
    print(person.name)

# Contar mascotas por persona
query = (Person
         .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
         .join(Pet, JOIN.LEFT_OUTER)
         .group_by(Person))

for person in query:
    print(f"{person.name} tiene {person.pet_count} mascotas")

db.close()
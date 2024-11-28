import peewee
import datetime

from peewee import Database, SmallIntegerField, ForeignKeyField

# Configuración de la base de datos MySQL
database = peewee.MySQLDatabase(
    "tienda",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',
    charset='utf8mb4'  # Asegura compatibilidad con caracteres especiales
)

class clientes(peewee.Model):
    codigo_cli = peewee.IntegerField(primary_key=True)
    nombre = peewee.CharField()
    localidad = peewee.CharField()
    tlf = peewee.CharField()

    class Meta:
        database = database
        db_table = 'clientes'

class proveedores(peewee.Model):
    codigo_prov = peewee.SmallIntegerField(primary_key=True)
    nombre = peewee.CharField()
    localidad = peewee.CharField()
    fecha_alta = peewee.DateTimeField

    class Meta:
        database = database
        db_table = 'proveedores'

class articulos(peewee.Model):
    codarticulo = peewee.SmallIntegerField(primary_key=True)
    denominacion  = peewee.CharField()
    precio = peewee.FloatField()
    stock = SmallIntegerField()
    zona = peewee.CharField()
    codigo_prov = ForeignKeyField(proveedores, backref='articulos', column_name='codigo_prov')

    class Meta:
        database = database
        db_table = 'articulos'

class compras(peewee.Model):
    numcompra = peewee.SmallIntegerField(primary_key=True)
    fechacompra = peewee.DateTimeField()
    codigo_cli = ForeignKeyField(clientes, backref='compras', column_name='codigo_cli' )

    class Meta:
        database = database
        table_name = 'compras'

# Modelo de detalle de compras
class detallecompras(peewee.Model):
    numcompra = ForeignKeyField(compras, backref='detalles', column_name='numcompra')
    codarticulo = ForeignKeyField(articulos, backref='detalles', column_name='codarticulo')
    unidades = peewee.SmallIntegerField()

    class Meta:
        database = database
        table_name = 'detallecompras'
        primary_key = peewee.CompositeKey('numcompra', 'codarticulo')

# Conectar a la base de datos
database.connect()

# Consulta de ejemplo: Obtener los datos de los clientes y sus compras
print("\n1. Obtener los datos de los clientes y sus compras")
query = (clientes
         .select(clientes, compras)
         .join(compras, peewee.JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli)))

for result in query.dicts():
    print(result)

print("\n2. Obtener lo mismo que en la pregunta 1, visualizando código de cliente, nombre, localidad, número de compra y fecha de compra (mostrando 0 para clientes sin compras).")
query = (clientes
         .select(
             clientes.codigo_cli,
             clientes.nombre,
             clientes.localidad,
             peewee.fn.COALESCE(compras.numcompra, 0).alias('numcompra'),
             compras.fechacompra
         )
         .join(compras, peewee.JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli)))

for result in query.dicts():
    print(result)

print("\n3. Obtener por cada cliente el detalle de compras realizado")
query = (clientes
         .select(
             clientes.codigo_cli,
             clientes.nombre,
             clientes.localidad,
             compras.numcompra,
             detallecompras.codarticulo,
             detallecompras.unidades,
             articulos.precio,
             (detallecompras.unidades * articulos.precio).alias('importe')
         )
         .join(compras, on=(clientes.codigo_cli == compras.codigo_cli))
         .join(detallecompras, on=(compras.numcompra == detallecompras.numcompra))
         .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo)))

for result in query.dicts():
    print(result)

print("\n4. Obtener el total de compra de cada cliente")
query = (clientes
         .select(
             clientes.codigo_cli,
             clientes.nombre,
             clientes.localidad,
             compras.numcompra,
             peewee.fn.SUM(detallecompras.unidades * articulos.precio).alias('importe_total')
         )
         .join(compras, on=(clientes.codigo_cli == compras.codigo_cli))
         .join(detallecompras, on=(compras.numcompra == detallecompras.numcompra))
         .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo))
         .group_by(clientes.codigo_cli, compras.numcompra))

for result in query.dicts():
    print(result)

print("\n5. Obtener el total de las compras de cada cliente y el número de compras realizadas")
query = (clientes
         .select(
             clientes.codigo_cli,
             clientes.nombre,
             clientes.localidad,
             clientes.tlf,
             peewee.fn.COUNT(compras.numcompra).alias('total_compras'),
             peewee.fn.COALESCE(peewee.fn.SUM(detallecompras.unidades * articulos.precio), 0).alias('importe_total')
         )
         .join(compras, peewee.JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli))
         .join(detallecompras, peewee.JOIN.LEFT_OUTER, on=(compras.numcompra == detallecompras.numcompra))
         .join(articulos, peewee.JOIN.LEFT_OUTER, on=(detallecompras.codarticulo == articulos.codarticulo))
         .group_by(clientes.codigo_cli))

for result in query.dicts():
    print(result)

print("\n6. Obtener para cada artículo las unidades compradas por los clientes, el importe y el nombre de su proveedor. Se deben visualizar los artículos sin compras.")
query = (articulos
         .select(
             articulos.codarticulo,
             articulos.denominacion,
             articulos.stock,
             articulos.precio,
             peewee.fn.COALESCE(peewee.fn.SUM(detallecompras.unidades), 0).alias('unidades_compradas'),
             peewee.fn.COALESCE(peewee.fn.SUM(detallecompras.unidades * articulos.precio), 0).alias('importe'),
             proveedores.nombre.alias('nombre_proveedor')
         )
         .join(proveedores, on=(articulos.codigo_prov == proveedores.codigo_prov))
         .join(detallecompras, peewee.JOIN.LEFT_OUTER, on=(articulos.codarticulo == detallecompras.codarticulo))
         .group_by(articulos.codarticulo, articulos.denominacion, articulos.stock, articulos.precio, proveedores.nombre))

for result in query.dicts():
    print(result)

print("\n7. Obtener para cada proveedor los artículos que suministra")
query = (proveedores
         .select(
             proveedores.codigo_prov,
             proveedores.nombre,
             articulos.codarticulo,
             articulos.denominacion
         )
         .join(articulos, on=(proveedores.codigo_prov == articulos.codigo_prov)))

for result in query.dicts():
    print(result)

print("\n8. Visualizar por cada proveedor el número de artículos que suministra")
query = (proveedores
         .select(
             proveedores.codigo_prov,
             proveedores.nombre,
             peewee.fn.COUNT(articulos.codarticulo).alias('num_articulos')
         )
         .join(articulos, peewee.JOIN.LEFT_OUTER, on=(proveedores.codigo_prov == articulos.codigo_prov))
         .group_by(proveedores.codigo_prov, proveedores.nombre))

for result in query.dicts():
    print(result)

print("\n9. Visualizar el código de cliente, nombre y localidad de los clientes de Talavera que compraron artículos de la zona Centro")
query = (clientes
         .select(
             clientes.codigo_cli,
             clientes.nombre,
             clientes.localidad
         )
         .join(compras, on=(clientes.codigo_cli == compras.codigo_cli))
         .join(detallecompras, on=(compras.numcompra == detallecompras.numcompra))
         .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo))
         .where(
             (clientes.localidad == 'Barcelona') &
             (articulos.zona == 'Zona B')
         )
         .distinct())

for result in query.dicts():
    print(result)

print("\n10. Visualizar código, nombre y localidad de los proveedores que suministran artículos de la zona centro")
query = (proveedores
         .select(
             proveedores.codigo_prov,
             proveedores.nombre,
             proveedores.localidad
         )
         .join(articulos, on=(proveedores.codigo_prov == articulos.codigo_prov))
         .where(articulos.zona == 'Zona A')
         .distinct())

for result in query.dicts():
    print(result)


# Cerrar la conexión
database.close()
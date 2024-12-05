from peewee import *
from datetime import datetime

# Configuración de la base de datos MySQL
database = MySQLDatabase(
    "tienda",
    host='localhost',
    port=3306,
    user='ruper',
    password='A1a2A3a4A5',
    charset='utf8mb4')  # Asegura compatibilidad con caracteres especiales)

# Configuración de la base de datos SQLite
sqlite_db = SqliteDatabase('hospital.db')

# Configuración de la base de datos PostgreSQL
postgres_db = PostgresqlDatabase(
    "tienda",
    user="ruper",
    password="A1a2A3a4A5",
    host="localhost",
    port=5432,  # Puerto por defecto de PostgreSQL
)

# Clase base para asociar todos los modelos a la misma base de datos
class BaseModel(Model):
    class Meta: database = database  # Asociar la base de datos configurada

class clientes(BaseModel):
    codigo_cli = SmallIntegerField(primary_key=True)
    nombre = CharField(max_length=20)
    localidad = CharField(max_length=15)
    tlf = CharField(max_length=10)

    class Meta:
        table_name = 'clientes'

class proveedores(BaseModel):
    codigo_prov = SmallIntegerField(primary_key=True)
    nombre = CharField()
    localidad = CharField()
    fecha_alta = DateTimeField()
    comision = FloatField()

    class Meta:
        table_name = 'proveedores'

class articulos(BaseModel):
    codarticulo = SmallIntegerField(primary_key=True)
    denominacion  = CharField()
    precio = FloatField()
    stock = SmallIntegerField()
    zona = CharField()
    codigo_prov = ForeignKeyField(proveedores, backref='articulos', column_name='codigo_prov')

    class Meta:
        table_name = 'articulos'

class compras(BaseModel):
    numcompra = SmallIntegerField(primary_key=True)
    fechacompra = DateTimeField()
    codigo_cli = ForeignKeyField(clientes, backref='compras', column_name='codigo_cli' )

    class Meta:
        table_name = 'compras'

# Modelo de detalle de compras
class detallecompras(BaseModel):
    numcompra = ForeignKeyField(compras, backref='detallecompras', column_name='numcompra')
    codarticulo = ForeignKeyField(articulos, backref='detallecompras', column_name='codarticulo')
    unidades = SmallIntegerField()

    class Meta:
        table_name = 'detallecompras'
        primary_key = CompositeKey('numcompra', 'codarticulo')




# Conectar a la base de datos
database.connect()

# Consulta para obtener los datos de los proveedores
query = proveedores.select()
print("\n1- Datos de los proveedores:")
for proveedor in query:
    print(
        "Código Proveedor: ", proveedor.codigo_prov,
        "Nombre: ", proveedor.nombre,
        "Localidad: ", proveedor.localidad,
        "Fecha Alta: ", proveedor.fecha_alta,
        "Comisión: ", proveedor.comision
    )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener los datos de los clientes y sus compras
query = (
    clientes
    .select()
    .join(compras, JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli))
)
print("\n2- Datos de los clientes y sus compras:")
for cliente in query:
    for compra in cliente.compras:
        print(
            "Código Cliente:", cliente.codigo_cli,
            "Nombre:", cliente.nombre,
            "Localidad:", cliente.localidad,
            "Teléfono:", cliente.tlf,
            "Número Compra:", compra.numcompra,
            "Fecha Compra:", compra.fechacompra
        )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener el detalle de compras por cliente
query = (
    clientes
    .select()
    .join(compras, JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli))
)
print("\n3- Datos de los clientes, sus compras, detalles de compras y precios de artículos:")
for cliente in query:
    for compra in cliente.compras:  # Relación de cliente con sus compras
        for detalle in compra.detallecompras:  # Relación de compra con sus detalles
            print(
                "Código Cliente:", cliente.codigo_cli,
                "Nombre:", cliente.nombre,
                "Localidad:", cliente.localidad,
                "Número Compra:", compra.numcompra,
                "Código Artículo:", detalle.codarticulo.codarticulo,
                "Unidades Compradas:", detalle.unidades,
                "Precio Artículo:", detalle.codarticulo.precio,
                "Importe:", detalle.unidades * detalle.codarticulo.precio
            )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener el total de compra de cada cliente
query = (
    clientes
    .select()
    .join(compras, JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli))
    .group_by(clientes.codigo_cli, compras.numcompra)
)
print("\n4- Total de compra por cliente:")
for cliente in query:
    for compra in cliente.compras:  # Relación de cliente con sus compras
        total_compra = 0
        for detalle in compra.detallecompras:  # Relación de compra con sus detalles
            total_compra+= detalle.unidades * detalle.codarticulo.precio
            print(
                "Código Cliente:", cliente.codigo_cli,
                "Nombre:", cliente.nombre,
                "Localidad:", cliente.localidad,
                "Número de Compra:", compra.numcompra,
                "Importe Total:", total_compra
            )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener el total de compra de cada cliente y el número de compras
query = (
    clientes
    .select()
    .join(compras, JOIN.LEFT_OUTER, on=(clientes.codigo_cli == compras.codigo_cli))
    .group_by(clientes.codigo_cli, compras.numcompra)
)
print("\n5- Total de compras por cada cliente:")
for cliente in query:
    for compra in cliente.compras:  # Relación de cliente con sus compras
        total_compra = 0
        numero_compras = 0
        for detalle in compra.detallecompras:  # Relación de compra con sus detalles
            numero_compras += 1
            total_compra+= detalle.unidades * detalle.codarticulo.precio
            print(
                "Código Cliente:", cliente.codigo_cli,
                "Nombre:", cliente.nombre,
                "Localidad:", cliente.localidad,
                "Telefono:", cliente.tlf,
                "Número de Compras:", numero_compras,
                "Importe Total:", total_compra
            )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener los datos de los artículos, sus compras y proveedores
query = (
    articulos
    .select()
    .join(detallecompras, JOIN.LEFT_OUTER, on=(articulos.codarticulo == detallecompras.codarticulo))
    .join(proveedores, JOIN.LEFT_OUTER, on=(articulos.codigo_prov == proveedores.codigo_prov))
)
print("\n6- Artículos, unidades compradas, importe y proveedor:")
for articulo in query:
    total_unidades = 0
    total_importe = 0

    # Iterar sobre los detalles de compras relacionados con el artículo
    for detalle in articulo.detallecompras:  # Relación de artículos con detalle de compras
        total_unidades += detalle.unidades
        total_importe += detalle.unidades * articulo.precio

    print(
        "Código Artículo:", articulo.codarticulo,
        "Denominación:", articulo.denominacion,
        "Stock:", articulo.stock,
        "Precio:", articulo.precio,
        "Unidades Compradas:", total_unidades,
        "Importe Total de Compras:", total_importe,
        "Proveedor:", articulo.codigo_prov.nombre if articulo.codigo_prov else "Sin Proveedor"
    )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener el total de compra de cada cliente y el número de compras
query = (
    proveedores
    .select()
    .join(articulos, JOIN.LEFT_OUTER, on=(proveedores.codigo_prov == articulos.codigo_prov))
    .group_by(proveedores.codigo_prov, articulos.denominacion)
)
print("\n7- Artículos suministrados por cada proveedor:")
for proveedor in query:
    for articulo in proveedor.articulos:  # Relación de cliente con sus compras
        print(
            "Código proveedor:", proveedor.codigo_prov,
            "Nombre:", proveedor.nombre,
            "Codigo Articulo:", articulo.codarticulo,
            "Denominacion:", articulo.denominacion
        )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener el número de artículos suministrados por cada proveedor
query = (
    proveedores
    .select(proveedores.codigo_prov, proveedores.nombre, fn.COUNT(articulos.codarticulo).alias('numero_articulos'))
    .join(articulos, JOIN.LEFT_OUTER, on=(proveedores.codigo_prov == articulos.codigo_prov))
    .group_by(proveedores.codigo_prov)
)
print("\n8- Número de artículos suministrados por cada proveedor:")
for proveedor in query:
    print(
        "Código Proveedor:", proveedor.codigo_prov,
        "Nombre:", proveedor.nombre,
        "Número de Artículos Suministrados:", proveedor.numero_articulos
    )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener clientes de Talavera que compraron artículos de la Zona A
query = (
    clientes
    .select(clientes.codigo_cli, clientes.nombre, clientes.localidad)
    .join(compras, JOIN.INNER, on=(clientes.codigo_cli == compras.codigo_cli))
    .join(detallecompras, JOIN.INNER, on=(compras.numcompra == detallecompras.numcompra))
    .join(articulos, JOIN.INNER, on=(detallecompras.codarticulo == articulos.codarticulo))
    .where((clientes.localidad == "Madrid") & (articulos.zona == "Zona A"))
)
print("\n9- Clientes de Madrid que compraron artículos de la Zona A:")
for cliente in query:
    print(
        "Código Cliente:", cliente.codigo_cli,
        "Nombre:", cliente.nombre,
        "Localidad:", cliente.localidad
    )
# -------------------------------------------------------------------------------------------------------------
# Consulta para obtener los proveedores que suministran artículos de la zona Centro
query = (
    proveedores
    .select(proveedores.codigo_prov, proveedores.nombre, proveedores.localidad)
    .join(articulos, JOIN.INNER, on=(proveedores.codigo_prov == articulos.codigo_prov))
    .where(articulos.zona == "Zona A")
)
print("\n10- Proveedores que suministran artículos de la Zona A:")
for proveedor in query:
    print(
        "Código Proveedor:", proveedor.codigo_prov,
        "Nombre:", proveedor.nombre,
        "Localidad:", proveedor.localidad
    )


# Obtener todas las compras con detalles de cliente, artículos y proveedor
query = (compras
    .select(
        compras.numcompra,
        compras.fechacompra,
        clientes.nombre.alias('cliente_nombre'),
        articulos.denominacion.alias('articulo_nombre'),
        articulos.precio,
        detallecompras.unidades,
        proveedores.nombre.alias('proveedor_nombre'),
        proveedores.localidad.alias('proveedor_localidad')
    )
    .join(clientes, on=(compras.codigo_cli == clientes.codigo_cli))  # Relación compras-clientes
    .switch(compras)
    .join(detallecompras, on=(compras.numcompra == detallecompras.numcompra))  # Relación compras-detallecompras
    .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo))  # Relación detallecompras-articulos
    .join(proveedores, on=(articulos.codigo_prov == proveedores.codigo_prov))  # Relación articulos-proveedores
)

# Mostrar resultados
for compra in query.dicts():
    print(compra)


# Obtener las compras realizadas por un cliente específico
codigo_cliente = 1

# Consulta para compras de un cliente
query = (compras
    .select(
        compras.numcompra,
        compras.fechacompra,
        detallecompras.unidades,
        articulos.denominacion.alias('articulo_nombre'),
        articulos.precio,
        proveedores.nombre.alias('proveedor_nombre')
    )
    .join(clientes, on=(compras.codigo_cli == clientes.codigo_cli))
    .switch(compras)
    .join(detallecompras, on=(compras.numcompra == detallecompras.numcompra))
    .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo))
    .join(proveedores, on=(articulos.codigo_prov == proveedores.codigo_prov))
    .where(clientes.codigo_cli == codigo_cliente)
)
# Mostrar resultados
for compra in query.dicts():
    print(compra)


# Listar todos los artículos con su proveedor y las unidades vendidas
query = (articulos
    .select(
        articulos.codarticulo,
        articulos.denominacion,
        articulos.precio,
        articulos.stock,
        proveedores.nombre.alias('proveedor_nombre'),
        proveedores.localidad.alias('proveedor_localidad'),
        fn.SUM(detallecompras.unidades).alias('total_unidades_vendidas')
    )
    .join(proveedores, on=(articulos.codigo_prov == proveedores.codigo_prov))
    .switch(articulos)
    .join(detallecompras, JOIN.LEFT_OUTER, on=(articulos.codarticulo == detallecompras.codarticulo))
    .group_by(articulos.codarticulo, proveedores.codigo_prov)
)

# Mostrar resultados
for articulo in query.dicts():
    print(articulo)


# Obtener el historial de compras y los detalles de un artículo específico
codigo_articulo = 101
# Consulta para el historial de compras de un artículo
historial_articulo = (detallecompras
    .select(
        compras.numcompra,
        compras.fechacompra,
        clientes.nombre.alias('cliente_nombre'),
        detallecompras.unidades,
        articulos.denominacion.alias('articulo_nombre'),
        proveedores.nombre.alias('proveedor_nombre')
    )
    .join(articulos, on=(detallecompras.codarticulo == articulos.codarticulo))
    .join(compras, on=(detallecompras.numcompra == compras.numcompra))
    .join(clientes, on=(compras.codigo_cli == clientes.codigo_cli))
    .join(proveedores, on=(articulos.codigo_prov == proveedores.codigo_prov))
    .where(articulos.codarticulo == codigo_articulo)
)

# Mostrar resultados
for detalle in historial_articulo.dicts():
    print(detalle)

# Consulta para proveedores y artículos con orden por comisión
proveedores_articulos = (proveedores
    .select(
        proveedores.nombre.alias('proveedor_nombre'),
        proveedores.comision,
        articulos.denominacion.alias('articulo_nombre'),
        articulos.precio
    )
    .join(articulos, on=(proveedores.codigo_prov == articulos.codigo_prov))
    .order_by(proveedores.comision.desc())
)

# Mostrar resultados
for proveedor in proveedores_articulos.dicts():
    print(proveedor)

# Cerrar la conexión
database.close()
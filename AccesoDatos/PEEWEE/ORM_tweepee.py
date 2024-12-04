from peewee import *
from datetime import datetime

# Configuración de la base de datos
DATABASE = 'tweepee.db'
database = SqliteDatabase(DATABASE)


# Base Model para usar la base de datos
class BaseModel(Model):
    class Meta:
        database = database


# Modelos
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    # Método para obtener los usuarios que este usuario sigue
    def following(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.to_user)
                .where(Relationship.from_user == self)
                .order_by(User.username))

    # Método para obtener los seguidores de este usuario
    def followers(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.from_user)
                .where(Relationship.to_user == self)
                .order_by(User.username))


# Modelo para las relaciones entre usuarios (muchos a muchos)
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')  # Usuario que sigue
    to_user = ForeignKeyField(User, backref='related_to')  # Usuario seguido

    class Meta:
        # Garantiza que no haya relaciones duplicadas
        indexes = (
            (('from_user', 'to_user'), True),
        )


class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()
    is_published = BooleanField(default=False)  # Nuevo campo con valor predeterminado False

# Modelo de favoritos (usuarios marcando mensajes como favoritos)
class Favorite(BaseModel):
    user = ForeignKeyField(User, backref='favorites')  # Usuario que marcó como favorito
    tweet = ForeignKeyField(Message, backref='favorites')  # Mensaje marcado como favorito


# ----------------------------------------------------------------------------------------------------------------------
# Insertar datos de muestra
def insert_data():
    # Crear usuarios
    user1 = User.create(username="alice", password="alicepass", email="alice@example.com", join_date=datetime.now())
    user2 = User.create(username="bob", password="bobpass", email="bob@example.com", join_date=datetime.now())
    user3 = User.create(username="charlie", password="charliepass", email="charlie@example.com", join_date=datetime.now())

    # Crear relaciones (seguidores)
    Relationship.create(from_user=user1, to_user=user2)  # Alice sigue a Bob
    Relationship.create(from_user=user2, to_user=user3)  # Bob sigue a Charlie
    Relationship.create(from_user=user3, to_user=user1)  # Charlie sigue a Alice

    # Crear mensajes
    msg1 = Message.create(user=user1, content="¡Hola, soy Alice!", pub_date=datetime.now(), is_published=True)
    msg2 = Message.create(user=user2, content="El primer mensaje de Bob", pub_date=datetime.now(), is_published=True)
    msg3 = Message.create(user=user3, content="¡Charlie está aquí!!", pub_date=datetime.now(), is_published=True)
    msg4 = Message.create(user=user1, content="El segundo mensaje de Alice", pub_date=datetime.now(), is_published=False)

    # Crear favoritos
    Favorite.create(user=user2, tweet=msg1)  # Bob marca como favorito el mensaje de Alice
    Favorite.create(user=user3, tweet=msg2)  # Charlie marca como favorito el mensaje de Bob
    Favorite.create(user=user1, tweet=msg3)  # Alice marca como favorito el mensaje de Charlie

# ----------------------------------------------------------------------------------------------------------------------
def ver_usuarios():
    print("\nUsuarios en la base de datos:")
    for user in User.select():
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Join Date: {user.join_date}")
# ----------------------------------------------------------------------------------------------------------------------
def ver_relaciones():
    print("\nRelaciones de usuarios:")
    for user in User.select():
        print(f"\nUsuario: {user.username}")
        print("  Sigue a:")
        for following in user.following():
            print(f"    {following.username}")
        print("  Seguidores:")
        for follower in user.followers():
            print(f"    {follower.username}")
# ----------------------------------------------------------------------------------------------------------------------
def ver_mensajes():
    print("\nMensajes publicados por los usuarios (ordenados de más nuevo a más viejo):")
    for user in User.select():
        print(f"\nMensajes de {user.username}:")
        messages = Message.select().where(Message.user == user).order_by(Message.pub_date.desc())
        for message in messages:
            print(f"  {message.pub_date}: {message.content}")
# ----------------------------------------------------------------------------------------------------------------------
def ver_favoritos():
    print("\nFavoritos en la base de datos:")
    query = (Favorite
             .select(Favorite, Message, User)
             .join(Message, on=(Favorite.tweet == Message.id))
             .join(User, on=(Message.user == User.id)))
    for favorite in query:
        print(f"Usuario que marcó como favorito: {favorite.user.username}, "
              f"Tweet: {favorite.tweet.content}, "
              f"Autor del Tweet: {favorite.tweet.user.username}")
# ----------------------------------------------------------------------------------------------------------------------
database.connect()

# Crear tablas si no existen
database.create_tables([User, Relationship, Message, Favorite])
insert_data()

ver_usuarios()
ver_relaciones()
ver_mensajes()
ver_favoritos()

database.close()


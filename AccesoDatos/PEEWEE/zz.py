from peewee import *
from datetime import datetime

DATABASE = 'tweepee.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField
    email = CharField()
    join_date = DateTimeField()

    def following(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.to_user)
                .where(Relationship.from_user==self)
                .order_by(User.username)
                )

    def followers(self):
        return(User
               .select()
               .join(Relationship,on=Relationship.from_user)
               .where(Relationship.to_user==self)
               .order_by(User.username)
               )

class Relationship(BaseModel):
    from_user=ForeignKeyField(User,backref='relationships')
    to_user=ForeignKeyField(User,backref='related_to')

    class Meta:
        indexes=(
            (('from_user', 'to_user'),True),
        )


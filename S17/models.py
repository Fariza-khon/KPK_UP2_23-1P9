from peewee import *

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    type_name = CharField(
        max_length=50,
        null=False,
        unique=True,
        index=True
    )

    class Meta:
        table_name = 'room_types'

class Room(BaseModel):
    room_number = CharField(
        max_length=20,
        null=False
    )
    floor = IntegerField(
        null=False,
        constraints=[Check('floor >= 1')]
    )
    building = CharField(
        max_length=50,
        null=False
    )
    capacity = IntegerField(
        null=False,
        constraints=[Check('capacity > 0')]
    )

    class Meta:
        table_name = 'rooms'
        indexes = (
            (('room_number', 'building', 'floor'), True),  # Составной уникальный индекс
        )

class RoomRoomType(BaseModel):
    room = ForeignKeyField(
        Room,
        field='id',
        backref='types',
        on_delete='CASCADE',
        null=False
    )
    room_type = ForeignKeyField(
        RoomType,
        field='id',
        backref='rooms',
        on_delete='CASCADE',
        null=False
    )

    class Meta:
        table_name = 'room_room_type'
        primary_key = CompositeKey('room', 'room_type')  # Составной первичный ключ
        indexes = (
            ('room_id',),
            ('room_type_id',)
        )

def init_db():
    db.connect()
    db.create_tables([RoomType, Room, RoomRoomType], safe=True)

if __name__ == '__main__':
    init_db()

from peewee import *

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    id = AutoField(primary_key=True)
    type_name = CharField(
        max_length=50,
        null=False,
        unique=True,
        index=True
    )

    class Meta:
        table_name = 'room_types'

class Room(BaseModel):
    id = AutoField(primary_key=True)
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
    is_active = BooleanField(
        null=False,
        default=True
    )

    class Meta:
        table_name = 'rooms'
        constraints = [SQL('UNIQUE(room_number, building)')]

class RoomRoomType(BaseModel):
    room = ForeignKeyField(
        Room,
        field='id',
        backref='room_types_link',
        on_delete='CASCADE',
        null=False,
        column_name='room_id'
    )
    room_type = ForeignKeyField(
        RoomType,
        field='id',
        backref='rooms_link',
        on_delete='CASCADE',
        null=False,
        column_name='room_type_id'
    )

    class Meta:
        table_name = 'room_room_type'
        primary_key = CompositeKey('room', 'room_type')
        indexes = (
            Index('idx_room_id', 'room'),
            Index('idx_room_type_id', 'room_type'),
        )

def init_db():
    db.connect()
    db.create_tables([RoomType, Room, RoomRoomType], safe=True)

if __name__ == '__main__':
    init_db()

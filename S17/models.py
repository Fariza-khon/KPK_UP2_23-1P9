from peewee import *

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    type_name = CharField(max_length=50, null=False, unique=True)

    class Meta:
        table_name = 'room_types'

class Room(BaseModel):
    room_number = CharField(max_length=20, null=False)
    floor = IntegerField(null=False)
    building = CharField(max_length=50, null=False)
    capacity = IntegerField(null=False)
    is_active = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'rooms'
        constraints = [SQL('UNIQUE(room_number, building)')]

class RoomRoomType(BaseModel):
    room = ForeignKeyField(Room, backref='room_types_link', on_delete='CASCADE', null=False)
    room_type = ForeignKeyField(RoomType, backref='rooms_link', on_delete='CASCADE', null=False)

    class Meta:
        table_name = 'room_room_type'
        primary_key = CompositeKey('room', 'room_type')

def init_db():
    db.connect()
    db.create_tables([RoomType, Room, RoomRoomType], safe=True)

if __name__ == '__main__':
    init_db()

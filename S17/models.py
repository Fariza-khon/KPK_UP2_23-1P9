from peewee import *
from typing import List
from playhouse.fields import ManyToManyField

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    type_name = CharField(max_length=50, null=False, unique=True)
    is_active = BooleanField(null=False, default=True)
    
    class Meta:
        table_name = 'room_types'
        
    def to_dict(self):
        return {
            'id': self.id,
            'type_name': self.type_name,
            'is_active': self.is_active
        }

class Room(BaseModel):
    room_number = CharField(max_length=20, null=False)
    floor = IntegerField(constraints=[Check('floor >= 1')], null=False)
    building = CharField(max_length=50, null=False)
    capacity = IntegerField(constraints=[Check('capacity > 0')], null=False)
    is_active = BooleanField(null=False, default=True)
    room_types = ManyToManyField(RoomType, backref='rooms', through='RoomRoomType')
    
    class Meta:
        table_name = 'rooms'
        constraints = [SQL('UNIQUE(room_number, building)')]
        
    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'floor': self.floor,
            'building': self.building,
            'capacity': self.capacity,
            'is_active': self.is_active,
            'types': [rt.room_type.to_dict() for rt in self.room_types.through.select()]
        }

class RoomRoomType(BaseModel):
    room = ForeignKeyField(Room, backref='room_types_link')
    room_type = ForeignKeyField(RoomType, backref='rooms_link')
    
    class Meta:
        table_name = 'room_room_type'
        indexes = (
            (('room', 'room_type'), True),
        )

# Обновленные методы работы с типами
def set_room_types(self, type_ids: List[int]):
    # Очищаем существующие связи
    self.room_types.through.filter(room=self).delete()
    
    # Добавляем новые связи
    for type_id in type_ids:
        room_type = RoomType.get_or_none(RoomType.id == type_id)
        if room_type:
            RoomRoomType.create(room=self, room_type=room_type)

def get_room_types(self):
    return [rt.room_type.to_dict() for rt in self.room_types.through.select()]

# Добавляем методы в класс Room
Room.set_room_types = set_room_types
Room.get_room_types = get_room_types

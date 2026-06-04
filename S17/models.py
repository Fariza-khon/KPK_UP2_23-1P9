from peewee import *
from typing import List

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

    class Meta:
        table_name = 'rooms'
        constraints = [SQL('UNIQUE(room_number, building)')]

    def get_types(self):
        """Получить все типы аудитории в виде списка RoomTypeResponse"""
        return [rt.room_type.to_dict() for rt in self.room_types_link]

    def set_types(self, type_ids: List[int]):
        """Установить типы аудитории по списку ID"""
        # Удаляем старые связи
        RoomRoomType.delete().where(RoomRoomType.room == self).execute()
        # Добавляем новые связи
        for type_id in type_ids:
            RoomType.get_or_none(RoomType.id == type_id)
            RoomRoomType.create(room=self, room_type_id=type_id)

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'floor': self.floor,
            'building': self.building,
            'capacity': self.capacity,

# Вариант № 17. Room Service (Сервис аудиторий)

## Модель RoomTypeResponse

Структура объекта типа аудитории в ответах API:

| Parameter | Description | Type |
|-----------|-------------|---------|
| id | ID типа аудитории | int |
| type_name | Название типа | str |
| is_active | Статус активности (при мягком удалении = False) | boolean |

---

## 1. Создание типа аудитории (create)

### Параметры для создания

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------|-----------|---------|--------------------------------------|----------|
| type_name | Название типа аудитории | Yes | str | Уникальное значение, min length 1, max length 50 | - |

**Unique combination:** `type_name` (должен быть уникальным).

### Информация после успешного создания

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |

---

## 2. Изменение типа аудитории по ID (change)

### Параметры для изменения

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|---------------------|-----------|---------|--------------------------------------|----------|
| type_name | Новое название типа | No | str | Уникальное значение, min length 1, max length 50 | - |

**Unique combination:** `type_name` (должен оставаться уникальным после изменения).

### Информация после успешного изменения

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |

---

## 3. Удаление типа аудитории по ID (delete)

* Реализуется **мягкое удаление** — поле `is_active` устанавливается в `False`.
* Возвращает **True**, если тип аудитории был успешно помечен как удалённый (is_active = False).
* Возвращает **False** в противном случае (например, если запись не найдена).

---

## 4. Получение типа аудитории по ID (get)

### Информация после успешного поиска

| Parameter | Description | Type |
|-----------|---------------------|---------|
| id | ID типа аудитории | int |
| type_name | Название типа | str |
| is_active | Статус активности (при мягком удалении = False) | boolean |

---

## 5. Получение списка типов аудитории (get list)

### Параметры для поиска

| Parameter | Description | Type |
|-----------|----------------------------|---------|
| type_name | Частичное совпадение названия | str |
| limit | Лимит количества записей | int |

### Информация после успешного поиска

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |

---

## 6. Создание аудитории (create)

### Параметры для создания

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------------------|-----------|---------|------------------------------|----------|
| room_number | Номер аудитории | Yes | str | - | Уникальное значение в комбинации с building |
| floor | Этаж | Yes | int | ≥ 1 | - |
| building | Корпус | Yes | str | - | - |
| capacity | Вместимость | Yes | int | > 0 | - |
| type_ids | Список ID типов | No | array of int | - | [] |
| is_active | Статус активности | No | boolean | - | True |

**Unique combination:** `(room_number, building)` — должна быть уникальной.

### Информация после успешного создания

| Parameter | Description | Type |
|-----------|-------------------------|---------|
| id | ID аудитории | int |
| room_number | Номер аудитории | str |
| floor | Этаж | int |
| building | Корпус | str |
| capacity | Вместимость | int |
| is_active | Статус активности | boolean |
| types | Типы аудитории | array of RoomTypeResponse |

---

## 7. Изменение аудитории по ID (change)

### Параметры для изменения

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------------------|-----------|---------|------------------------------|----------|
| room_number | Новый номер аудитории | No | str | Если указан, должен быть уникальным в комбинации с `building` | - |
| floor | Новый этаж | No | int | ≥ 1 | - |
| building | Новый корпус | No

erDiagram
    ROOM_TYPE {
        int id PK
        string type_name
        boolean is_active
    }

    ROOM {
        int id PK
        string room_number
        int floor
        string building
        int capacity
        boolean is_active
    }

    ROOM_ROOM_TYPE {
        int room_id PK,FK
        int type_id PK,FK
    }

    ROOM ||--o{ ROOM_ROOM_TYPE : id → room_id
    ROOM_TYPE ||--o{ ROOM_ROOM_TYPE : id → type_id


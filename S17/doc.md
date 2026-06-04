# Вариант № 17. Room Service (Сервис аудиторий)

## Модель RoomTypeResponse

Структура объекта типа аудитории в ответах API:

| Parameter | Description | Type |
|-----------|-------------|---------|
| id | ID типа аудитории | int |
| type_name | Название типа | str |
| is_active | Статус активности | boolean |
---

## 1. Создание типа аудитории (create)

### Parameters for creation

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------|-----------|---------|--------------------------------------|----------|
| type_name | Название типа аудитории | Yes | str | Уникальное значение, min length 1, max length 50 | - |

**Unique combination:** `type_name` (должен быть уникальным).

### Information after successful creation

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |

---

## 2. Изменение типа аудитории по ID (change)

### Parameters for change

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|---------------------|-----------|---------|--------------------------------------|----------|
| type_name | Новое название типа | No | str | Уникальное значение, min length 1, max length 50 | - |

**Unique combination:** `type_name` (должен оставаться уникальным после изменения).

### Information after successful change

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |

---

## 3. Удаление типа аудитории по ID (delete)

### Return Value

| Type |
|---------|
| boolean |

* **True** — тип аудитории успешно помечен как удалённый (is_active = False)
* **False** — запись не найдена или произошла ошибка

---

## 4. Получение типа аудитории по ID (get)

### Information after successful search

| Parameter | Description | Type |
|-----------|---------------------|---------|
| id | ID типа аудитории | int |
| type_name | Название типа | str |
| is_active | Статус активности | boolean |

---

## 5. Получение списка типов аудитории (get list)

### Search parameters

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|----------------------------|-----------|---------|----------------------|----------|
| type_name | Частичное совпадение названия | No | str | - | - |
| limit | Лимит количества возвращаемых записей | No | int | ≤ 100 | 10 |

### Information after successful search

| Parameter | Type |
|-----------|---------|
| id | int |
| type_name | str |
| is_active | boolean |
| total | int | # Общее количество записей |
| count | int | # Количество записей в текущей порции |

---

## 6. Создание аудитории (create)

### Parameters for creation

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------------------|-----------|---------|------------------------------|----------|
| room_number | Номер аудитории | Yes | str | - | Уникальное значение в комбинации с building |
| floor | Этаж | Yes | int | ≥ 1 | - |
| building | Корпус | Yes | str | - | - |
| capacity | Вместимость | Yes | int | > 0 | - |
| type_ids | Список ID типов | No | array of int | - | [] |
| is_active | Статус активности | No | boolean | - | True |

**Unique combination:** `(room_number, building)` — должна быть уникальной.

### Information after successful creation

| Parameter | Description | Type |
|-----------|-------------------------|---------|
| id | ID аудитории | int |
| room_number | Номер аудитории | str |
| floor | Этаж | int |
| building | Корпус | str |
| capacity | Вместимость | int |
| is_active | Статус активности | boolean |
| types | Типы аудитории (агрегированный результат из ROOM_ROOM_TYPE) | array of RoomTypeResponse |

---

## 7. Изменение аудитории по ID (change)

### Parameters for change

| Parameter | Description | Required | Type | Constraint | Default |
|-----------|-------------------------|-----------|---------|------------------------------|----------|
| room_number | Новый номер аудитории | No | str | Если указан, должен быть уникальным в комбинации с building | - |
| floor | Новый этаж | No | int | ≥ 1 | - |
| building | Новый корпус | No | str | Если указан, комбинация (room_number, building) должна быть уникальной | - |
| capacity | Новая вместимость | No | int | > 0 | - |
| type_ids | Новые ID типов (заменяют существующие связи) | No | array of int | - | - |
| is_active | Новый статус активности | No | boolean | - | - |

### Information after successful change

| Parameter | Type |
|-----------|---------|
| id | int |
| room_number | str |
| floor | int |
| building | str |
| capacity | int |
| is_active | boolean |
| types | array of RoomTypeResponse |


---
## ER‑диаграмма (Mermaid)

```mermaid
erDiagram
    ROOM_TYPE {
        int id PK
        string type_name
        boolean is_active
    }

    ROOM {
        int id PK
        string room_number
        string building
        int floor
        int capacity
        boolean is_active
    }
    
    { ROOM } {
        UNIQUE (room_number, building)
    }

    ROOM_ROOM_TYPE {
        int room_id PK, FK
        int type_id PK, FK
    }

    ROOM ||--o{ ROOM_ROOM_TYPE : id → room_id
    ROOM_TYPE ||--o{ ROOM_ROOM_TYPE : id → type_id

    NOTE RIGHT OF ROOM
        // Описание формирования связи
        Связь с типами аудитории осуществляется через таблицу ROOM_ROOM_TYPE
        Поле types в API формируется как агрегация связанных записей
    END NOTE






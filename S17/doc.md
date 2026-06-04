
## ER‑диаграмма (Mermaid)

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
        int room_id PK, FK
        int type_id PK, FK
    }

    ROOM ||--o{ ROOM_ROOM_TYPE : id → room_id
    ROOM_TYPE ||--o{ ROOM_ROOM_TYPE : id → type_id

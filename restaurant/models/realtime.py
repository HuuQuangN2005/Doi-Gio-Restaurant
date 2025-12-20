from datetime import datetime


class OrderStatus:
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELED = 4


class OrderDetail:
    def __init__(
        self,
        food_id: int,
        food_name: str,
        quantity: int,
        price: float,
        detail_status: int = OrderStatus.PENDING,
        note: str = "",
        order_id: str = None,
        detail_id: str = None,
    ):
        self.id = detail_id
        self.order_id = order_id
        self.food_id = food_id
        self.food_name = food_name
        self.quantity = quantity
        self.price = price
        self.note = note
        self.detail_status = detail_status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "food_id": self.food_id,
            "food_name": self.food_name,
            "quantity": self.quantity,
            "price": self.price,
            "detail_status": self.detail_status,
            "note": self.note,
            "subtotal": float(self.quantity * self.price),
        }


class Order:
    def __init__(
        self,
        table_id: int,
        employee_id: int,
        status: int = OrderStatus.PENDING,
        created_at: str = None,
        order_id: str = None,
    ):
        self.id = order_id
        self.table_id = table_id
        self.employee_id = employee_id
        self.status = status
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self):
        return {
            "table_id": self.table_id,
            "employee_id": self.employee_id,
            "status": self.status,
            "created_at": self.created_at,
        }

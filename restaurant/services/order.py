from typing import List, Dict, Any
from firebase_admin import db

from restaurant.models.realtime import Order, OrderDetail, OrderStatus
from restaurant.utils import Utils
from restaurant.services.product import product_service


class OrderService:
    def __init__(self):
        self.orders_ref = db.reference("orders")
        self.details_ref = db.reference("order_details")

    def create_order(self, table_id: int, employee_id: int) -> Order:
        return Order(table_id=table_id, employee_id=employee_id)

    def save_order(self, order: Order, items: List[OrderDetail]) -> bool:
        try:
            new_order_push = self.orders_ref.push(order.to_dict())
            order_id = new_order_push.key
            order.id = order_id

            for item in items:
                item.order_id = order_id
                self.details_ref.push(item.to_dict())

            return True
        except Exception as e:
            Utils.logger.error(f"OrderService: Save order error - {str(e)}")
            return False

    def add_order_detail(
        self, order_id: str, food_id: int, quantity: int, note: str = ""
    ) -> bool:
        try:
            food = product_service.get_food_by_id(food_id)
            if not food:
                return False

            new_detail = OrderDetail(
                food_id=food.id,
                food_name=food.name,
                quantity=quantity,
                price=food.price,
                note=note,
                order_id=order_id,
                detail_status=OrderStatus.PENDING,
            )

            self.details_ref.push(new_detail.to_dict())
            return True
        except Exception as e:
            Utils.logger.error(f"OrderService: Add detail error - {str(e)}")
            return False

    def get_order_details(
        self, order_id: str = None, status: int = None
    ) -> Dict[str, Any]:
        try:
            query_result = None
            if order_id is not None:
                query_result = (
                    self.details_ref.order_by_child("order_id").equal_to(order_id).get()
                )

            if status is not None:
                query_result = (
                    self.details_ref.order_by_child("detail_status")
                    .equal_to(status)
                    .get()
                )
            return query_result if query_result else {}
        except Exception as e:
            Utils.logger.error(f"OrderService: Query details error - {str(e)}")
            return {}

    def get_orders(self, order_id: str = None, id_ban: int = None) -> Dict[str, Any]:
        try:
            query_result = None
            if order_id is not None:
                query_result = (
                    self.orders_ref.order_by_child("order_id").equal_to(order_id).get()
                )

            if id_ban is not None:
                query_result = (
                    self.orders_ref.order_by_child("table_id")
                    .equal_to(int(id_ban))
                    .get()
                )
            return query_result if query_result else {}
        except Exception as e:
            Utils.logger.error(f"OrderService: Query details error - {str(e)}")
            return {}

    def update_detail_status(self, detail_id: str, new_status: int) -> bool:
        try:
            self.details_ref.child(detail_id).update({"detail_status": new_status})
            return True
        except Exception as e:
            Utils.logger.error(f"OrderService: Update detail status error - {str(e)}")
            return False

    def update_detail_note(self, detail_id: str, new_note: str) -> bool:
        try:
            self.details_ref.child(detail_id).update({"note": new_note})
            return True
        except Exception as e:
            Utils.logger.error(f"OrderService: Update detail status error - {str(e)}")
            return False

    def delete_order(self, order_id: str) -> bool:
        try:
            self.orders_ref.child(order_id).delete()

            details = (
                self.details_ref.order_by_child("order_id").equal_to(order_id).get()
            )
            if details:
                for d_id in details.keys():
                    self.details_ref.child(d_id).delete()
            return True

        except Exception as e:
            Utils.logger.error(f"OrderService: Delete order error - {str(e)}")
            return False

    def delete_order_detail(self, order_detail_id: str) -> bool:
        try:
            self.details_ref.child(order_detail_id).delete()
            return True

        except Exception as e:
            Utils.logger.error(f"OrderService: Delete order error - {str(e)}")
            return False


order_service = OrderService()

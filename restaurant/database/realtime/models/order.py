from restaurant.database.realtime.models import FirebaseModel
from datetime import datetime
from restaurant.utils import Utils


class TableReservation(FirebaseModel):
    FIREBASE_NODE = "table_reservations"

    def __init__(
        self, customer_name, email, phone, date, time, party_size, note="", key=None
    ):
        date_time_str = f"{date} {time}"

        dt_object = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")

        localized_dt = Utils.TIMEZONE.localize(dt_object)
        datetime = localized_dt.isoformat()

        super().__init__(
            key=key,
            customer_name=customer_name,
            phone=phone,
            email=email,
            party_size=party_size,
            note=note,
            datetime = datetime,
            status="pending",
        )

from typing import Dict, Any, Optional, Callable

from src.client.odoo_client import OdooClient


class SaleOrderExtractor:

    FIELDS = [
        "id",
        "name",
        "partner_id",
        "date_order",
        "state",
        "amount_total",
        "create_date",
        "write_date",
    ]

    def __init__(self):

        self.client = OdooClient()

    def extract(
        self,
        last_write_date: Optional[str] = None,
        batch_size: int = 100,
        batch_handler: Optional[
            Callable[[list[Dict[str, Any]]], None]
        ] = None,
    ):

        domain = []

        if last_write_date:

            domain.append(
                ["write_date", ">", last_write_date]
            )

        return self.client.search_read_all(
            model="sale.order",
            domain=domain,
            fields=self.FIELDS,
            batch_size=batch_size,
            batch_handler=batch_handler,
        )
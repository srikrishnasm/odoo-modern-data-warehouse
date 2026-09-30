from src.client.odoo_client import OdooClient


class CustomerExtractor:

    def __init__(self):
        self.client = OdooClient()

    def extract(
        self,
        batch_size=100,
        batch_handler=None,
        last_write_date=None,
    ):

        fields = [
            "id",
            "name",
            "email",
            "phone",
            "create_date",
            "write_date",
        ]

        domain = []

        if last_write_date:
            domain.append(
                ("write_date", ">", last_write_date)
            )

            print(
                f"Incremental extraction from: "
                f"{last_write_date}"
            )
        else:
            print("Full extraction")

        return self.client.search_read_all(
            model="res.partner",
            fields=fields,
            domain=domain,
            batch_size=batch_size,
            batch_handler=batch_handler,
        )
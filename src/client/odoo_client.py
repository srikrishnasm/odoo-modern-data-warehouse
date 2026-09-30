import requests

from config.settings import ODOO_URL, ODOO_API_KEY


class OdooClient:
    """
    Client for communicating with Odoo JSON-2 API.
    """

    def __init__(self):
        self.base_url = ODOO_URL

        self.headers = {
            "Authorization": f"bearer {ODOO_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "odoo-data-extractor/1.0",
        }

        self.timeout = 60

    def search_read(
        self,
        model,
        fields,
        domain=None,
        offset=0,
        limit=10,
    ):
        if domain is None:
            domain = []

        url = f"{self.base_url}/json/2/{model}/search_read"

        payload = {
            "domain": domain,
            "fields": fields,
            "offset": offset,
            "limit": limit,
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.exceptions.HTTPError as error:
            print(f"Odoo API HTTP error: {response.status_code}")
            print(response.text)
            raise error

        except requests.exceptions.RequestException as error:
            print(f"Odoo API request failed: {error}")
            raise error

        return response.json()
    
    def search_read_all(
        self,
        model,
        fields,
        domain=None,
        batch_size=100,
        batch_handler=None,
    ):
        if domain is None:
            domain = []

        all_records = []
        offset = 0
        max_write_date = None

        while True:

            print(
                f"Fetching {model}: "
                f"offset={offset}, limit={batch_size}"
            )

            records = self.search_read(
                model=model,
                fields=fields,
                domain=domain,
                offset=offset,
                limit=batch_size,
            )

            if not records:
                break

            print(f"Fetched {len(records)} records")

            # Find latest write_date
            for record in records:
                write_date = record.get("write_date")

                if write_date:
                    if (
                        max_write_date is None
                        or write_date > max_write_date
                    ):
                        max_write_date = write_date

            if batch_handler:
                batch_handler(records)
            else:
                all_records.extend(records)

            if len(records) < batch_size:
                break

            offset += batch_size

        if batch_handler:
            print("Extraction completed")

            return max_write_date

        print(
            f"Total records extracted from {model}: "
            f"{len(all_records)}"
        )

        return all_records, max_write_date
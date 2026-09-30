select
    product_id,
    product_name,
    product_code,
    list_price,
    create_date,
    write_date
from {{ ref('stg_product') }}
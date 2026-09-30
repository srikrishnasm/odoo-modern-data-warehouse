select
    date_trunc('month', date_order) as sales_month,
    count(distinct order_id) as total_orders

from {{ ref('stg_sale_order') }}

where state in ('sale', 'done')

group by
    date_trunc('month', date_order)

order by
    sales_month
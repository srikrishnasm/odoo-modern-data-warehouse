with customer_revenue as (
    select
        customer_id,
        customer_name,
        total_orders,
        total_revenue,
        average_order_value
    from {{ ref('customer_revenue') }}
)

select
    customer_id,
    customer_name,
    total_orders,
    total_revenue,
    average_order_value,
    row_number() over (
        order by total_revenue desc
    ) as revenue_rank
from customer_revenue
order by total_revenue desc
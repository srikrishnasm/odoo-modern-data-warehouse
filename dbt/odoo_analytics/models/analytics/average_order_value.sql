select
    count(distinct order_id) as total_orders,
    sum(amount_total) as total_revenue,
    round(
        sum(amount_total) / nullif(count(distinct order_id), 0),
        2
    ) as average_order_value

from {{ ref('fact_sales') }}

where state in ('sale', 'done')
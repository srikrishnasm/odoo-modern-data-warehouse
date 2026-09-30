select
    f.product_id,
    p.product_name,

    sum(f.quantity) as total_quantity,
    count(distinct f.sale_order_id) as total_orders,
    sum(f.line_subtotal) as total_revenue,
    avg(f.unit_price) as average_unit_price

from {{ ref('fact_sales_line') }} f

inner join {{ ref('dim_products') }} p
    on f.product_id = p.product_id

where f.state in ('sale', 'done')

group by
    f.product_id,
    p.product_name
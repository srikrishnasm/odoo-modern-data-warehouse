select
    sol.sale_order_line_id,
    sol.sale_order_id,
    sol.product_id,

    so.customer_id,
    so.date_order,
    so.state,

    sol.quantity,
    sol.unit_price,
    sol.line_subtotal,

    sol.create_date,
    sol.write_date

from {{ ref('stg_sale_order_line') }} sol

inner join {{ ref('stg_sale_order') }} so
    on sol.sale_order_id = so.order_id
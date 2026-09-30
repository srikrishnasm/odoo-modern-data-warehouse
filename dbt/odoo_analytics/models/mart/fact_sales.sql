with sales_orders as (

    select
        order_id,
        order_name,
        customer_id,
        date_order,
        state,
        amount_total,
        create_date,
        write_date
    from {{ ref('stg_sale_order') }}

)

select
    order_id,
    order_name,
    customer_id,
    date_order,
    state,
    amount_total,
    create_date,
    write_date
from sales_orders
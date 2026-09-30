with source as (

    select
        id,
        order_id,
        product_id,
        product_uom_qty,
        price_unit,
        price_subtotal,
        create_date,
        write_date
    from {{ source('odoo', 'sale_order_line') }}

),

deduplicated as (

    select
        id,
        order_id,
        product_id,
        product_uom_qty,
        price_unit,
        price_subtotal,
        create_date,
        write_date,

        row_number() over (
            partition by id
            order by write_date desc
        ) as rn

    from source

)

select
    id as sale_order_line_id,
    order_id as sale_order_id,
    product_id,
    product_uom_qty as quantity,
    price_unit as unit_price,
    price_subtotal as line_subtotal,
    create_date,
    write_date

from deduplicated

where rn = 1
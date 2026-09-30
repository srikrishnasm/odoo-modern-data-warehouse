with source as (

    select
        id,
        name,
        partner_id,
        date_order,
        state,
        amount_total,
        create_date,
        write_date
    from {{ source('odoo', 'sale_order') }}

),

deduplicated as (

    select
        id,
        name,
        partner_id,
        date_order,
        state,
        amount_total,
        create_date,
        write_date,

        row_number() over (
            partition by id
            order by write_date desc
        ) as rn

    from source

),

cleaned as (

    select
        id as order_id,
        name as order_name,
        partner_id as customer_id,
        date_order,
        state,
        amount_total,
        create_date,
        write_date
    from deduplicated
    where rn = 1

)

select *
from cleaned
with source as (

    select
        id,
        name,
        default_code,
        list_price,
        create_date,
        write_date
    from {{ source('odoo', 'product') }}

),

deduplicated as (

    select
        id,
        name,
        default_code,
        list_price,
        create_date,
        write_date,

        row_number() over (
            partition by id
            order by write_date desc
        ) as rn

    from source

)

select
    id as product_id,
    trim(name) as product_name,
    nullif(trim(default_code), '') as product_code,
    list_price,
    create_date,
    write_date

from deduplicated

where rn = 1
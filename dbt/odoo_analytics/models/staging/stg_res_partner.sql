with source as (

    select
        id,
        name,
        email,
        phone,
        create_date,
        write_date
    from {{ source('odoo', 'res_partner') }}

),

deduplicated as (

    select
        id,
        name,
        email,
        phone,
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
        id as customer_id,

        trim(name) as customer_name,

        nullif(trim(email), '') as email,

        nullif(trim(phone), '') as phone,

        create_date,
        write_date

    from deduplicated

    where rn = 1

)

select *
from cleaned
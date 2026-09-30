with customers as (

    select
        customer_id,
        customer_name,
        email,
        phone,
        create_date,
        write_date
    from {{ ref('stg_res_partner') }}

)

select
    customer_id,
    customer_name,
    email,
    phone,
    create_date,
    write_date

from customers
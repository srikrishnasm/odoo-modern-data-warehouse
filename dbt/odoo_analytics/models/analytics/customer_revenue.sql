with sales as (

    select
        customer_id,
        amount_total
    from {{ ref('fact_sales') }}
    where state in ('sale', 'done')

),

customer_revenue as (

    select
        customer_id,
        count(*) as total_orders,
        sum(amount_total) as total_revenue,
        avg(amount_total) as average_order_value
    from sales
    group by customer_id

)

select
    c.customer_id,
    c.customer_name,
    c.email,
    r.total_orders,
    r.total_revenue,
    r.average_order_value

from customer_revenue r

left join {{ ref('dim_customers') }} c
    on r.customer_id = c.customer_id
with sales as (

    select
        date_order,
        amount_total
    from {{ ref('fact_sales') }}
    where state in ('sale', 'done')

),

monthly_sales as (

    select
        date_trunc('month', date_order) as sales_month,
        count(*) as total_orders,
        sum(amount_total) as total_revenue,
        avg(amount_total) as average_order_value

    from sales

    group by 1

)

select
    sales_month,
    total_orders,
    total_revenue,
    average_order_value

from monthly_sales
order by sales_month
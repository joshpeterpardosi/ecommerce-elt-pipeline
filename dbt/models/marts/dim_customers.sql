select
    c.customer_unique_id,
    count(distinct o.order_id) as order_count,
    any_value(c.zip_code_prefix) as zip_code_prefix,
    any_value(c.city) as city,
    any_value(c.state) as state
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o on o.customer_id = c.customer_id
group by c.customer_unique_id

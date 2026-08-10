select
    order_id,
    sum(cast(price as numeric)) as total_price,
    sum(cast(freight_value as numeric)) as total_freight,
    count(*) as item_count,
    count(distinct seller_id) as distinct_seller_count
from {{ source('raw', 'order_items') }}
group by order_id

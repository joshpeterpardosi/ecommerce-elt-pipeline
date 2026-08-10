select
    order_id,
    customer_id,
    order_status,
    order_purchased_at,
    order_approved_at,
    order_delivered_carrier_at,
    order_delivered_customer_at,
    order_estimated_delivery_at,
    case
        when order_delivered_customer_at is null then null
        else date_diff(
            date(order_delivered_customer_at),
            date(order_estimated_delivery_at),
            day
        )
    end as delivery_delay_days
from {{ ref('stg_orders') }}

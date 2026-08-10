select
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchased_at,
    o.order_approved_at,
    o.order_delivered_carrier_at,
    o.order_delivered_customer_at,
    o.order_estimated_delivery_at,
    case
        when o.order_delivered_customer_at is null then null
        else date_diff(
            date(o.order_delivered_customer_at),
            date(o.order_estimated_delivery_at),
            day
        )
    end as delivery_delay_days,
    oi.total_price,
    oi.total_freight,
    oi.item_count,
    oi.distinct_seller_count,
    p.total_payment_value,
    p.max_installments,
    p.payment_types,
    p.payment_type_count
from {{ ref('stg_orders') }} o
left join {{ ref('stg_customers') }} c on c.customer_id = o.customer_id
left join {{ ref('stg_order_items') }} oi on oi.order_id = o.order_id
left join {{ ref('stg_payments') }} p on p.order_id = o.order_id

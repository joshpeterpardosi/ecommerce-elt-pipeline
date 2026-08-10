select
    order_id,
    sum(cast(payment_value as numeric)) as total_payment_value,
    max(cast(payment_installments as int64)) as max_installments,
    array_agg(distinct payment_type order by payment_type) as payment_types,
    count(distinct payment_type) as payment_type_count
from {{ source('raw', 'order_payments') }}
group by order_id

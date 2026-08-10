with primary_product as (
    select
        order_id,
        product_id
    from {{ source('raw', 'order_items') }}
    qualify row_number() over (
        partition by order_id
        order by cast(price as numeric) desc, order_item_id
    ) = 1
)

select
    f.order_id,
    f.customer_unique_id,
    f.order_status,
    f.delivery_delay_days,
    f.total_price as price,
    f.total_freight as freight,
    f.item_count,
    f.distinct_seller_count,
    f.total_payment_value,
    f.max_installments,
    f.payment_types,
    f.payment_type_count,
    dc.order_count as customer_order_count,
    dp.product_category_name,
    dp.product_weight_g,
    dp.product_length_cm,
    dp.product_height_cm,
    dp.product_width_cm,
    r.review_score
from {{ ref('fct_orders') }} f
left join {{ ref('dim_customers') }} dc on dc.customer_unique_id = f.customer_unique_id
left join primary_product pp on pp.order_id = f.order_id
left join {{ ref('dim_products') }} dp on dp.product_id = pp.product_id
left join {{ ref('stg_order_reviews') }} r on r.order_id = f.order_id

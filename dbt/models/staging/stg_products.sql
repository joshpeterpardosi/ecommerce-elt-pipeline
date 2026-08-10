select
    p.product_id,
    t.product_category_name_english as product_category_name,
    cast(p.product_name_lenght as int64) as product_name_length,
    cast(p.product_description_lenght as int64) as product_description_length,
    cast(p.product_photos_qty as int64) as product_photos_qty,
    cast(p.product_weight_g as numeric) as product_weight_g,
    cast(p.product_length_cm as numeric) as product_length_cm,
    cast(p.product_height_cm as numeric) as product_height_cm,
    cast(p.product_width_cm as numeric) as product_width_cm
from {{ source('raw', 'products') }} p
left join {{ source('raw', 'product_category_name_translation') }} t
    on p.product_category_name = t.product_category_name

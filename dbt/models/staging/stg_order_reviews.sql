select
    order_id,
    review_id,
    cast(review_score as int64) as review_score,
    review_comment_title,
    review_comment_message,
    cast(review_creation_date as timestamp) as review_created_at,
    cast(review_answer_timestamp as timestamp) as review_answered_at
from {{ source('raw', 'order_reviews') }}
qualify row_number() over (
    partition by order_id
    order by cast(review_creation_date as timestamp) desc, review_id
) = 1

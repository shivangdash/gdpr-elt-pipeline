select
    o.order_id,
    o.customer_id,
    o.order_total,
    o.ordered_at,
    c.created_at as customer_created_at
from {{ source('raw', 'orders') }} o
join {{ ref('stg_customer_data') }} c
    on o.customer_id = c.customer_id

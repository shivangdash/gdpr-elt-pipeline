select
    order_id,
    customer_id,
    order_total,
    ordered_at
from {{ ref('int_customer_orders') }}

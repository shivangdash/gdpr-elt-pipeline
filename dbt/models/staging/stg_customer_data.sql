with source as (
    select
        customer_id,
        name,
        email,
        phone,
        ssn,
        address,
        created_at
    from {{ source('raw', 'customer_data') }}
)

select * from source

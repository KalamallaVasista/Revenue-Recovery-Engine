SELECT 
    transaction_id,
    customer_id,
    CAST(payment_date AS DATE) AS payment_date,
    amount
FROM {{ source('raw_data', 'raw_transactions') }}
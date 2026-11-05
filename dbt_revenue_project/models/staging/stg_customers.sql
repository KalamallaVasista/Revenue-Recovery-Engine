SELECT 
    customer_id,
    CAST(signup_date AS DATE) AS signup_date,
    plan_tier,
    is_churned,
    monthly_fee
FROM {{ source('raw_data', 'raw_customers') }}
WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

transactions AS (
    SELECT 
        customer_id,
        SUM(amount) AS lifetime_value,
        MAX(payment_date) AS last_payment_date
    FROM {{ ref('stg_transactions') }}
    GROUP BY customer_id
),

tickets AS (
    SELECT 
        customer_id,
        COUNT(ticket_id) AS total_tickets,
        ROUND(AVG(frustration_score), 1) AS avg_frustration_score
    FROM {{ ref('stg_tickets') }}
    GROUP BY customer_id
)

SELECT 
    c.customer_id,
    c.signup_date,
    c.plan_tier,
    c.is_churned,
    c.monthly_fee,
    COALESCE(t.lifetime_value, 0) AS lifetime_value,
    t.last_payment_date,
    COALESCE(ti.total_tickets, 0) AS total_support_tickets,
    COALESCE(ti.avg_frustration_score, 0) AS avg_frustration_score,
    CASE 
        WHEN c.is_churned = 1 THEN 'Already Churned'
        WHEN COALESCE(ti.avg_frustration_score, 0) >= 7.0 THEN 'High Risk'
        WHEN COALESCE(ti.avg_frustration_score, 0) >= 4.0 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS churn_risk_segment
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
LEFT JOIN tickets ti ON c.customer_id = ti.customer_id
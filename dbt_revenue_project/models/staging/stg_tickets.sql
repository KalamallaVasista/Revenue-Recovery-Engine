SELECT 
    ticket_id,
    customer_id,
    CAST(ticket_date AS DATE) AS ticket_date,
    ticket_text,
    frustration_score
FROM {{ source('raw_data', 'raw_tickets') }}
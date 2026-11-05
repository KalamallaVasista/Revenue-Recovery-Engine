import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

os.makedirs('data', exist_ok=True)
np.random.seed(42)
num_customers = 1000
customer_ids = range(1001, 1001 + num_customers)

customers = pd.DataFrame({
    'customer_id': customer_ids,
    'signup_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700)) for _ in range(num_customers)],
    'plan_tier': np.random.choice(['Basic', 'Pro', 'Enterprise'], num_customers, p=[0.5, 0.3, 0.2]),
    'is_churned': np.random.choice([0, 1], num_customers, p=[0.75, 0.25])
})
tier_pricing = {'Basic': 29, 'Pro': 99, 'Enterprise': 299}
customers['monthly_fee'] = customers['plan_tier'].map(tier_pricing)

transactions = []
for _, row in customers.iterrows():
    num_months = random.randint(1, 6) if row['is_churned'] == 1 else random.randint(6, 24)
    for i in range(num_months):
        payment_date = row['signup_date'] + timedelta(days=30 * i)
        transactions.append({
            'transaction_id': f"TXN-{random.randint(100000, 999999)}",
            'customer_id': row['customer_id'],
            'payment_date': payment_date.strftime('%Y-%m-%d'),
            'amount': row['monthly_fee']
        })
transactions_df = pd.DataFrame(transactions)

analyzer = SentimentIntensityAnalyzer()
ticket_texts = [
    "Absolutely love the new dashboard update!",
    "The platform is too slow, I am losing money.",
    "How do I reset my password?",
    "Horrible customer service, canceling my account.",
    "Works fine, no issues so far.",
    "Billing is incorrect for the third month in a row!",
    "Great tool but a bit expensive."
]

tickets = pd.DataFrame({
    'ticket_id': range(5001, 5001 + 1500),
    'customer_id': np.random.choice(customer_ids, 1500),
    'ticket_date': [(datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(1500)],
    'ticket_text': np.random.choice(ticket_texts, 1500)
})

def calculate_frustration(text):
    score = analyzer.polarity_scores(text)['compound']
    return round(((1 - score) / 2) * 9 + 1, 1)

tickets['frustration_score'] = tickets['ticket_text'].apply(calculate_frustration)

customers.to_csv('data/raw_customers.csv', index=False)
transactions_df.to_csv('data/raw_transactions.csv', index=False)
tickets.to_csv('data/raw_tickets.csv', index=False)

print("✅ Success: Datasets generated in the /data folder.")
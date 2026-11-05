import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# 1. Safely encode the password to handle the '@' symbol
password = urllib.parse.quote_plus("Reddy@9441")

# 2. Connect using the encoded password
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/revenue_recovery")

try:
    print("Reading CSV files...")
    df_customers = pd.read_csv('data/raw_customers.csv')
    df_transactions = pd.read_csv('data/raw_transactions.csv')
    df_tickets = pd.read_csv('data/raw_tickets.csv')

    print("Uploading Customers to MySQL...")
    df_customers.to_sql('raw_customers', con=engine, if_exists='replace', index=False)

    print("Uploading Transactions to MySQL...")
    df_transactions.to_sql('raw_transactions', con=engine, if_exists='replace', index=False)

    print("Uploading Tickets to MySQL...")
    df_tickets.to_sql('raw_tickets', con=engine, if_exists='replace', index=False)

    print("✅ Success: All data loaded into MySQL!")

except Exception as e:
    print(f"❌ An error occurred: {e}")
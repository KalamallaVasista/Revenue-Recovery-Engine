# 🚀 Revenue Recovery & Churn Risk Engine

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)<img width="606" height="341" alt="Screenshot 2026-11-07 133912" src="https://github.com/user-attachments/assets/b224ae72-75ad-4c2e-8a49-57e68dbe4bc2" />

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📌 Executive Summary
The **Revenue Recovery & Churn Risk Engine** is an end-to-end analytical pipeline designed to identify at-risk monthly recurring revenue (MRR) and provide business leaders with actionable retention strategies. By mapping customer frustration signals and support ticket volume, this tool segments high-risk accounts and features a dynamic "What-If" simulator to forecast the exact ROI of offering targeted retention discounts.

## 🏗️ Architecture & Data Pipeline
This project utilizes a modern data stack approach, transforming raw operational data into a highly optimized dimensional model for business intelligence.

* **Data Generation:** Python scripts generate highly realistic, relational customer transaction and support ticket datasets.
* **Data Warehouse:** Hosted locally on a MySQL database.
* **Data Transformation (dbt Core):** Modular staging views clean and cast raw data, feeding into a final dimensional data mart (`fct_customer_risk`) that calculates dynamic Lifetime Value (LTV) and categorizes accounts into Churn Risk Segments.
* **Data Visualization (Power BI):** Direct connection to the data mart utilizing custom DAX measures for real-time scenario simulation.

## 📊 Key Dashboard Features
* **Dynamic 'What-If' Revenue Simulator:** Empowers account managers to input a proposed discount percentage, instantly calculating the **Projected Revenue Saved** versus the **Offer Investment Cost** using complex DAX parameters.
* **Behavioral Churn Mapping:** Correlates Support Ticket Volume with Customer Frustration Scores to identify "Danger Zone" customer segments across different subscription tiers.
* **Actionable Outreach Target Matrix:** A strictly filtered, row-level dataset of High and Medium risk customers, allowing the marketing team to immediately export the list for targeted discount campaigns.

## 💻 Core DAX Logic Highlight
To enable the interactive simulation, the dashboard relies on decoupled parameter tables and calculated measures:

```dax
-- Calculating the Cost of the Proposed Discount
Offer Investment Cost = 
[At-Risk Revenue (MRR)] - [Projected Revenue Saved]

-- Dynamically filtering the target audience
At-Risk Customers = 
CALCULATE(
    COUNT('revenue_recovery fct_customer_risk'[customer_id]),
    'revenue_recovery fct_customer_risk'[churn_risk_segment] IN {"High Risk", "Medium Risk"}
)




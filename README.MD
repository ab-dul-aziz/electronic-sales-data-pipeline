# **Electronic Sales Data Analysis Pipeline**
An end-to-end data pipeline for analyzing electonics sales using PostgreSQL, Apache Airflow, Elasticsearch, and Kibana.


## **Table of Contents**
1. [Introduction](#introduction)
2. [Data Overview](#data-overview)
3. [Problem Breakdown](#problem-breakdown)
4. [Methodology](#methodology)
7. [Conclusion](#conclusion)
8. [Recommendations](#recommendations)
9. [About Me](#about-me)


## **Introduction**
The company aims to analyze annual electronics sales data to gain deeper insights. As part of this initiative, an automated process will be implemented from end-to-end process using Airflow. First, raw data will be store into a database (PostgreSQL). The data will then be retrieved from the database, cleaned, and posted to Elasticsearch for further processing. Finally, the results of the data analysis will be visualized using Kibana to enable faster and more accurate data-driven decision-making.


## **Data Overview**
This dataset obtained from [Kaggle](https://www.kaggle.com/datasets/cameronseamons/electronic-sales-sep2023-sep2024) and contains comprehensive customer behaviour.

Here's a summary of the columns in the dataset.

Column              | Description
------------------- | ---------------
Customer ID         | Unique identifier for each customer.
Age                 | Age of the customer (numeric)
Gender              | Gender of the customer (Male or Female)
Loyalty Member      | (Yes/No)
Product Type        | Type of electronic product sold (e.g., Smartphone, Laptop, Tablet)
SKU                 | a unique code for each product.
Rating              | Customer rating of the product (1-5 stars) (Should have no Null Ratings)
Order Status        | Status of the order (Completed, Cancelled)
Payment Method      | Method used for payment (e.g., Cash, Credit Card, Paypal)
Total Price         | Total price of the transaction (numeric)
Unit Price          | Price per unit of the product (numeric)
Quantity            | Number of units purchased (numeric)
Purchase Date       | Date of the purchase (format : YYYY-MM-DD)
Shipping Type       | Type of shipping chosen (e.g., Standard, Overnight, Express)
Add-ons Purchased   | List of any additional items purchased (e.g., Accessories, Extended Warranty)
Add-on Total        | Total price of add-ons purchased (numeric)


## **Problem Breakdown**
- What is the sales trend from September 2023 to September 2024?
- Which electronic products are the most popular?
- What is the sales trend for each product category from September 2023 to September 2024?
- Which age group constitutes the largest customer base?
- How significant is the company’s revenue from customers registered as members?
- Has the company met its sales target for this year?
- What is the company's reputation among customers based on the NPS score?
- Which shipping method is most commonly used by customers?
- How many orders have been canceled by customers?


## **Methodology**
The methodology consists of the following steps:

1. **Input Data to PostgreSQL**: Initial data storage in PostgreSQL.
2. **ETL with Apache Airflow**: Airflow DAGs handle data extraction, transformation, and loading processes.
3. **Data Cleaning**: Essential cleaning performed within Airflow with validation checks.
4. **Loading to Elasticsearch**: Cleaned data is pushed to Elasticsearch for indexing.
5. **Visualization with Kibana**: Dashboards created in Kibana for data exploration and analysis.


## **Conclusion**
- **Revenue Growth**:
    - Significant revenue growth in early 2024 driven by marketing strategies and new product launches.
    - Smartphones contributed the most to sales, followed by smartwatches and laptops, while headphones had the lowest sales.

- **Customer Segments**:
    - Non-members accounted for the majority of sales, highlighting an opportunity to increase customer membership.
    - Only 21% of total revenue came from members, showing reliance on non-members and potential for loyalty growth.

- **Product Trends**:
    - Smartphones and laptops appeal to broader consumer segments due to their daily necessity.
    - Accessories like headphones have shorter lifespans and are more trend-dependent.

- **Marketing Strategies**:
    - Cross-selling and product bundling (e.g., laptop + mouse, smartphone + tempered glass) are recommended to boost sales momentum.

- **Customer Satisfaction**:
    - Despite exceeding the sales target by 108%, the Net Promoter Score (NPS) is low (0.19%), indicating dissatisfaction.
    - Improving product quality and customer service is critical to enhance satisfaction and reduce churn.


## Recommendations
- **Marketing Strategy**: The company should concentrate its marketing efforts on high-potential segments, such as health and wellness products for the elderly, or solutions that support professional and educational needs.
- **Loyalty Enhancement**: Strengthen customer relationships to foster loyalty and attract new members.
- **Transaction Experience Optimization**: Identify the underlying causes of transaction cancellations and implement strategies to resolve these issues effectively.
- **Shipping Strategy**: Introduce shipping discounts to incentivize customer purchases and increase overall sales volume.

## **About Me**
Abdul Aziz <br>
LinkedIn: [Abdul Aziz](https://www.linkedin.com/in/abdul-aziz-data-enthusiast/)



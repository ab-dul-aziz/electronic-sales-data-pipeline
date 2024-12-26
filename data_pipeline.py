'''
=================================================
This program is designed to automate the process of fetching data from PostgreSQL, performing data cleaning, and posting the cleaned data to Elasticsearch. The dataset used pertains to electronics sales over the course of one year, from September 2023 to September 2024.
=================================================
'''

# Import Libraries
import pandas as pd
import psycopg2 as db
import datetime as dt
import pendulum
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Import data from PostgreSQL
def import_from_postgresql():
    """
    Connects to a PostgreSQL database, fetches data from the table, and saves it to a CSV file.

    Steps:
    1. Establishes a connection to the PostgreSQL database using the provided connection string.
    2. Executes a SQL query to fetch all data from the table.
    3. Saves the fetched data as a CSV file to the desired location.

    Return:
        None - This function does not return any value; it performs the data fetching and saving process.

    Example usage:
        In an Airflow DAG, this function is called as part of the workflow:
        fetch_from_sql = PythonOperator(
            task_id='import_from_postgresql', 
            python_callable=import_from_postgresql
        )

    Notes:
        This function fetches data from the `electronics_sales` table in the PostgreSQL database and saves it as a CSV file named 'raw_data.csv' in the `/opt/airflow/data/` directory.
    """

    # Connect to PostgreSQL
    conn_string = "dbname='electronics_sales_db' host='postgres' user='airflow' password='airflow'"
    conn = db.connect(conn_string)
    
    # Fetch data from PostgreSQL
    df = pd.read_sql("SELECT * FROM electronics_sales;", conn)
    conn.close()

    # Save to a CSV file
    df.to_csv('/opt/airflow/data/raw_data.csv', index=False)

# Data Cleaning
def cleaning_data():
    """
    Cleans the raw data by performing several transformations and saves the cleaned data to a new CSV file. The function reads the raw data from a CSV file and applies several data cleaning steps:
    1. Drops duplicate rows.
    2. Adds a 'transaction_id' column as the index, starting from 1.
    3. Modifies the 'Add-ons Purchased' column, setting non-null values to 'Add ons' and null values to None.
    4. Handles missing values by:
        - Filling missing values in the 'Add-ons Purchased' column with 'No Add ons'.
        - Filling missing values in categorical columns with the mode.
        - Filling missing values in numerical columns with the median value.
    5. Normalizes column names by stripping spaces, converting to lowercase, and replacing spaces with underscores.
    
    After cleaning data, the function saves the cleaned dataset to a new CSV file.

    Return:
        None - This function does not return any value; it performs data cleaning and saves the cleaned data to a new CSV file.

    Example usage:
        In an Airflow DAG, this function is called as part of the workflow:
        data_cleaning = PythonOperator(
            task_id='cleaning_data', 
            python_callable=cleaning_data
        )

    Notes:
        The cleaned dataset is saved to the file 'cleaned_data.csv' in the /opt/airflow/data/ directory.
    """

    # Read CSV file
    df = pd.read_csv('/opt/airflow/data/raw_data.csv')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Change value add-ons column
    df['Add-ons Purchased'] = df['Add-ons Purchased'].apply(lambda x: 'Add ons' if pd.notna(x) else None) 
    
    # Handle missing values
    for column in df.columns:
        if column == 'Add-ons Purchased':
            df[column] = df[column].fillna('No Add ons')                # Handling missing value for column 'Add-ons Purchased'
        elif column in df.select_dtypes(include=['object']).columns:
            df[column] = df[column].fillna(df[column].mode()[0])        # Handling missing value for categorical columns with mode
        elif column in df.select_dtypes(include=['number']).columns:
            df[column] = df[column].fillna(df[column].median())         # Handling missing value for numerical columns with median

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r'[-\s]', '_')   # Remove leading/trailing spaces, lowercase, and change space and hyphen into underscore

    # Add column transaction_id as an index
    df.insert(0, 'transaction_id', range(1, len(df) + 1))

    # Add column revenue
    df['revenue'] = df['total_price'] + df['add_on_total']

    # Change value paymnent method
    df['payment_method'] = df['payment_method'].str.replace('Paypal', 'PayPal')

    # Save the cleaned data to a CSV file
    df.to_csv('/opt/airflow/data/clean_data.csv', index=False)
    print("Data cleaned and saved to CSV.")


# Export cleaned data to ElasticSearch
def export_to_elasticsearch():
    """
    Exports cleaned data to an Elasticsearch index using bulk indexing.

    Steps:
    1. Connects to the Elasticsearch instance running on the specified host and port.
    2. Reads the cleaned data from the CSV file 
    3. Prepares the data for bulk indexing by converting it to a list of dictionaries.
    4. Performs bulk indexing of the data into the 'sales_data' index in Elasticsearch.

    Return:
        None - This function does not return any value; it performs data indexing to Elasticsearch.

    Example usage:
        In an Airflow DAG, this function is called as part of the workflow:
        post_to_elasticsearch = PythonOperator(
            task_id='export_to_elasticsearch', 
            python_callable=export_to_elasticsearch
        )

    Notes:
        The Elasticsearch instance is accessed through the host 'elasticsearch' at port 9200.
        The function uses the `bulk` helper function from the `elasticsearch.helpers` module for efficient indexing. The data is indexed into the 'sales_data' index in Elasticsearch.
    """

    # Connect to Elasticsearch
    es = Elasticsearch([{'host':'elasticsearch', 'port':9200, 'scheme':'http'}])

    # Read CSV file
    df = pd.read_csv('/opt/airflow/data/clean_data.csv')

    # Prepare data for bulk indexing
    actions = [
        {
            "_index": "electronics_sales",  
            "_source": r.to_dict()   
        }
        for _, r in df.iterrows() 
    ]

    # Bulk indexing
    bulk(es, actions)
    print(f"Successfully indexed {len(actions)} documents to Elasticsearch.")

# Set timezone
local_tz = pendulum.timezone("Asia/Jakarta")

# DAG configuration
default_args = {
    'owner': 'aziz',
    'start_date': local_tz.datetime(2024, 11, 1),
    'retries': 1
}

# Define the DAG
with DAG('P2M3_aziz_DAG',
         description='DAG to import raw data from PostgreSQL, cleaned data, and post to Elasticsearch',
         default_args=default_args,
         schedule_interval='10,20,30 9 * * 6',  # Run every Saturday at 9:10, 9:20, and 9:30
         catchup=False
         ) as dag:
    
    # Ensure proper indentation of task definitions
    fetch_from_sql = PythonOperator(
        task_id='import_from_postgresql', 
        python_callable=import_from_postgresql
    )

    data_cleaning = PythonOperator(
        task_id='cleaning_data', 
        python_callable=cleaning_data
    )

    post_to_elasticsearch = PythonOperator(
        task_id='export_to_elasticsearch', 
        python_callable=export_to_elasticsearch
    )

    # Task dependencies
    fetch_from_sql >> data_cleaning >> post_to_elasticsearch
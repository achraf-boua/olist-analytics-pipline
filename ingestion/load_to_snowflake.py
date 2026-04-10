import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

# Mapping fichier CSV → nom de table dans Snowflake RAW
CSV_TO_TABLE = {
    "olist_customers_dataset.csv": "CUSTOMERS",
    "olist_orders_dataset.csv": "ORDERS",
    "olist_order_items_dataset.csv": "ORDER_ITEMS",
    "olist_products_dataset.csv": "PRODUCTS",
    "olist_sellers_dataset.csv": "SELLERS",
    "olist_order_payments_dataset.csv": "ORDER_PAYMENTS",
    "olist_order_reviews_dataset.csv": "ORDER_REVIEWS",
}


def get_connection():
    """Établit une connexion à Snowflake en utilisant les variables d'environnement."""
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

def load_csv(conn, csv_path: str, table_name: str):
    """Charge un fichier CSV dans une table Snowflake."""
    print(f"loading {csv_path} into {table_name}...", end=" ")

    df = pd.read_csv(csv_path)

    #Snowflake accepte les noms de colonnes en majuscules, on les convertit pour éviter
    df.columns = [col.upper() for col in df.columns]

    #write_pandas crée la table si elle n'existe pas et charge les données

    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name,
        auto_create_table=True,
        overwrite=True,  # Remplace les données existantes
        )
    print(f">> {nrows:,} rows loaded")
    return nrows

def main():
    print("="*50)
    print("Olist Data Ingestion to Snowflake RAW")
    print("="*50)

    conn = get_connection()
    print("Connected to Snowflake successfully! \n")


    data_dir = "data/olist"
    total_rows = 0

    for csv_file, table_name in CSV_TO_TABLE.items():
        cvs_path = os.path.join(data_dir, csv_file)
        if not os.path.exists(cvs_path):
            print(f"File not found: {cvs_path}, skipping...")
            continue

        rows = load_csv(conn, cvs_path, table_name)
        total_rows += rows

    conn.close()
    print(f"\n="*50)
    print(f" Done! Total rows loaded into OLIST_DB.RAW: {total_rows:,}")
    print(f"="*50)

if __name__ == "__main__":
    main()
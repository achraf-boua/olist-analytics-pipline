#========================================================
#  Cette version utilise pathlib pour gérer les chemins 
# et ajoute des colonnes de métadonnées pour la date 
# d'ingestion et le nom du fichier source.
#========================================================

# Déclattion des bibliothèques nécessaires

import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
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


# chemin absolu vers les données source et la date d'ingestion  

path = Path("/home/achloq/olist-analytics-pipline/data/olist")
date_ingestion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#===================================================================
# Cette fonction crée une connexion à Snowflake en utilisant
# les informations d'identification stockées dans le fichier .env.    
# Elle configure également le contexte de la session pour utiliser
# l'entrepôt, la base de données et le schéma appropriés.
#===================================================================

def get_connection():
    """Crée une connexion à Snowflake avec les credentials du .env"""
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="OLIST_WH",
        database="OLIST_DB",
        schema="RAW",
        role="ACCOUNTADMIN",
    )
    # Force le contexte — nécessaire pour write_pandas
    cursor = conn.cursor()
    cursor.execute("USE WAREHOUSE OLIST_WH")
    cursor.execute("USE DATABASE OLIST_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.close()
    return conn

# Cette fonction charge un fichier CSV dans une table Snowflake.
def load_csv(conn, csv_path: str, table_name: str, file_name: str):
    """Charge un fichier CSV dans une table Snowflake."""
    print(f"loading {csv_path} into {table_name}...", end=" ")

    df = pd.read_csv(csv_path)
    df['DATE_INGESTION'] = date_ingestion
    df['SOURCE_FILE'] = file_name
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
#   connexion à Snowflake
    conn = get_connection()
    print("Connected to Snowflake successfully! \n")

    total_rows = 0

    for file, table_name in CSV_TO_TABLE.items():
        chemin_fichier = path / file
        if not chemin_fichier.exists():
            print(f"File not found: {chemin_fichier}, skipping...")
            continue
        rows = load_csv(conn, chemin_fichier, table_name, file)
        print(f"Le fichier {file} a été chargé dans la table {table_name} avec succès.")
        total_rows += rows 

#   Fermeture de la connexion
    conn.close()
    print(f"\n="*50)
    print(f" Done! Total rows loaded into OLIST_DB.RAW: {total_rows:,}")
    print(f"="*50)

if __name__ == "__main__":
    main()
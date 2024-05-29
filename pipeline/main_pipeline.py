import os
import json
import pandas as pd
from connection import close_conn, create_conn
from ingestion.to_landing import load_table_to_landing
# from transformation.etl import (
#     clean_data,
#     create_schema,
#     load_tables_staging,
#     read_table,
# )


def main():

    engine = create_conn()

    """ Landing area """
    file_path = os.getenv('FILE_PATH')
    table_name = os.getenv('TABLE_NAME')
    df = pd.read_csv(file_path)
    print(df)
    load_table_to_landing(df, engine, table_name)

    close_conn(engine)


if __name__ == "__main__":
    main()

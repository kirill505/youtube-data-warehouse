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
    file_path = os.getenv('SAVE_PATH')


    table_name = os.getenv('TABLE_NAME')
    files  = [file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]
    print(file_path, files)

    df = pd.DataFrame()
    for file in files:
        file_url = os.path.join(file_path, file)
        df_appended = pd.read_csv(file_url)
        # data.append(df)
        # print(len(data), data)

        df = pd.concat([df, df_appended])

    # df = pd.read_csv(file_path)
    print(df)
    load_table_to_landing(df, engine, table_name)

    close_conn(engine)


if __name__ == "__main__":
    main()

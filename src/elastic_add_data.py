import variables
import pandas as pd

from elasticsearch import Elasticsearch, helpers
es = Elasticsearch([{'host':variables.host , 'port': variables.port}])


def add_csv_to_index(input_df, key_columns, index_name):
    """
    This function will create a key  column in the df
    to later on use as the _id in they key for each document.


    """
    def create_id_col(x):
        row = ""
        for k in key_columns:
            row = row + str(x.get(k)) + "|"
        return "_".join(row.split("|")[:-1])

    input_df["_id"]  = input_df.apply(lambda x: create_id_col(x), axis=1)
    to_elastic_data = list(input_df.T.to_dict().values())

    response = helpers.bulk(es, to_elastic_data, index=index_name, doc_type='_doc', request_timeout=200)
    return response


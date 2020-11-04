import variables
import flatdict
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host':variables.host, 'port': variables.port}])

def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    return res

def get_search_object(text, query_size = 100):
    search_object = {
        "size": query_size ,
                'query':
                         {'match':
                                   {
                                       variables.cn_text : { 'query': text ,
                                        # 'operator': 'and',
                                        # 'fuzziness' : 'auto'
                                                 }
                                   }
                          },

                     }
    return search_object



def format_matched_obj(search_res):
    res = [flatdict.FlatDict(e) for e in search_res['hits']['hits']]
    df = pd.DataFrame(res)
    df.columns = variables.columns_index
    return df


def query_text(text, query_size = 100, index_name = "not_an_index"):
    search_object = get_search_object(text, query_size = query_size)
    search_res = search(es,
                                           index_name = index_name ,
                                           search = json.dumps(search_object))
    return format_matched_obj(search_res)

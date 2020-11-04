import requests
import json
import src import variables
from elasticsearch import Elasticsearch

settings = {
    'settings': {
        'index': {
            'number_of_shards': variables.number_of_shards ,
            'number_of_replicas': variables.number_of_replicas ,
            # configure our default similarity algorithm explicitly to use bm25,
            'similarity': {
                'default': {
                    'type': 'BM25',
                     "b": variables.b ,
                     "k1": variables.k1
                }
            }
        }
    },
    # we will be indexing our documents in the title field using the English analyzer,
    # which removes stop words for us, the default standard analyzer doesn't have
    # this preprocessing step
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html
    'mappings': {
            'properties': {
                variables.cn_text : {
                    'type': 'text',
                    'analyzer': 'english'
                },
                variables.cn_doc_name : {"type": "text"}
            }
    }
}


def re_index(es, indexes, settings, delete_if_exists = True):
    for index in indexes:
        if delete_if_exists:
            print(es.indices.delete(index=indexes, ignore=[400, 404]))
        headers = {'Content-Type': 'application/json'}
        response = requests.put(variables.index_url + index, data=json.dumps(settings), headers=headers)
        return response

if __name__ == "__main__":
    #
    es = Elasticsearch([{'host': variables.host, 'port': variables.port}])
    #
    indexes = ['squad']
    re_index(es, indexes, settings, delete_if_exists = True)

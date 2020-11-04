"""
This is just a file with common variables
"""
# ELASTIC index configurations
host = "localhost"
port = 9200

number_of_shards = 1
number_of_replicas = 1

# BM25 configurations
b = 0.6
k1 = 0.1

# COLUMN NAMES
cn_text = "text" # name of the text property
cn_doc_name = "doc_name" # name of the document name property
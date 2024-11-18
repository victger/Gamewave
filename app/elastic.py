from elasticsearch import Elasticsearch
from app.elastic_utils import *

es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
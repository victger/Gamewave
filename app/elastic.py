from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, "scheme": "http"}])

def search_all_data(index_name, size=2000):
    """Fetch all data from the given index."""
    query = {"query": {"match_all": {}}}
    result = es.search(index=index_name, body=query, size=size)
    return [hit['_source'] for hit in result['hits']['hits']]

def search_with_filters(index_name, filters, size=2000):
    """Search data with filters applied (Game, Video title, Channel, Date, Tags)."""
    query = {"bool": {"must": filters}}
    result = es.search(index=index_name, query=query, size=size)
    return [hit['_source'] for hit in result['hits']['hits']]

def autocomplete_suggestions(index_name, field, tokens, filters, size=2000):
    """Fetch autocomplete suggestions based on field and tokens."""
    autocomplete_clauses = [
        {
            "bool": {
                "should": [
                    {"prefix": {field: {"value": i}}},
                    {"fuzzy": {field: {"value": i, "fuzziness": "AUTO"}}}
                ]
            }
        } for i in tokens
    ]
    
    query_body = {"bool": {"must": filters + autocomplete_clauses}}
    
    response = es.search(index=index_name, query=query_body, size=size)
    return response
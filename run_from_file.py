import sys
from query_class import *
from parse_query import parse_query_from_json

if not sys.argv[1]:
    raise ValueError('Please provide a file string as argument')
    # replace this with a folder of JSON files

with open(sys.argv[1], 'r') as f:
    daily_queries = f.readlines()

for file in daily_queries:
    # use Scott's function
    query_object = parse_query_from_json(file)

    query_object.run()
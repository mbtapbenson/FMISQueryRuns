import os
import sys
import json
from query_class import *

def parse_query_from_json(filename):
    with open(filename, 'r') as f:
        query_json = json.load(f)
    
    # We have query_json, now we need to parse the fields into a valid query. 

    # Important parameter: query type. Using this, we can reference a dictionary of type:constructor. 
    
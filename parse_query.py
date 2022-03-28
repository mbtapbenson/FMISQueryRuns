import os
import sys
import json
from query_class import *

query_type_dict = {"direct_query": Query.__init__,
                    "parameterized_query": ParameterizedQuery.__init__,
                    "vendors_query": VendorsQuery.__init__, 
                    "parameterized_query_2_dates": ParameterizedQueryTwoDates.__init__,
                    "parameterized_query_1_date": ParameterizedQueryOneDate.__init__,
                    "date_looping_query": DateLoopingQuery.__init__,
                    "date_looping_query_time_duration": DateLoopingQueryDuration.__init__, 
                    "filter_fields_input": FilterFieldsInput.__init__
}

def parse_query_from_json(filename):
    with open(filename, 'r') as f:
        query_json = json.load(f)
    
    # We have query_json, now we need to parse the fields into a valid query. 
    
    # Important parameter: query type. Using this, we can reference a dictionary of type:constructor. 

    query_constructor = query_type_dict.get(query_json['query_type'])

    return query_constructor(query_json['query_dlpath'], query_json['qname'], query_json['base_name'], 
                            query_json['query_type'], query_json['parameters'])

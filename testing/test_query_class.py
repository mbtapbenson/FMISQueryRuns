import unittest
import json
import query_class
import parse_query

class TestQueryMethods(unittest.TestCase):

    def example_query(dlpath, qname, base_name, qtype, parameters):
        # Simple helper function for using the query parser. Otherwise, we would have to switch functions 
        # based on query type. 
        ex_query_dict = {'query_dlpath': dlpath, 'qname': qname, 'base_name': base_name, 
                        'query_type': qtype, 'parameters': parameters}
        
        json.dump(ex_query_dict, 'example_query_test.json')

        ex_query_obj = parse_query.parse_query_from_json('example_query_test.json')

        ex_query_obj.run()


if __name__ == '__main__':
    unittest.main()
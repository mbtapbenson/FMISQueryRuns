import os
import datetime
import sys

from rm_head import rm_head_function

sys.path.append('/home/rubix/Desktop/Project-Ducttape')
import ducktape

# GLOBAL VARIABLES:
rubix_tape_base_path = "/home/rubix/Desktop/Project-Ducttape"
rubix_tape_data_path = "/home/rubix/Desktop/Project-Ducttape/data"
rubix_tape_data_file_path = "/home/rubix/O_drive_mnt_pt/VENDOR_MANAGEMENT/Data_Analytics/Data_Files/Daily_Reports"
rubix_tape_script_path = "/home/rubix/Desktop/Project-Ducttape/scripts"
rubix_tape_items_path = "/home/rubix/O_drive_mnt_pt/1_P&L_Division/Data_Analytics/Data_Repositories/Inventory_Mgmt_Data/Inventory_Items"
# the tape_itmes_path seems to be deprecated.

class Query:
    def __init__(self, dlpath, qname, base_name, qtype, parameters) -> None:
        # Parameters for this:
        # - DL path
        # - Query Name (ex. PL_PO_ENCUMB)
        # - base name (ex. pl_invent_mgmt). This is used for file storage.
        # - Query type (ex. direct_query)
        # - Query Parameters (ex. date ranges)
        # - Query Schedule (a file containing which file to dump this query. each schedule file is 
        # a different interval, for example, weekly.)

        self.dlpath = dlpath
        self.qname = qname
        # This is of the form "UPPERCASE_QUERY_NAME"
        self.base_name = base_name
        # This is of the form "lowercase_more_explicit_name"
        self.query_type = qtype
        # This is the query function to be used. We haven't implemented this yet.
        # Command pattern?
        # Baed on the JSON file, you would return a different version of the Query class (but still be able to run it).
        # just call query.fetch()
        self.parameters = parameters

    def run(self):
        # Needs a date (for storage)
        # needs a "basename" for storage purposes

        date = self.setup()
        # this has to return the date, so that we can use it in the dl_path in the query
        
        # run the query here

        # example download path: 
        # dlpath = '/home/rubix/Desktop/Project-Ducttape/data/pl_invent_mgmt/' + date + '/'
        # note: the dlpath is just rubix_tape_data_path + base_name + date

        query_dlpath = rubix_tape_data_path + self.base_name + date
        
        # Create browser object
        display, browser = ducktape.chrome_initialize(query_dlpath)
        # dl_path is not strictly necessary
        ducktape.fmis_login(browser)

        # here, we have to access some kind of dictionary of qtype:query function
        self.fetch(browser)

        ducktape.wait_for_file(query_dlpath)
        ducktape.chrome_close(display, browser)

        self.teardown(date)

    def fetch(self, browser):
        ducktape.fmis_get_direct_query(browser, self.qname)

    def setup(self):
        date = datetime.date.today().strftime("%m%d%Y-%H%M%S")

        # Key steps here:
        # cd to rubix_tape_base_path
        os.chdir(rubix_tape_base_path)
        # mkdir tape_data_path/basename/today's date
        os.mkdir(rubix_tape_data_path + self.base_name + date)
        
        return date

    def teardown(self, date):
        # need to change the file name to a new format. 
        # this changes it from the "old style" (uppercase) to the "new style" (lowercase)
        query_path = self.to_path(rubix_tape_data_path, self.base_name, date, self.qname)

        os.rename(query_path + '\_*.xlsx', 
                  query_path + '-' + date + '.xlsx')

        # need to run rm_head.py (in rubix_tape_base_path)
        # this formats columns and sends the formatted file to the O drive 
        rm_head_function(self.to_path([rubix_tape_data_path, self.base_name, date, self.qname + '-' + date + '.xlsx']), 
                         self.to_path([rubix_tape_items_path, self.qname + '.xlsx']))

        # the db type and the location are deprecated

    def to_path(list_of_strings):
        # converts 

        path_sep = '/'

        base_path = ''

        for file in list_of_strings:
            base_path += file + path_sep
        
        return base_path

# Here, we implement the query subclasses:

class ParameterizedQuery(Query):
    def fetch(self, browser):
        ducktape.fmis_get_parameterized_query(browser, self.qname)
    
class VendorsQuery(Query):
    def fetch(self, browser):
        ducktape.fmis_vendors_query(browser, self.qname, *self.parameters)

class ParameterizedQueryTwoDates(Query):
    def fetch(self, browser):
        ducktape.fmis_get_parameterized_query_2_dates(browser, self.qname, *self.parameters)

class ParameterizedQueryOneDate(Query):
    def fetch(self, browser):
        ducktape.fmis_get_parameterized_query_1_date(browser, self.qname)

class DateLoopingQuery(Query):
    def fetch(self, browser):
        ducktape.fmis_date_looping_query(browser, self.qname, *self.parameters)

class DateLoopingQueryDuration(Query):
    def fetch(self, browser):
        ducktape.fmis_date_looping_query_time_duration(browser, self.qname, *self.parameters)

class FilterFieldsInput(Query):
    def fetch(self, browser):
        ducktape.fmis_filter_fields_input(browser, self.qname, *self.parameters)
import os
import datetime 
import sys

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
    def __init__(self, dlpath, qname, base_name, qtype, parameters, schedule) -> None:
        # Parameters for this:
        # - DL path
        # - Query Name (ex. PL_PO_ENCUMB)
        # - base name (ex. pl_invent_mgmt). This is used for file storage.
        # - Query type (ex. direct_query)
        # - Query Parameters (ex. date ranges)
        # - Query Schedule

        self.dlpath = dlpath
        self.qname = qname
        # This is of the form "UPPERCASE_QUERY_NAME"
        self.base_name = base_name
        # This is of the form "lowercase_more_explicit_name"
        self.query_type = qtype
        self.parameters = parameters
        self.schedule = schedule

        # if this query is not scheduled in crontab, schedule it. 

    def run(self):
        # Needs a date (for storage)
        # needs a "basename" for storage purposes

        date = self.setup()
        # this has to return the date

        # run the query here
        # THIS IS A PLACEHOLDER
        dlpath = '/home/rubix/Desktop/Project-Ducttape/data/pl_invent_mgmt/' + date + '/'
        # note: the dlpath is just rubix_tape_data_path + base_name + date

        display, browser = ducktape.chrome_initialize(self.dlpath)
        ducktape.fmis_login(browser)
        ducktape.fmis_get_direct_query(browser, 'PL_INV_ITEM')
        ducktape.wait_for_file(dlpath)
        ducktape.chrome_close(display, browser)

    def setup(self):
        date = datetime.date.today().strftime("%m%d%Y-%H%M%S")

        # Key steps here:
        # cd to rubix_tape_base_path
        os.chdir(rubix_tape_base_path)
        # mkdir tape_data_path/basename/today's date
        os.mkdir(rubix_tape_data_path + self.base_name + date)
        pass

    def teardown(self):
        # need to change the file name to a new format. 
        # this changes it from the "old style" (uppercase) to the "new style" (lowercase)

        # need to run rm_head.py (in rubix_tape_base_path)
        # this formats columns and sends the formatted file to the O drive 

        # the db type and the location are deprecated (i'm pretty sure)
        pass
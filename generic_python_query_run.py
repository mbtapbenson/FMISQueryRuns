import sys
import ducktape

if not sys.argv[1]:
    raise ValueError('Please provide a date string as argument')

date = sys.argv[1]

dlpath = '/home/rubix/Desktop/Project-Ducttape/data/pl_invent_mgmt/' + date + '/'

display, browser = ducktape.chrome_initialize(dlpath)
ducktape.fmis_login(browser)
ducktape.fmis_get_direct_query(browser, 'PL_INV_ITEM')
ducktape.wait_for_file(dlpath)
ducktape.chrome_close(display, browser)
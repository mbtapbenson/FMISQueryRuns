import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import os
import json

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('fmis-new-query-logger-db0ca47a558c.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('New Query Form (Responses)')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

records_data = sheet_instance.get_all_records()
# This is a dict

#print(records_data)

# TODO:
# - Iterate through the responses
# - Figure out which ones are new (search run directory for JSON files with matching name) or are overriding previous ones
# For the new ones:
# - Format them into query JSON files (rename, clean up parameters, generate base name)
# - Save JSON files with proper naming convention
# - Schedule them (put into the correct folders) according to their schedule parameter

# Naming convention: basename.json
# base name = qname.lower()
# Current base names are used for storage and for script naming.

def get_basename(qname):
    # this is a placeholder until we formalize this
    return qname.lower()

def get_run_directory_files(runs_directory):
    # Gets all existing files in runs_directory
    listOfFiles = list()

    for (dirpath, dirnames, filenames) in os.walk(runs_directory):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    return listOfFiles

def schedule_to_path(schedule_code):
    schedule_dict = {'Weekly': 'weekly_path',
                    'Monthly': 'monthly_path',
                    'Yearly': 'yearly_path',
                    'Mornings (6AM)': 'morning_path',
                    'Evenings (8AM)': 'evening_path'}
    
    return schedule_dict[schedule_code]

def process_new_query(form_response):
    # rename parameter names
    mapping = {'Query Name':'qname', 'Query Type': 'query_type', 'Start Date (Query 2 Dates)':'start_date',
                'End Date (Query 2 Dates)': 'end_date'}
    
    for key in mapping:
        form_response[mapping[key]] = form_response.pop(key)
    
    # generate base name
    form_response['base_name'] = get_basename(form_response['qname'])
     
    # save to JSON
    json_string = json.dumps(form_response)

    # Calculate directory to put it in
    schedule_path = schedule_to_path(form_response['Schedule'])

    # save to correctly scheduled path
    with open(schedule_path + '/' + form_response['base_name'] + '.json', 'w') as outfile:
        outfile.write(json_string)

# Here's where the actual run starts
# gets all run files as a reference for which files to process
target_dir_files = get_run_directory_files('runs/directory/here')
new_queries = []

for response in records_data:
    # checks if query name is either new or overriding a previous filename
    if (get_basename(response['Query Name']) not in target_dir_files) or ((get_basename(response['Query Name']) not in target_dir_files) and (response['Override Previous?'] == 'Yes')):
        process_new_query(response)

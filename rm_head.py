#!/usr/bin/python3

import warnings
import sys
import xlsxwriter
import pandas as pd
import datetime
import rm_head_utils

def rm_head_function(filename, writepath):
    #queryname is Excel file name shown in the O-drive, ie.PL_BUYER_BACKLOG
    #conv specifies the data type of certain fields when reading the Excel file
    queryname = writepath.split("/")[-1].replace(".xlsx", "")
    conv = rm_head_utils.read_excel_converter.get(queryname)

    #Read xlsx file using pandas (skip first row)
    # Forcing all field to str intentionally to avoid leading zeros downstream 
    # df = pd.read_excel(filename, sheet_name='sheet1', skiprows=1, dtype=str)
    df = pd.read_excel(filename, sheet_name='sheet1', skiprows=1, dtype=str, converters = conv)

    #Adding appropriate column name, pass in the first 3 characters to find_col_name
    df_colname = rm_head_utils.find_col_name(df.columns[0][:2])

    #Adding timestamp in newly added column, ie. df['PO - Query Date']= datetime.datetime.now()
    df[df_colname] = datetime.datetime.now()

    # Store the file with removed header at path defined by sys.argv[2]
    writer = pd.ExcelWriter(writepath, engine='xlsxwriter', datetime_format='YYYY-MM-DD')
    df.to_excel(writer, index=False, sheet_name='sheet1')
    writer.save()

#Arguments:
# sys.argv[1] is the input path                                                                                                                                                                       
# sys.arg[2] is the output path                                                                                                                                                                       
filename= sys.argv[1]
writepath = sys.argv[2]

#queryname is Excel file name shown in the O-drive, ie.PL_BUYER_BACKLOG
#conv specifies the data type of certain fields when reading the Excel file
queryname = writepath.split("/")[-1].replace(".xlsx", "")
conv = rm_head_utils.read_excel_converter.get(queryname)


#Function for extracting field initials
#def find_col_name(colname):
#    if colname in dictionary_header.keys():
#        return dictionary_header.get(colname)
#    else:
#        return "Query Date"


#Read xlsx file using pandas (skip first row)
# Forcing all field to str intentionally to avoid leading zeros downstream 
# df = pd.read_excel(filename, sheet_name='sheet1', skiprows=1, dtype=str)
df = pd.read_excel(filename, sheet_name='sheet1', skiprows=1, dtype=str, converters = conv)

#Adding appropriate column name, pass in the first 3 characters to find_col_name
df_colname = rm_head_utils.find_col_name(df.columns[0][:2])

#Adding timestamp in newly added column, ie. df['PO - Query Date']= datetime.datetime.now()
df[df_colname] = datetime.datetime.now()


# Store the file with removed header at path defined by sys.argv[2]
writer = pd.ExcelWriter(writepath, engine='xlsxwriter', datetime_format='YYYY-MM-DD')
df.to_excel(writer, index=False, sheet_name='sheet1')
writer.save()
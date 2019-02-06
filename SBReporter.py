#! /opt/Python/Python-3.6.5/python
# coding: utf8


"""
  Sergey Brazgin 05/2018
  sbrazgin@mail.ru
  Create Excel-file from single SQL
"""
import openpyxl
import logging
import logging.config
import sys
import cx_Oracle
import traceback
import configparser
import getopt
from pathlib import Path


# parameters
def read_params(inputfile):

    # global vars
    global log_file
    global username
    global password
    global hostName
    global portNumber
    global sid
    global sql_file
    global sqlCommand
    global first_row
    global first_col
    global excel_page

    # default
    excel_page = "Report"

    # start
    logger.debug('Input parameter file is "'+ inputfile+'"')

    my_file = Path(inputfile)
    if not my_file.is_file():
        print('Parameter file: '+inputfile+" does not exists!")
        logger.error('Parameter file: '+inputfile+" does not exists!")
        sys.exit(2)

    config = configparser.ConfigParser()
    config.read(inputfile)

    sql_file = config['REPORT']['sql_file']
    excel_page = config['REPORT']['excel_page']
    log_file = config['LOG']['log_file']
    username = config['DB']['username']
    password = config['DB']['password']
    hostName = config['DB']['hostName']
    portNumber = config['DB']['portNumber']
    sid = config['DB']['sid']

    first_row = int(config['REPORT']['first_row'])
    first_col = int(config['REPORT']['first_col'])

    # read sql file
    my_file = Path(sql_file)
    sqlCommand = ''
    if not my_file.is_file():
        print('Sql file: '+sql_file+" does not exists!")
        logger.error('Sql file: '+sql_file+" does not exists!")
        sys.exit(2)

    with open(sql_file, 'r') as myfile:
        sqlCommand=myfile.read()

    logger.info("Sql="+sqlCommand)

    if sqlCommand == '':
        logger.error('Sql file: '+sql_file+" empty!")
        sys.exit(2)


# -----------------------------------------------------------------------------------
def add_to_excel(cur_sor):
    my_file = Path(excel_file)
    if not my_file.is_file():
        logger.error('Excel file: '+excel_file+" does not exists!")
        sys.exit(2)

    wb = openpyxl.load_workbook(filename=excel_file)
    try:
        ws = wb[excel_page]  # 'Report'
    except Exception as e:
        logger.error('Function - add_to_excel In Exception')
        logger.error('  error open page: ',excel_page)
        logger.error(traceback.print_exc())

    row = first_row
    for tupple_row in cur_sor:
        col = first_col
        for list_item in tupple_row:
            ws.cell(row=row, column=col, value=list_item)
            col = col + 1
        row = row + 1
    wb.save(excel_file)


# -----------------------------------------------------------------------------------
# Function to Execute Sql commands over TNS
def runSqlTNS(sqlCommand, username, password, hostName, portNumber, sID):
    dsn_tns = cx_Oracle.makedsn(hostName, portNumber, sID)
    # print dsn_tns
    db = cx_Oracle.connect(username, password, dsn_tns)
    logger.info("db.version="+db.version)
    cursor = db.cursor()
    cursor.execute(sqlCommand)
    return cursor


# -----------------------------------------------------------------------------------
# MAIN proc
def main(argv):
    global excel_file
    global logger

    # -------------------
    # create logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info('Started')

    # -------------------
    # read input params
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        logger.debug('No input params - Exit 2')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            logger.debug('Help - Exit 2')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    inputfile  = inputfile.strip()
    outputfile = outputfile.strip()

    logger.debug('inputfile='+inputfile)
    logger.debug('outputfile='+outputfile)

    if inputfile == '' or outputfile == '':
        print('test.py -i <inputfile> -o <outputfile>')
        logger.debug('No input params 2 - Exit 2')
        sys.exit(2)

    excel_file = outputfile

    # -------------------
    # Read report params
    read_params(inputfile)

    # -------------------
    # Run Select
    try:
        c = runSqlTNS(sqlCommand, username, password, hostName, portNumber, sid)
    except Exception as e:
        logger.error('Function - runSql In Exception')
        logger.error(traceback.print_exc())
    try:
        add_to_excel(c)  # Send the Cursor to writetoExcel Function
        c.close()
    except Exception as e:
        logger.error('Function - writeToExcel In Exception')
        logger.error(traceback.print_exc())

    logger.info('Finished')


if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1:])



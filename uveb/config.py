import os
from dotenv import load_dotenv


PROJECT_FOLDER          = os.path.expanduser('/Users/apple/Desktop/uveb_b')
load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))


PROJECT_NAME            = os.getenv('PROJECT_NAME')
VERSION                 = os.getenv('VERSION')
ENV                     = os.getenv('ENV')

DEBUG                   = True if ENV == 'development' else False

DEV_DB_HOST             = os.getenv('DEV_DB_HOST')
DEV_DB_USER             = os.getenv('DEV_DB_USER')
DEV_DB_PASS             = os.getenv('DEV_DB_PASS')
DEV_DB_SCHEMA           = os.getenv('DEV_DB_SCHEMA')

PROD_DB_HOST            = os.getenv('PROD_DB_HOST')
PROD_DB_USER            = os.getenv('PROD_DB_USER')
PROD_DB_PASS            = os.getenv('PROD_DB_PASS')
PROD_DB_SCHEMA          = os.getenv('PROD_DB_SCHEMA')




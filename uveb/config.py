import os
# from dotenv import load_dotenv


# PROJECT_FOLDER          = os.path.expanduser('/Users/apple/Desktop/UVR/uveb_b')
# load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))


PROJECT_NAME            = os.getenv('PROJECT_NAME')
VERSION                 = os.getenv('VERSION')
ENV                     = os.getenv('ENV')

DEBUG                   = True if ENV == 'development' else False

DEV_DB_HOST             = os.getenv('DEV_DB_HOST')
DEV_DB_PORT             = os.getenv('DEV_DB_PORT')
DEV_DB_USER             = os.getenv('DEV_DB_USER')
DEV_DB_PASS             = os.getenv('DEV_DB_PASS')
DEV_DB_SCHEMA           = os.getenv('DEV_DB_SCHEMA')

PROD_DB_HOST            = os.getenv('PROD_DB_HOST')
PROD_DB_PORT            = os.getenv('PROD_DB_PORT')
PROD_DB_USER            = os.getenv('PROD_DB_USER')
PROD_DB_PASS            = os.getenv('PROD_DB_PASS')
PROD_DB_SCHEMA          = os.getenv('PROD_DB_SCHEMA')

SECRET_KEY              = os.getenv('SECRET_KEY')
MAIN_BUCKET             = os.getenv('MAIN_BUCKET')
ALI_ACCESS_KEY          = os.getenv('ALI_ACCESS_KEY')
ALI_SECRET_KEY          = os.getenv('ALI_SECRET_KEY')
ALI_ENDPOINT            = os.getenv('ALI_ENDPOINT')

TESTING                 = False if os.getenv('MAIL_TESTING') == 'False' else True
MAIL_SERVER             = os.getenv('MAIL_SERVER')
MAIL_PORT               = int(os.getenv('MAIL_PORT'))
MAIL_USE_TLS            = False if os.getenv('MAIL_USE_TLS') == 'False' else True
MAIL_USE_SSL            = False if os.getenv('MAIL_USE_SSL') == 'False' else True
MAIL_USERNAME           = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD           = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER     = (os.getenv('MAIL_SENDER'), os.getenv('MAIL_USERNAME'))
MAIL_MAX_EMAILS         = None if os.getenv('MAIL_MAX_EMAILS') == 'None' else int(os.getenv('MAIL_MAX_EMAILS'))
MAIL_ASCII_ATTACHMENTS  = False if os.getenv('MAIL_ASCII_ATTACHMENTS') == 'False' else True

IMAGE_EXTENSIONS_ALLOWED= ['jpg', 'jpeg', 'png']
VIDEO_EXTENSIONS_ALLOWED= ['mp4']



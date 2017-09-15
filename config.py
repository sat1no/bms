import os, random, string
import pytz

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
UPLOAD_FOLDER= 'C:\Users\rafal\Desktop\Flask'
MAX_CONTENT_PATH= 16 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SIJAX_STATIC_PATH = path
SIJAX_JSON_URI = '/static/js/sijax/json2.js'
WARSAW = pytz.timezone('Europe/Warsaw')

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
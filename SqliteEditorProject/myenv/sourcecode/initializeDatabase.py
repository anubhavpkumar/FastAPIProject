import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

queries = [
    'CREATE TABLE kinkster (id INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT NOT NULL, lastName TEXT, emailAddress TEXT, userstatus TEXT, location TEXT NOT NULL)',
    'CREATE TABLE kinkster_fetish_map (id INTEGER PRIMARY KEY AUTOINCREMENT, userId INTEGER NOT NULL, fetish text not null)',
    'CREATE TABLE kinkster_hardlimits_map (id INTEGER PRIMARY KEY AUTOINCREMENT, userId INTEGER NOT NULL, hardlimit text not null)',
    'CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT NOT NULL, lastName TEXT, emailAddress TEXT NOT NULL, phoneNumber TEXT NOT NULL, userpassword TEXT NOT NULL, isPhoneVerified BOOLEAN, isEmailVerified BOOLEAN)'
]

con = sqlite3.connect('kink.db');
cursorObj = con.cursor()

for query in queries:
    logging.debug('Executing: ' + query)
    cursorObj.execute(query)

logging.debug('Commiting to database')
con.commit()
logging.debug('Migration Complete')
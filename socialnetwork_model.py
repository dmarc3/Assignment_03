'''
Implementation of database model.
'''
import os
import logging
import peewee as pw

file = 'socialnetwork.db'
if not os.path.exists(file):
    logging.info('Creating database as %s', file)
else:
    logging.info('Loading database: %s', file)
db = pw.SqliteDatabase(file)
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(pw.Model):
    '''
    Define base model via PeeWee.Model
    '''
    logging.info('Model initialized.')
    class Meta:
        database = db

class Users(BaseModel):
    '''
    Defines the User
    '''
    user_id = pw.CharField(primary_key=True, unique=True, max_length=30)
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)
    user_email = pw.CharField()

class Status(BaseModel):
    '''
    Defines the Status
    '''
    status_id = pw.CharField(primary_key=True, unique=True)
    user = pw.ForeignKeyField(Users, backref='statuses', field='user_id', on_delete='CASCADE')
    status_text = pw.CharField()

db.create_tables([Users, Status])
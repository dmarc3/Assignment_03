'''
Implementation of database model.
Authors: Kathleen Wong and Marcus Bakke
'''
# pylint: disable=R0903
import os
import logging
import peewee as pw

FILE = 'socialnetwork.db'
if not os.path.exists(FILE):
    logging.info('Creating database as %s', FILE)
else:
    logging.info('Loading database: %s', FILE)
db = pw.SqliteDatabase(FILE)
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(pw.Model):
    '''
    Define base model via PeeWee.Model
    '''
    logging.info('Model initialized.')
    class Meta:
        '''
        Meta class for BaseModel
        '''
        database = db

class Users(BaseModel):
    '''
    Defines the User
    '''
    user_id = pw.CharField(primary_key=True, unique=True, max_length=30)
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)
    user_email = pw.CharField()

    class Meta:
        '''
        Implement constraints
        '''
        constraints = [pw.Check('LENGTH(user_id) < 30'),
                       pw.Check('LENGTH(user_name) < 30'),
                       pw.Check('LENGTH(user_last_name) < 100')]

class Status(BaseModel):
    '''
    Defines the Status
    '''
    status_id = pw.CharField(primary_key=True, unique=True)
    user = pw.ForeignKeyField(Users, on_delete='CASCADE', to_field='user_id')
    status_text = pw.CharField()


db.create_tables([Users, Status])

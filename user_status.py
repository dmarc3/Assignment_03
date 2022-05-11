'''
Classes to manage the user status messages
Author: Marcus Bakke

pylint disable E1101 (no-member) in order to element incorrect warnings
related to peewee model classes. I was trying to find a better way to
eliminate these warnings but couldn't. Seemed like pylint-peewee could
be a good pylint plugin but it seems under developed and I couldn't get
it to work.

This also appears to occur with Django as well.
Source: https://stackoverflow.com/questions/115977/using-pylint-with-django
'''
# pylint: disable=E1101
import logging
import peewee as pw
import socialnetwork_model as sm


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        logging.info('UserStatusCollection initialized.')
        self.database = sm.Status

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        try:
            status = self.database.create(status_id = status_id,
                                          user_id = user_id,
                                          status_text = status_text)
            status.save()
            logging.info('Added status %s by %s.', status_id, user_id)
            return True
        except pw.IntegrityError:
            logging.error('Unable to add %s.', status_id)
            return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message
        '''
        try:
            status = self.database.get(sm.Status.status_id == status_id)
            status.status_text = status_text
            status.save()
            logging.info('Modified status %s by %s.', status_id, user_id)
            return True
        except self.database.DoesNotExist:
            logging.error('Unable to modify %s.', status_id)
            return False

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        try:
            status = self.database.get(sm.Status.status_id == status_id)
            status.delete_instance()
            logging.info('Deleted status %s.', status_id)
            return True
        except self.database.DoesNotExist:
            logging.error('Unable to delete %s.', status_id)
            return False

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        try:
            status = self.database.get(sm.Status.status_id == status_id)
            logging.info('Found status %s.', status_id)
            return status
        except self.database.DoesNotExist:
            logging.error('Unable to find %s.', status_id)
            return None

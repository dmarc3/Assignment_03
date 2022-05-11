'''
Classes for user information for the social network project
All edits made by Kathleen Wong to incorporate logging issues.
'''
# pylint: disable=E1101
import logging
import peewee as pw
import socialnetwork_model as sm


class UserCollection:
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        logging.info('UserCollection initialized.')
        self.database = sm.Users

    def add_user(self, user_id, user_email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        try:
            user = self.database.create(user_id=user_id,
                                        user_email=user_email,
                                        user_name=user_name,
                                        user_last_name=user_last_name)
            user.save()
            logging.info('Added user %s', user_id)
            return True
        except pw.IntegrityError:
            logging.error('Unable to add %s.', user_id)
            return False

    def modify_user(self, user_id, user_email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        try:
            user = self.database.get(self.database.user_id == user_id)
            user.user_email = user_email
            user.user_name = user_name
            user.user_last_name = user_last_name
            user.save()
            logging.info('Modified user %s.', user_id)
            return True
        except self.database.DoesNotExist:
            logging.error('Unable to user %s.', user_id)
            return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        try:
            user = self.database.get(sm.Users.user_id == user_id)
            user.delete_instance()
            logging.info('Deleted user %s.', user_id)
            return True
        except self.database.DoesNotExist:
            logging.error('Unable to delete %s.', user_id)
            return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        try:
            user = self.database.get(sm.Users.user_id == user_id)
            logging.info('Found user %s.', user_id)
            return user
        except self.database.DoesNotExist:
            logging.error('Unable to find %s.', user_id)
            return None

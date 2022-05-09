'''
Classes for user information for the social network project
All edits made by Kathleen Wong to incorporate logging issues.
'''
# pylint: disable=R0903
import logging
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
            with sm.db.transaction():
                new_user = self.database.create(
                    user_id=user_id,
                    user_email=user_email,
                    user_name=user_name,
                    user_last_name=user_last_name,)
                new_user.save()
            return True
        except Exception as e:
            logging.info(f'Error creating user = {user_id}')
            logging.info(e)
            logging.info('See how the database protects our data')
            return False

    def modify_user(self, user_id, user_email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        if user_id not in self.database:
            logging.error('Unable to modify %s because it ' \
                          'does not exist in UserCollection.', user_id)
            logging.debug("UserCollection contains following users': %s",
                          ', '.join(self.database.keys()))
            return False
        self.database[user_id].email = user_email
        self.database[user_id].user_name = user_name
        self.database[user_id].user_last_name = user_last_name
        logging.info('Successfully modified user %s!', user_id)
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        if user_id not in self.database:
            # Fails if status does not exist
            logging.error('Unable to delete %s because it '
                          'does not exist in UserCollection.', user_id)
            logging.debug("UserCollection contains following user': %s,",
                          ', '.join(self.database.keys()))
            return False
        try:
            user = sm.Users.get(user_id == user_id)
            user.delete_instance()
        except Exception as e:
            logging.info(f'Error deleting user = {user_id}')
            logging.info(e)
            logging.info('See how the database protects our data')
        logging.info('Successfully deleted user %s!', user_id)
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        if user_id not in self.database:
            logging.error('Unable to find %s in UserCollection.', user_id)
            logging.debug("UserCollection contains following users': %s",
                          ', '.join([user.user_id for user in self.database]))
            return sm.Users(None, None, None, None)
        return self.database[user_id]

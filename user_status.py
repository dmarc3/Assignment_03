'''
Classes to manage the user status messages
All edits by Marcus Bakke.
'''
# pylint: disable=R0903
import logging

class UserStatus():
    '''
    class to hold status message data
    '''

    def __init__(self, status_id, user_id, status_text):
        logging.info('%s status initialized.', status_id)
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        logging.info('UserStatusCollection initialized.')
        self.database = {}

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        logging.info('Attempting to add status %s to UserStatusCollection...', status_id)
        if status_id in self.database:
            # Rejects new status if status_id already exists
            logging.error('Unable to add %s because it ' \
                          'already exists in UserStatusCollection.',
                          status_id)
            logging.debug("UserStatusCollection contains following status': %s",
                          ', '.join(self.database.keys()))
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        self.database[status_id] = new_status
        logging.info('Successfully added status %s!', status_id)
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        logging.info('Attempting to modify status %s...', status_id)
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            logging.error('Unable to modify %s because it ' \
                          'does not exist in UserStatusCollection.',
                          status_id)
            logging.debug("UserStatusCollection contains following status': %s",
                          ', '.join(self.database.keys()))
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        logging.info('Successfully modified status %s!', status_id)
        return True

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        logging.info('Attempting to delete status %s from UserStatusCollection...',
                     status_id)
        if status_id not in self.database:
            # Fails if status does not exist
            logging.error('Unable to delete %s because it ' \
                          'does not exist in UserStatusCollection.',
                          status_id)
            logging.debug("UserStatusCollection contains following status': %s",
                          ', '.join(self.database.keys()))
            return False
        del self.database[status_id]
        logging.info('Successfully deleted status %s!', status_id)
        return True

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        logging.info('Attempting to find status %s in UserStatusCollection...',
                     status_id)
        if status_id not in self.database:
            # Fails if the status does not exist
            logging.error('Unable to find %s in UserStatusCollection.',
                          status_id)
            logging.debug("UserStatusCollection contains following status': %s",
                          ', '.join(self.database.keys()))
            return UserStatus(None, None, None)
        logging.info('Successfully found status %s!', status_id)
        return self.database[status_id]

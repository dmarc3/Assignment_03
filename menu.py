'''
Provides a basic frontend

Kathleen incorporated all changes to users.py
Marcus incorporated all changes to user_status.py code.
'''
import sys
import logging
from datetime import datetime
import main

# Build logger
FILE_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(FILE_FORMAT)
LOG_FILE = f'log_{datetime.today():%d-%m-%Y}.log'
file_handler = logging .FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
# Add launch statement
logger.info('Session launched at %s.', datetime.today().strftime(':%H:%M:%S'))


def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        logging.info("An error occurred while trying to add new user")
    else:
        logging.info("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if main.update_user(user_id, email, user_name, user_last_name, user_collection):
        logging.info("User was successfully updated")
    else:
        logging.info("An error occurred while trying to update user")


def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if not result:
        logging.info("ERROR: User does not exist")
    else:
        logging.info('User ID: %s', result.user_id)
        logging.info('Email: %s', result.user_email)
        logging.info('Name: %s', result.user_name)
        logging.info('Last name: %s', result.user_last_name)


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        logging.info("An error occurred while trying to delete user")
    else:
        logging.info("User was successfully deleted")


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        logging.info("An error occurred while trying to add new status")
    else:
        logging.info("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        logging.info("An error occurred while trying to update status")
    else:
        logging.info("Status was successfully updated")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result:
        logging.info("ERROR: Status does not exist")
    else:
        logging.info("User ID: %s", result.user_id)
        logging.info("Status ID: %s", result.status_id)
        logging.info("Status text: %s", result.status_text)


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        logging.info("An error occurred while trying to delete status")
    else:
        logging.info("Status was successfully deleted")


def quit_program():
    '''
    Quits program
    '''
    logging.info('Quitting program.')
    sys.exit()


if __name__ == '__main__':
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': add_status,
        'H': update_status,
        'I': search_status,
        'J': delete_status,
        'K': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Add status
                            H: Update status
                            I: Search status
                            J: Delete status
                            K: Quit

                            Please enter your choice: """)
        user_selection = user_selection.upper().strip()
        if user_selection in menu_options:
            logging.info('User selected %s ' \
                         '-> executing %s.',
                         user_selection,
                         menu_options[user_selection].__name__)
            menu_options[user_selection]()
        else:
            logging.info('%s is an invalid option.', user_selection)
            logging.info("Invalid option")

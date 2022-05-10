'''
Unittests for users.py.
Author: Kathleen Wong
'''
import unittest
import peewee as pw
import users
import socialnetwork_model as sm

MODELS = [sm.Users, sm.Status]
test_db = pw.SqliteDatabase(':memory:')
test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
test_db.connect()
test_db.create_tables(MODELS)
test_db.execute_sql('PRAGMA foreign_keys = ON;')


class TestUser(unittest.TestCase):
    '''
    Test class for users.py
    '''
    user_collection = users.UserCollection()

    def test_init(self):
        '''
        Test __init__ method.
        '''
        self.assertEqual(type(self.user_collection.database), type(sm.Users))

    def test_add_user(self):
        '''
        Test add_user method.
        '''
        user = self.user_collection.add_user('test01', 'test@gmail.com', 'Test', 'Account')
        self.assertTrue(user)
        user2 = self.user_collection.add_user('test01', 'test@gmail.com', 'Test', 'Account')
        self.assertFalse(user2)

    def test_modify_user(self):
        '''
        Test modify_user method.
        '''
        self.user_collection.add_user('test01', 'test@gmail.com', 'Test', 'Account')
        user = self.user_collection.database.get(self.user_collection.database.user_id == 'test01')
        self.assertEqual('test@gmail.com', user.user_email)
        self.assertEqual('Test', user.user_name)
        self.assertEqual('Account', user.user_last_name)
        self.user_collection.modify_user('test01', 'test1@gmail.com', 'Test1', 'Account1')
        modified_user = self.user_collection.database.get(
                        self.user_collection.database.user_id == 'test01')
        self.assertEqual('test1@gmail.com', modified_user.user_email)
        self.assertEqual('Test1', modified_user.user_name)
        self.assertEqual('Account1', modified_user.user_last_name)
        false = self.user_collection.modify_user('fail', 'fail@gmail.com', 'Fail', 'Account')
        self.assertFalse(false)

    def test_delete_user(self):
        '''
        Test delete_user
        '''
        self.user_collection.add_user('test01', 'test@gmail.com', 'Test', 'Account')
        self.user_collection.delete_user('test01')
        self.user_collection.delete_user('fail')

    def search_user(self):
        self.user_collection.add_user('test01', 'test@gmail.com', 'Test', 'Account')
        user = self.user_collection.search_user('test01')
        self.assertEqual(user.user_email, 'test@gmail.com')
        self.assertEqual(user.user_name, 'Test')
        self.assertEqual(user.user_last_name, 'Account')
        fail = self.user_collection.search_user('fail')
        self.assertFalse(fail)

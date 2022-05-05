'''
Unittest module.
Disable "Too many public methods" pylint message.
'''
# pylint: disable=R0904
import unittest
import os
import logging
from mock import patch
import users
import user_status
import main

class TestMain(unittest.TestCase):
    '''
    Test class for main.py
    '''
    def setUp(self):
        '''
        setUp method to disable logging.
        '''
        logging.disable(logging.CRITICAL)

    def test_init_user_collection(self):
        '''
        Test UserCollection initialization
        '''
        user_collection = main.init_user_collection()
        self.assertEqual(type(user_collection), type(users.UserCollection()))
        self.assertEqual(user_collection.database, {})

    def test_users(self):
        '''
        Test Users class initialization
        '''
        user = users.Users('test123', 'myemail@gmail.com', 'Test1', 'Test2')
        self.assertEqual(user.user_id, 'test123')
        self.assertEqual(user.email, 'myemail@gmail.com')
        self.assertEqual(user.user_name, 'Test1')
        self.assertEqual(user.user_last_name, 'Test2')

    def test_init_status_collection(self):
        '''
        Test UserStatusCollection initialization
        '''
        user_status_collection = main.init_status_collection()
        self.assertEqual(type(user_status_collection), type(user_status.UserStatusCollection()))
        self.assertEqual(user_status_collection.database, {})

    def test_user_status(self):
        '''
        Test UserStatus class initialization
        '''
        status = user_status.UserStatus('test123_00001', 'test123', 'Test status!')
        self.assertEqual(status.status_id, 'test123_00001')
        self.assertEqual(status.user_id, 'test123')
        self.assertEqual(status.status_text, 'Test status!')

    def test_load_users(self):
        '''
        Test load_users method
        '''
        # Test good accounts
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        result = main.load_users(filename, user_collection)
        expected = {'dave03': users.Users('dave03', 'david.yuen@gmail.com', 'David', 'Yuen'),
                    'evmiles97': users.Users('evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles')}
        for key, value in user_collection.database.items():
            for attr in ['user_id', 'email', 'user_name', 'user_last_name']:
                self.assertEqual(getattr(value, attr), getattr(expected[key], attr))
        self.assertTrue(result)

        # Test bad accounts
        user_collection = main.init_user_collection()
        filenames = [os.path.join('test_files', 'test_bad_accounts_1.csv'),
                     os.path.join('test_files', 'test_bad_accounts_2.csv'),
                     os.path.join('test_files', 'test_bad_accounts_3.csv'),
                     os.path.join('test_files', 'test_bad_accounts_4.csv'),
                     'this_file_doesnt_exist.csv']
        for filename in filenames:
            result = main.load_users(filename, user_collection)
            self.assertFalse(result)

    def test_save_users(self):
        '''
        Test save_users method
        '''
        # Successful Save
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        main.load_users(filename, user_collection)
        main.add_user('mbak79', 'mbakke4@uw.edu', 'Marcus', 'Bakke', user_collection)
        out_file = os.path.join('test_files', 'saved_add_accounts.csv')
        exp_file = os.path.join('test_files', 'test_save_accounts.csv')
        main.save_users(out_file, user_collection)
        with open(out_file, 'r', encoding='utf-8') as out:
            with open(exp_file, 'r', encoding='utf-8') as exp:
                self.assertEqual(out.readline(), exp.readline())
        # Unsuccessful Save
        self.assertFalse(main.save_users('this/folder/doesnt/exist.csv', user_collection))

    def test_load_status_updates(self):
        '''
        Test load_status_updates method
        '''
        # Test good accounts
        status_collection = main.init_status_collection()
        result = main.load_status_updates(os.path.join('test_files',
                                                       'test_good_status_updates.csv'),
                                          status_collection)
        expected = {'evmiles97_00001': user_status.UserStatus('evmiles97_00001',
                                                              'evmiles97',
                                                              'Code is finally compiling'),
                    'dave03_00001': user_status.UserStatus('dave03_00001',
                                                           'dave03',
                                                           'Sunny in Seattle this morning'),
                    'evmiles97_00002': user_status.UserStatus('evmiles97_00002',
                                                              'evmiles97',
                                                              'Perfect weather for a hike')}
        for key, value in status_collection.database.items():
            for attr in ['status_id', 'user_id', 'status_text']:
                self.assertEqual(getattr(value, attr), getattr(expected[key], attr))
        self.assertTrue(result)

        # ADD FAILED SCENARIO

    def test_save_status_updates(self):
        '''
        Test save_status_updates method
        '''
        # Test successful save
        status_collection = main.init_status_collection()
        filename = os.path.join('test_files', 'test_good_status_updates.csv')
        main.load_status_updates(filename, status_collection)
        main.add_status('mbak79', 'mbak79_00001', 'Yay! Homework!', status_collection)
        out_file = os.path.join('test_files', 'saved_status_updates.csv')
        exp_file = os.path.join('test_files', 'test_save_status_updates.csv')
        main.save_status_updates(out_file, status_collection)
        with open(out_file, 'r', encoding='utf-8') as out:
            with open(exp_file, 'r', encoding='utf-8') as exp:
                self.assertEqual(out.readline(), exp.readline())
        # ADD FAILED SCENARIO

    def test_add_user(self):
        '''
        Test add_user method
        '''
        # Test add_user function success
        user_collection = main.init_user_collection()
        result = main.add_user('mbak79', 'mbakke4@uw.edu', 'Marcus', 'Bakke', user_collection)
        self.assertTrue(result)
        self.assertEqual(user_collection.database['mbak79'].user_id, 'mbak79')
        self.assertEqual(user_collection.database['mbak79'].email, 'mbakke4@uw.edu')
        self.assertEqual(user_collection.database['mbak79'].user_name, 'Marcus')
        self.assertEqual(user_collection.database['mbak79'].user_last_name, 'Bakke')
        # Test add_user function failure
        result = main.add_user('mbak79', 'test@gmail.com', 'Test1', 'Test2', user_collection)
        self.assertFalse(result)
        self.assertEqual(user_collection.database['mbak79'].user_id, 'mbak79')
        self.assertEqual(user_collection.database['mbak79'].email, 'mbakke4@uw.edu')
        self.assertEqual(user_collection.database['mbak79'].user_name, 'Marcus')
        self.assertEqual(user_collection.database['mbak79'].user_last_name, 'Bakke')
        result = main.add_user('mba1239', 'test@.', 'Test1', 'Test2', user_collection)
        self.assertFalse(result)

    def test_update_user(self):
        '''
        Test update_user method
        '''
        # Test update_user function success
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        main.load_users(filename, user_collection)
        result = main.update_user('dave03',
                                  'newemail@gmail.com',
                                  'Notdave',
                                  'Notyuen',
                                  user_collection)
        self.assertEqual(user_collection.database['dave03'].email, 'newemail@gmail.com')
        self.assertEqual(user_collection.database['dave03'].user_name, 'Notdave')
        self.assertEqual(user_collection.database['dave03'].user_last_name, 'Notyuen')
        self.assertTrue(result)
        # Test update_user function failure
        result = main.update_user('test123',
                                  'some_email@gmail.com',
                                  'Test1',
                                  'Test',
                                  user_collection)
        self.assertFalse(result)
        result = main.update_user('test123',
                                  'some_email@gmail.com',
                                  'Test',
                                  'Test',
                                  user_collection)
        self.assertFalse(result)
        result = main.update_user('test 123',
                                  'some_email@gmail.com',
                                  'Test',
                                  'Test',
                                  user_collection)
        self.assertFalse(result)
        result = main.update_user('test123',
                                  'some_email@gmail.com',
                                  'Test',
                                  '123124',
                                  user_collection)
        self.assertFalse(result)

    @patch('users.UserCollection.delete_user')
    def test_mock_delete_user(self, mock_delete_user):
        '''
        Test delete_user method with mock
        '''
        # Set mock return value
        mock_delete_user.return_value = True
        # Test delete_user function success
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        main.load_users(filename, user_collection)
        result = main.delete_user('dave03', user_collection)
        self.assertTrue(result)
        self.assertTrue(mock_delete_user.called)
        # self.assertTrue('dave03' not in user_collection.database)
        # Set mock return value
        mock_delete_user.return_value = False
        # Test delete_user function failure
        result = main.delete_user('test123', user_collection)
        self.assertFalse(result)
        self.assertTrue(mock_delete_user.called)

    def test_delete_user(self):
        '''
        Test delete_user method
        '''
        # Test delete_user function success
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        main.load_users(filename, user_collection)
        result = main.delete_user('dave03', user_collection)
        self.assertTrue(result)
        self.assertTrue('dave03' not in user_collection.database)
        # Test delete_user function failure
        result = main.delete_user('test123', user_collection)
        self.assertFalse(result)

    def test_search_user(self):
        '''
        Test search_user method
        '''
        # Test search_user function success
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        main.load_users(filename, user_collection)
        result = main.search_user('dave03', user_collection)
        self.assertIsNotNone(result)
        expected = users.Users('dave03', 'david.yuen@gmail.com', 'David', 'Yuen')
        keys = ['user_id', 'email', 'user_name', 'user_last_name']
        for attr in keys:
            self.assertEqual(getattr(result, attr), getattr(expected, attr))
        # Test search_user function failure
        result = main.search_user('test123', user_collection)
        self.assertIsNone(result)

    def test_add_status(self):
        '''
        Test add_status method
        '''
        # Test add_status function success
        status_collection = main.init_status_collection()
        result = main.add_status('mbak79',
                                 'mbak79_00001',
                                 'Still doing homework!',
                                 status_collection)
        self.assertTrue(result)
        self.assertEqual(status_collection.database['mbak79_00001'].status_id,
                         'mbak79_00001')
        self.assertEqual(status_collection.database['mbak79_00001'].user_id,
                         'mbak79')
        self.assertEqual(status_collection.database['mbak79_00001'].status_text,
                         'Still doing homework!')
        # Test add_user function failure
        result = main.add_status('mbak79',
                                 'mbak79_00001',
                                 'Still doing more homework!',
                                 status_collection)
        self.assertFalse(result)
        self.assertEqual(status_collection.database['mbak79_00001'].status_id,
                         'mbak79_00001')
        self.assertEqual(status_collection.database['mbak79_00001'].user_id,
                         'mbak79')
        self.assertEqual(status_collection.database['mbak79_00001'].status_text,
                         'Still doing homework!')
        result = main.add_status('mbake152',
                                 'mbake152_asdfaa',
                                 'Still doing more homework!',
                                 status_collection)
        self.assertFalse(result)

    def test_update_status(self):
        '''
        Test update_status method
        '''
        # Test update_status function success
        status_collection = main.init_status_collection()
        filename = os.path.join('test_files', 'test_good_status_updates.csv')
        main.load_status_updates(filename, status_collection)
        result = main.update_status('dave03_00001',
                                    'dave04',
                                    'Dave has a new status!',
                                    status_collection)
        self.assertEqual(status_collection.database['dave03_00001'].user_id,
                         'dave04')
        self.assertEqual(status_collection.database['dave03_00001'].status_text,
                         'Dave has a new status!')
        self.assertTrue(result)
        # Test update_status function failure
        result = main.update_status('test123_00001',
                                    'test123',
                                    'Twitter is dumb',
                                    status_collection)
        self.assertFalse(result)
        result = main.update_status('test123_kljlkasdf',
                                    'test123',
                                    'Twitter is dumb',
                                    status_collection)
        self.assertFalse(result)
        result = main.update_status('test123_00001',
                                    'test 123',
                                    'Twitter is dumb',
                                    status_collection)
        self.assertFalse(result)
        result = main.update_status('test123_00001',
                                    'test123',
                                    1231,
                                    status_collection)
        self.assertFalse(result)

    def test_delete_status(self):
        '''
        Test delete_status method
        '''
        # Test delete_status function success
        status_collection = main.init_status_collection()
        filename = os.path.join('test_files', 'test_good_status_updates.csv')
        main.load_status_updates(filename, status_collection)
        result = main.delete_status('dave03_00001', status_collection)
        self.assertTrue(result)
        self.assertTrue('dave03_00001' not in status_collection.database)
        # Test delete_status function failure
        result = main.delete_status('test123', status_collection)
        self.assertFalse(result)

    def test_search_status(self):
        '''
        Test search_status method
        '''
        # Test search_status function success
        status_collection = main.init_status_collection()
        filename = os.path.join('test_files', 'test_good_status_updates.csv')
        main.load_status_updates(filename, status_collection)
        result = main.search_status('dave03_00001', status_collection)
        self.assertIsNotNone(result)
        expected = user_status.UserStatus('dave03_00001', 'dave03', 'Sunny in Seattle this morning')
        keys = ['status_id', 'user_id', 'status_text']
        for attr in keys:
            self.assertEqual(getattr(result, attr), getattr(expected, attr))
        # Test search_user function failure
        result = main.search_status('test123_00001', status_collection)
        self.assertFalse(result)

    def test_validate_user_id(self):
        '''
        Tests validate_user_id method
        '''
        # Tests valid user_ids
        for user_id in ['dave03', 'evmiles97', 'mbakke63', 'andy14']:
            self.assertTrue(main.validate_user_id(user_id))
        # Test invalid user_ids
        for user_id in ['asdf 123', '123141']:
            self.assertFalse(main.validate_user_id(user_id))

    def test_validate_email(self):
        '''
        Tests validate_email method
        '''
        # Tests valid emails
        for email in ['marcusabakke@gmail.com', 'andy.miles@uw.edu', 'some_email@yahoo.com']:
            self.assertTrue(main.validate_email(email))
        # Test invalid emails
        for email in ['marcus bakke@gmail.com', 'marcus@gmail', 'marcus@g.g.mail.', '.asldkfjl']:
            self.assertFalse(main.validate_email(email))

    def test_validate_name(self):
        '''
        Tests validate_name method
        '''
        # Tests valid name
        for name in ['hello', 'my', 'Name', 'is', 'MarCus']:
            self.assertTrue(main.validate_name(name))
        # Test invalid user_ids
        for name in ['this has a space', '123141', 'Marcus-3000']:
            self.assertFalse(main.validate_name(name))

    def test_validate_status_id(self):
        '''
        Test validate_status_id method
        '''
        # Tests valid status_id
        for status_id in ['dave03_00001',
                   'evmiles97_00003',
                   'mbakke63_09813',
                   'andy14_87123']:
            self.assertTrue(main.validate_status_id(status_id))
        # Test invalid status_id
        for status_id in ['asdf_1231_1231',
                   'asdf1239874',
                   'dave03_hello',
                   'mbakke53_12.124',
                   'asdf 123_12345']:
            self.assertFalse(main.validate_status_id(status_id))

    def test_validate_status_text(self):
        '''
        Test validate_status_text method
        '''
        # Tests valid status_text
        for text in ['some text']:
            self.assertTrue(main.validate_status_text(text))
        # Test invalid status_text
        for text in [1234, 12314.0, {'dict': 'hello'}, (1, 2), [1, 2, 3]]:
            self.assertFalse(main.validate_status_text(text))

    def tearDown(self):
        '''
        Tear Down function to delete saved files
        '''
        logging.disable(logging.NOTSET)
        delete = [os.path.join('test_files', 'saved_add_accounts.csv'),
                  os.path.join('test_files', 'saved_status_updates.csv')]
        for file in delete:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()

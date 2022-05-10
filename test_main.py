'''
Unittest module.
Disable "Too many public methods" pylint message.
'''
# pylint: disable=R0904
import unittest
import os
import peewee as pw
import users
import user_status
import main
import socialnetwork_model as sm

MODELS = [sm.Users, sm.Status]
test_db = pw.SqliteDatabase(':memory:')

class TestMain(unittest.TestCase):
    '''
    Test class for main.py
    '''
    def setUp(self):
        '''
        setUp method to disable logging.
        '''
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        test_db.execute_sql('PRAGMA foreign_keys = ON;')
        self.user_collection = users.UserCollection()
        self.status_collection = user_status.UserStatusCollection()

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
        self.assertEqual(user_status_collection.database, sm.Status)

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
        # Load some user data
        main.load_users(os.path.join('test_files',
                                     'test_good_accounts.csv'),
                        self.user_collection)
        # Test good status
        result = main.load_status_updates(os.path.join('test_files',
                                                       'test_good_status_updates.csv'),
                                          self.status_collection)
        self.assertTrue(result)
        expected = [['evmiles97_00001', 'evmiles97', 'Code is finally compiling'],
                    ['dave03_00001', 'dave03', 'Sunny in Seattle this morning'],
                    ['evmiles97_00002', 'evmiles97', 'Perfect weather for a hike']]
        for i, status in enumerate(self.status_collection.database):
            self.assertEqual(status.status_id, expected[i][0])
            self.assertEqual(status.user.user_id, expected[i][1])
            self.assertEqual(status.status_text, expected[i][2])
        # Test bad status
        result = main.load_status_updates(os.path.join('test_files',
                                                       'test_bad_status_updates.csv'),
                                          self.status_collection)
        self.assertFalse(result)


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
        # Load some user data
        main.load_users(os.path.join('test_files',
                                     'test_good_accounts.csv'),
                        self.user_collection)
        # Test add_status function success
        inputs = ['evmiles97',
                  'evmiles97_00003',
                  'Still doing homework!',
                  self.status_collection]
        result = main.add_status(*inputs)
        self.assertTrue(result)
        status = self.status_collection.database.get(self.status_collection.database.status_id == inputs[1])
        self.assertEqual(status.user.user_id, inputs[0])
        self.assertEqual(status.status_id, inputs[1])
        self.assertEqual(status.status_text, inputs[2])
        # Test add_status function failure
        inputs = ['mbakke63',
                  'mbakke63_00001',
                  'This fails!',
                  self.status_collection]
        result = main.add_status(*inputs)
        self.assertFalse(result)
        # Test invalid inputs
        inputs = ['mba_kke63_00001',
                  'mbakke63',
                  'This fails!',
                  self.status_collection]
        result = main.add_status(*inputs)
        self.assertFalse(result)

    def test_update_status(self):
        '''
        Test update_status method
        '''
        # Load some user data
        main.load_users(os.path.join('test_files',
                                     'test_good_accounts.csv'),
                        self.user_collection)
        # Load some status data
        main.load_status_updates(os.path.join('test_files',
                                              'test_good_status_updates.csv'),
                                 self.status_collection)
        # Test update_status function success
        inputs = ['evmiles97_00001',
                  'evmiles97',
                  'Still doing homework!',
                  self.status_collection]
        result = main.update_status(*inputs)
        self.assertTrue(result)
        status = self.status_collection.database.get(self.status_collection.database.status_id == inputs[0])
        self.assertEqual(status.status_id, inputs[0])
        self.assertEqual(status.user.user_id, inputs[1])
        self.assertEqual(status.status_text, inputs[2])
        # Test add_status function failure
        inputs = ['mbakke63_00001',
                  'mbakke63',
                  'This fails!',
                  self.status_collection]
        result = main.update_status(*inputs)
        self.assertFalse(result)
        # Test invalid inputs
        inputs = ['mba_kke63_00001',
                  'mbakke63',
                  'This fails!',
                  self.status_collection]
        result = main.update_status(*inputs)
        self.assertFalse(result)

    def test_delete_status(self):
        '''
        Test delete_status method
        '''
        # Load some user data
        main.load_users(os.path.join('test_files',
                                     'test_good_accounts.csv'),
                        self.user_collection)
        # Load some status data
        main.load_status_updates(os.path.join('test_files',
                                              'test_good_status_updates.csv'),
                                 self.status_collection)
        # Test delete_status function success
        inputs = ['evmiles97_00001', self.status_collection]
        result = main.delete_status(*inputs)
        self.assertTrue(result)
        status = self.status_collection.database.get_or_none(self.status_collection.database.status_id == inputs[0])
        self.assertIsNone(status)
        # Test add_status function failure
        inputs = ['mbakke63_00001', self.status_collection]
        result = main.delete_status(*inputs)
        self.assertFalse(result)

    def test_search_status(self):
        '''
        Test search_status method
        '''
        # Load some user data
        main.load_users(os.path.join('test_files',
                                     'test_good_accounts.csv'),
                        self.user_collection)
        # Load some status data
        main.load_status_updates(os.path.join('test_files',
                                              'test_good_status_updates.csv'),
                                 self.status_collection)
        # Test search_status function success
        inputs = ['evmiles97_00001', self.status_collection]
        status = main.search_status(*inputs)
        self.assertEqual(status.status_id, 'evmiles97_00001')
        self.assertEqual(status.user.user_id, 'evmiles97')
        self.assertEqual(status.status_text, 'Code is finally compiling')
        # Test search_status function failure
        inputs = ['mbakke63_00001', self.status_collection]
        result = main.search_status(*inputs)
        self.assertIsNone(result)

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

    def test_validate_status_inputs(self):
        '''
        Test validate_status_inputs method
        '''
        # Test valid inputs
        inputs = [['dave03_00001', 'dave03', 'test1'],
                  ['evmiles97_00003', 'evmiles97', 'test2'],
                  ['mbakke63_09813', 'mbakke63', 'test3'],
                  ['andy14_87123', 'andy14', 'test4']]
        for inp in inputs:
            self.assertTrue(main.validate_status_inputs(*inp))
        # Test invalid inputs
        inputs = [['asdf_1231_1231', 'asdf_1231', 'test1'],
                  ['asdf1239874', 'asdf1239874', 'test2'],
                  ['dave03_hello', 'dave03', 'test3'],
                  ['mbakke53_12.124', 'mbakke53_12', 'test4'],
                  ['asdf 123_12345', 'asdf 123', 'test5'],
                  ['asdf123_12345', 'asdf 123', 'test5'],
                  ['asdf123_12345', 'asdf123', 1],
                  ['asdf123_12345', 'asdf123', (1, 1)],
                  ['asdf123_12345', 'asdf123', {}]]
        for inp in inputs:
            self.assertFalse(main.validate_status_inputs(*inp))

    def tearDown(self):
        '''
        Remove all tables at end of each test and close db.
        '''
        test_db.drop_tables(MODELS)
        test_db.close()

if __name__ == '__main__':
    unittest.main()

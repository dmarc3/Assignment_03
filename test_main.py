'''
Unittest module.
Disable "Too many public methods" pylint message.
Authors: Kathleen Wong and Marcus Bakke
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
        Author: Kathleen Wong
        '''
        user_collection = main.init_user_collection()
        self.assertEqual(type(user_collection), type(users.UserCollection()))
        self.assertEqual(user_collection.database, sm.Users)

    def test_init_status_collection(self):
        '''
        Test UserStatusCollection initialization
        Author: Marcus Bakke
        '''
        user_status_collection = main.init_status_collection()
        self.assertEqual(type(user_status_collection), type(user_status.UserStatusCollection()))
        self.assertEqual(user_status_collection.database, sm.Status)

    def test_load_users(self):
        '''
        Test load_users method
        Author: Kathleen Wong
        '''
        # Test good accounts
        user_collection = main.init_user_collection()
        filename = os.path.join('test_files', 'test_good_accounts.csv')
        result = main.load_users(filename, user_collection)
        expected = [['evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles'],
                   ['dave03', 'david.yuen@gmail.com', 'David', 'Yuen']]
        self.assertTrue(result)
        for i, user in enumerate(self.user_collection.database):
            self.assertEqual(user.user_id, expected[i][0])
            self.assertEqual(user.user_email, expected[i][1])
            self.assertEqual(user.user_name, expected[i][2])
            self.assertEqual(user.user_last_name, expected[i][3])
        fail = main.load_status_updates(os.path.join('test_files',
                                                       'test_bad_accounts_1.csv'),
                                          self.status_collection)
        self.assertFalse(fail)
        fake = main.load_users(filename, user_collection)
        self.assertFalse(fake)

    def test_add_user(self):
        '''
        Test add_user method
        Author: Kathleen Wong
        '''
        # Test add_user function success
        user_collection = main.init_user_collection()
        result = main.add_user('kwong', 'kwong@gmail.com', 'Kathleen', 'Wong', user_collection)
        self.assertTrue(result)
        fail = main.add_user('kwong', 'kwong@gmail.com', 'Kathleen', 'Wong', user_collection)
        self.assertFalse(fail)
        email = main.add_user('kwong', 'kwong', 'Kathleen', 'Wong', user_collection)
        self.assertFalse(email)
        user_id = main.add_user('k wong', 'kwong@gmail.com', 'Kathleen', 'Wong', user_collection)
        self.assertFalse(user_id)
        user_name = main.add_user('name', 'kwong@gmail.com', 'kathleen123',
                                  'wong123', user_collection)
        self.assertFalse(user_name)
        user_last_name = main.add_user('name', 'kwong@gmail.com',
                                       'kathleen', 'wong123', user_collection)
        self.assertFalse(user_last_name)

    def test_update_user(self):
        '''
        Test update_user method
        Author: Kathleen Wong
        '''
        # Test update_user function success
        user_collection = main.init_user_collection()
        main.add_user('dave03', 'dave@gmail.com', 'dave', 'yuen', user_collection)
        result = main.update_user('dave03',
                                  'newemail@gmail.com',
                                  'Notdave',
                                  'Notyuen',
                                  user_collection)
        user = user_collection.database.get(user_collection.database.user_id == 'dave03')
        self.assertEqual(user.user_email, 'newemail@gmail.com')
        self.assertEqual(user.user_name, 'Notdave')
        self.assertEqual(user.user_last_name, 'Notyuen')
        self.assertTrue(result)
        fail = main.update_user('fail', 'fail@gmail.com', 'Fail', 'Test', user_collection)
        self.assertFalse(fail)
        email = main.update_user('dave03', 'fail',  'Fail', 'Test', user_collection)
        self.assertFalse(email)

    def test_delete_user(self):
        '''
        Test delete_user method
        Author: Kathleen Wong
        '''
        user_collection = main.init_user_collection()
        main.add_user('dave03', 'dave@gmail.com', 'dave', 'yuen', user_collection)
        result = main.delete_user('dave03', user_collection)
        self.assertTrue(result)
        fail = main.delete_user('fail', user_collection)
        self.assertFalse(fail)

    def test_search_user(self):
        '''
        Test search_user method
        Author: Kathleen Wong
        '''
        user_collection = main.init_user_collection()
        main.add_user('dave03', 'dave@gmail.com', 'dave', 'yuen', user_collection)
        result = main.search_user('dave03', user_collection)
        self.assertTrue(result)
        fail = main.search_user('fail', user_collection)
        self.assertIsNone(fail)

    def test_add_status(self):
        '''
        Test add_status method
        Author: Marcus Bakke
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
        status = self.status_collection.database.get(
                 self.status_collection.database.status_id == inputs[1])
        self.assertEqual(status.user_id,
                         inputs[0])
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
        fail = main.add_status('fake', 'faketest', 'fake', self.status_collection)
        self.assertFalse(fail)

    def test_update_status(self):
        '''
        Test update_status method
        Author: Marcus Bakke
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
        status = self.status_collection.database.get(
                 self.status_collection.database.status_id == inputs[0])
        self.assertEqual(status.status_id, inputs[0])
        self.assertEqual(status.user_id, inputs[1])
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
        bad_results = main.load_status_updates(os.path.join('test_files',
                                              'test_bad_status_updates.csv'),
                                 self.status_collection)
        self.assertFalse(bad_results)
        bad_format_results = main.load_status_updates(os.path.join('test_files',
                                              'test_bad_status_updates_2.csv'),
                                 self.status_collection)
        self.assertFalse(bad_format_results)
        fake = main.load_status_updates(os.path.join('test_files',
                                              'fake.csv'),
                                 self.status_collection)
        self.assertFalse(fake)

    def test_delete_status(self):
        '''
        Test delete_status method
        Author: Marcus Bakke
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
        status = self.status_collection.database.get_or_none(
                 self.status_collection.database.status_id == inputs[0])
        self.assertIsNone(status)
        # Test add_status function failure
        inputs = ['mbakke63_00001', self.status_collection]
        result = main.delete_status(*inputs)
        self.assertFalse(result)

    def test_search_status(self):
        '''
        Test search_status method
        Author: Marcus Bakke
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
        self.assertEqual(status.user_id, 'evmiles97')
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
        Author: Marcus Bakke
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

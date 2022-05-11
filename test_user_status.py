'''
Unittests for user_status.py.
Author: Marcus Bakke
'''
import unittest
import peewee as pw
import user_status
import socialnetwork_model as sm

MODELS = [sm.Users, sm.Status]
test_db = pw.SqliteDatabase(':memory:')

class TestUserStatus(unittest.TestCase):
    '''
    Test class for user_status.py
    '''
    def setUp(self):
        '''
        Bind model classes to test database. Initialize collection.
        '''
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        test_db.execute_sql('PRAGMA foreign_keys = ON;')
        sm.Users.create(user_id='test123',
                        user_email='test@email.com',
                        user_name='test',
                        user_last_name='test-test')
        self.status_collection = user_status.UserStatusCollection()
        self.status_collection.add_status('test123_00001', 'test123', 'test status')

    def test_init(self):
        '''
        Test __init__ method.
        '''
        self.assertEqual(type(self.status_collection.database), type(sm.Status))

    def test_add_status(self):
        '''
        Test add_status method.
        '''
        # Test failed add_status call
        result = self.status_collection.add_status('test123_00001', 'test123', 'test status')
        self.assertFalse(result)
        # Test successful add_status call
        result = self.status_collection.add_status('test123_00002', 'test123', 'test status 2')
        self.assertTrue(result)
        logical_query = self.status_collection.database.status_id == 'test123_00002'
        status = self.status_collection.database.get(logical_query)
        self.assertEqual('test123_00002', status.status_id)
        self.assertEqual('test status 2', status.status_text)
        self.assertEqual('test123', status.user.user_id)

    def test_modify_status(self):
        '''
        Test modify_status method.
        '''
        # Test failed modify_status call
        result = self.status_collection.modify_status('test123_00002',
                                                      'test123',
                                                      'test modify status')
        self.assertFalse(result)
        # Test successful modify_status call
        result = self.status_collection.modify_status('test123_00001',
                                                      'test123',
                                                      'new modified status!')
        self.assertTrue(result)
        logical_query = self.status_collection.database.status_id == 'test123_00001'
        status = self.status_collection.database.get(logical_query)
        self.assertEqual('test123_00001', status.status_id)
        self.assertEqual('new modified status!', status.status_text)
        self.assertEqual('test123', status.user.user_id)

    def test_delete_status(self):
        '''
        Test delete_status method.
        '''
        # Test failed delete_status call
        result = self.status_collection.delete_status('test123_00002')
        self.assertFalse(result)
        # Test successful delete_status call
        result = self.status_collection.delete_status('test123_00001')
        self.assertTrue(result)
        logical_query = self.status_collection.database.status_id == 'test123_00001'
        status = self.status_collection.database.get_or_none(logical_query)
        self.assertIsNone(status)

    def test_search_status(self):
        '''
        Test search_status method.
        '''
        # Test failed delete_status call
        status = self.status_collection.search_status('test123_00002')
        self.assertFalse(status)
        # Test successful delete_status call
        status = self.status_collection.search_status('test123_00001')
        self.assertEqual('test123_00001', status.status_id)
        self.assertEqual('test status', status.status_text)
        self.assertEqual('test123', status.user.user_id)

    def tearDown(self):
        '''
        Remove all tables at end of each test and close db.
        '''
        test_db.drop_tables(MODELS)
        test_db.close()

if __name__ == '__main__':
    unittest.main()

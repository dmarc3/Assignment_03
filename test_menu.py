'''
Unittest module.
Disable "Too many public methods" pylint message.

Marcus: I mistakenly read the "Test menu.py" section of the README.md
and took it literally... I started writing all these unittests and
realized only after I was complete that I didn't need to do this. Oh
well... helped me find all of the bugs and practice mocking / patching
'''
# pylint: disable=R0904
import unittest
import os
import logging
from io import StringIO
from mock import patch
import main
import menu

class TestMenu(unittest.TestCase):
    '''
    Test class for menu.py
    '''
    def setUp(self):
        '''
        setUp method to initialize collections.
        Author: Marcus Bakke
        '''
        # Disable logger
        logging.disable(logging.CRITICAL)
        # User collection
        menu.user_collection = main.init_user_collection()
        main.load_users(os.path.join('test_files', 'test_good_accounts.csv'),
                        menu.user_collection)
        # Status collection
        menu.status_collection = main.init_status_collection()
        main.load_status_updates(os.path.join('test_files', 'test_good_status_updates.csv'),
                                 menu.status_collection)

    @patch('builtins.input')
    @patch('main.load_status_updates')
    def test_load_status_updates(self, mock_load, mock_input):
        '''
        Test load_status_updates method
        Author: Marcus Bakke
        '''
        test_file = os.path.join('test_files',
                                 'test_good_status_updates.csv')
        mock_input.return_value = test_file
        menu.load_status_updates()
        self.assertTrue(mock_input.called)
        self.assertTrue(mock_load.called)

    @patch('builtins.input')
    @patch('main.add_status')
    def test_add_status(self, mock_add, mock_input):
        '''
        Test add_status method
        Author: Marcus Bakke
        '''
        # Successful add_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_add.return_value = True
            mock_input.side_effect = ['mbakke63', 'mbakke63_00001', 'Test status 1']
            menu.add_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_add.called)
            self.assertEqual(output.getvalue(),
                             'New status was successfully added\n')
        # Failed add_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_add.return_value = False
            mock_input.side_effect = ['mbakke63', 'mbakke63_lkajsldkfj', 'Test status 2']
            menu.add_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_add.called)
            self.assertEqual(output.getvalue(),
                             'An error occurred while trying to add new status\n')

    @patch('builtins.input')
    @patch('main.update_status')
    def test_update_status(self, mock_update, mock_input):
        '''
        Test update_status method
        Author: Marcus Bakke
        '''
        # Successful update_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_update.return_value = True
            mock_input.side_effect = ['mbakke63', 'mbakke63_00001', 'Test status 1']
            menu.update_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_update.called)
            self.assertEqual(output.getvalue(),
                             'Status was successfully updated\n')
        # Failed update_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_update.return_value = False
            mock_input.side_effect = ['test123', 'test123_00001', 'Test status 2']
            menu.update_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_update.called)
            self.assertEqual(output.getvalue(),
                             'An error occurred while trying to update status\n')

    @patch('builtins.input')
    @patch('main.search_status')
    def test_search_status(self, mock_search, mock_input):
        '''
        Test search_status method
        Author: Marcus Bakke
        '''
        # Successful search_status call
        with patch('sys.stdout', new=StringIO()) as output:
            status_id = 'evmiles97_00002'
            mock_search.return_value = menu.status_collection.database[status_id]
            mock_input.return_value = status_id
            menu.search_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_search.called)
            self.assertEqual(output.getvalue(),
                            'User ID: evmiles97\n' \
                            'Status ID: evmiles97_00002\n' \
                            'Status text: Perfect weather for a hike\n')
        # Failed search_status call
        with patch('sys.stdout', new=StringIO()) as output:
            status_id = 'evmiles97_00002'
            mock_search.return_value = None
            mock_input.return_value = status_id
            menu.search_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_search.called)
            self.assertEqual(output.getvalue(),
                            'ERROR: Status does not exist\n')

    @patch('builtins.input')
    @patch('main.delete_status')
    def test_delete_status(self, mock_delete, mock_input):
        '''
        Test delete_status method
        Author: Marcus Bakke
        '''
        # Successful delete_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_delete.return_value = True
            mock_input.return_value = 'evmiles97_00002'
            menu.delete_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_delete.called)
            self.assertEqual(output.getvalue(),
                            'Status was successfully deleted\n')
        # Failed delete_status call
        with patch('sys.stdout', new=StringIO()) as output:
            mock_delete.return_value = False
            mock_input.return_value = 'evmiles97_00002'
            menu.delete_status()
            self.assertTrue(mock_input.called)
            self.assertTrue(mock_delete.called)
            self.assertEqual(output.getvalue(),
                            'An error occurred while trying to delete status\n')

    @patch('builtins.input')
    @patch('main.save_status_updates')
    def test_save_status(self, mock_save, mock_input):
        '''
        Test save_status method
        Author: Marcus Bakke
        '''
        mock_input.return_value = 'fake_file.csv'
        menu.save_status()
        self.assertTrue(mock_input.called)
        self.assertTrue(mock_save.called)

    @patch('sys.exit')
    def test_quit_program(self, mock_exit):
        '''
        Test quit_program method
        Author: Marcus Bakke
        '''
        menu.quit_program()
        self.assertTrue(mock_exit.called)

    def tearDown(self):
        '''
        tearDown method.
        Author: Marcus Bakke
        '''
        logging.disable(logging.NOTSET)




if __name__ == '__main__':
    unittest.main()

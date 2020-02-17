import unittest
import unittest.mock as umock
from Helpers import reader
import os


class TestReader(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join('input_files', 'test_input.txt')

    def test_get_list_from_file(self):
        test_file_content = 'King Crimson\nDio'
        m = umock.mock_open(read_data=test_file_content)
        with umock.patch('builtins.open', m) as m_open:
            result = reader.get_list_from_file(self.path)
            m_open.assert_called_once_with(self.path)
            self.assertEqual(result,test_file_content.split('\n'))
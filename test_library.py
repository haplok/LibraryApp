import unittest
import json
import os
from io import StringIO
from unittest.mock import patch

import controllers
from models import Library


class TestController(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_library.json'
        self.books = [{
            "id": 1,
            "title": 'TEST_TITLE_01',
            "author": 'TEST_AUTHOR_01',
            "year": '2000',
            "status": 'в наличии'},
            {
                "id": 3,
                "title": 'TEST_TITLE_02',
                "author": 'TEST_AUTHOR_02',
                "year": '2001',
                "status": 'выдана'}]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book for book in self.books], file, ensure_ascii=False, indent=4)

        self.library = Library(self.filename)
        self.controller = controllers.LibraryController(self.library)

    def tearDown(self):
        pass
        os.remove(self.filename)

    @patch('builtins.input', side_effect=['TEST_TITLE_03', 'TEST_AUTHOR_02', '2023', ''])
    def test_add_book(self, _):
        """
        Тест добавления книги через контроллер
        """
        self.controller.add_book()
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[2].title, 'TEST_TITLE_03')
        self.assertEqual(self.library.books[2].author, 'TEST_AUTHOR_02')
        self.assertEqual(self.library.books[2].year, '2023')

    @patch('builtins.input', side_effect=['3', ''])
    def test_remove_book(self, _):
        """
        Тест удаления книги через контроллер
        """
        self.controller.remove_book()
        sample = [{
            "id": 1,
            "title": "TEST_TITLE_01",
            "author": "TEST_AUTHOR_01",
            "year": "2000",
            "status": "в наличии"}, ]
        self.assertEqual([book.to_dict() for book in self.library.books], sample)

    @patch('builtins.input', side_effect=['2001', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_book(self, mock_output, _):
        """
        Тест поска книг через контроллер
        """
        self.controller.search_books()
        sample = "3. TEST_TITLE_02 - TEST_AUTHOR_02 (2001) [выдана]"
        self.assertEqual(mock_output.getvalue().strip(), sample)

    @patch('builtins.input', side_effect=[''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_books(self, mock_output, _):
        """
        Тест вывода всех книг через контроллер
        """
        self.controller.display_books()
        sample = ("1. TEST_TITLE_01 - TEST_AUTHOR_01 (2000) [в наличии]\n3. TEST_TITLE_02 - TEST_AUTHOR_02 (2001) ["
                  "выдана]")
        self.assertEqual(mock_output.getvalue().strip(), sample)

    @patch('builtins.input', side_effect=['1', 'выдана', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_book_status(self, mock_output, _):
        """
        Тест изменения статуса книги через контроллер
        """
        self.controller.change_book_status()
        self.assertEqual(self.library.books[0].status, 'выдана')
        sample = "Статус книги 'TEST_TITLE_01' изменен на 'выдана'"
        self.assertEqual(mock_output.getvalue().strip(), sample)

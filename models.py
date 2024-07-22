import json
import os
from typing import List, Optional


class Book:
    """
    Класс для представления книги в библиотеке.

    Attributes:
        id (int): Уникальный идентификатор, генерируется автоматически.
        title (str): Название книги.
        author (str): Автор книги.
        year (str): Год издания книги.
        status (str): Статус книги ("в наличии" по умолчанию).
    """

    def __init__(self, book_id: int, title: str, author: str, year: str, status: str = "в наличии") -> None:
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует объект Book в словарь.

        Returns:
            dict: Словарь с данными книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """
        Создает объект Book из словаря.

        Args:
            data (dict): Словарь с данными книги.

        Returns:
            Book: Новый объект Book.
        """
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    """
    Класс для управления библиотекой книг.

    Attributes:
        filename (str): Имя файла для сохранения данных библиотеки.
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self, filename: str = 'library.json') -> None:
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        """
        Загружает книги из файла.

        Returns:
            List[Book]: Список загруженных книг.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book.from_dict(item) for item in data]
        return []

    def save_books(self) -> None:
        """
        Сохраняет книги в файл.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: str) -> Book:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (str): Год издания книги.

        Returns:
            Book: Новая добавленная книга.
        """
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        return new_book

    def remove_book(self, book_id: int) -> Optional[Book]:
        """
        Удаляет книгу из библиотеки по ID.

        Args:
            book_id (int): Идентификатор книги.

        Returns:
            Optional[Book]: Удаленная книга или None, если книга не найдена.

        Raises:
            ValueError: Если книга с указанным ID не найдена.
        """
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            return book
        else:
            raise ValueError(f"Книга с id {book_id} не найдена")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Находит книгу по ID.

        Args:
            book_id (int): Идентификатор книги.

        Returns:
            Optional[Book]: Найденная книга или None, если книга не найдена.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(self, keyword: str) -> List[Book]:
        """
        Ищет книги по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска (может быть частью названия, автора или года).

        Returns:
            List[Book]: Список книг, соответствующих ключевому слову.
        """
        return [book for book in self.books if (keyword.lower() in book.title.lower()) or (
                keyword.lower() in book.author.lower()) or (str(book.year) == keyword)]

    def change_book_status(self, book_id: int, new_status: str) -> Optional[Book]:
        """
        Изменяет статус книги.

        Args:
            book_id (int): Идентификатор книги.
            new_status (str): Новый статус книги.

        Returns:
            Optional[Book]: Обновленная книга или None, если книга не найдена.

        Raises:
            ValueError: Если книга с указанным ID не найдена.
        """
        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status
            self.save_books()
            return book
        else:
            raise ValueError(f"Книга с id {book_id} не найдена")

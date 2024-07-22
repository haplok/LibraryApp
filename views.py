from models import Book
from typing import List


def display_books(books: List[Book]) -> None:
    """
    Функция отображения списка подходящих книг или их отсутствие.

    Args:
        books (List[Book]): Список подходящих книг.

    Returns:
        None
    """
    if books:
        for book in books:
            print(f"{book.id}. {book.title} - {book.author} ({book.year}) [{book.status}]")
    else:
        print("Библиотека пуста")


def display_message(message: str) -> None:
    """
    Функция отображения текста.

    Args:
        message (str): Текст для отображения.

    Returns:
        None
    """
    print(message)

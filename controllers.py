from views import display_books, display_message
from os import system
from typing import Callable, Any


def clear_scr(func: Callable) -> Callable:
    """
    Декоратор для очистки экрана перед выполнением функции и ожидания нажатия Enter после.

    Args:
        func (Callable): Функция, которую нужно обернуть.

    Returns:
        Callable: Обернутая функция.
    """

    def wrapper(*args, **kwargs) -> Any:
        system('cls')
        result = func(*args, **kwargs)
        input('''
        *Нажмите Enter для возврата в главное меню*''')
        return result

    return wrapper


class LibraryController:
    """
    Класс для управления библиотекой через взаимодействие с пользователем.

    Attributes:
        library: Экземпляр класса Library.
    """

    def __init__(self, library) -> None:
        self.library = library

    @clear_scr
    def add_book(self) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Returns:
            None
        """
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = input("Введите год издания книги: ")
        book = self.library.add_book(title, author, year)
        display_message(f"Книга '{book.title}' добавлена с id {book.id}")

    @clear_scr
    def remove_book(self) -> None:
        """
        Удаляет книгу из библиотеки по ID.

        Returns:
            None
        """
        try:
            book_id = int(input("Введите id книги для удаления: "))
            book = self.library.remove_book(book_id)
            display_message(f"Книга '{book.title}' удалена")
        except ValueError as e:
            display_message(str(e))

    @clear_scr
    def search_books(self) -> None:
        """
        Ищет книги в библиотеке по ключевому слову.

        Returns:
            None
        """
        keyword = input("Введите ключевое слово для поиска (название, автор или год): ")
        results = self.library.search_books(keyword)
        display_books(results)

    @clear_scr
    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.

        Returns:
            None
        """
        display_books(self.library.books)

    @clear_scr
    def change_book_status(self) -> None:
        """
        Изменяет статус книги в библиотеке по ID.

        Returns:
            None
        """
        try:
            book_id = int(input("Введите id книги для изменения статуса: "))
            new_status = input("Введите новый статус книги ('в наличии' или 'выдана'): ").lower()
            if new_status in ('в наличии', 'выдана'):
                book = self.library.change_book_status(book_id, new_status)
                display_message(f"Статус книги '{book.title}' изменен на '{book.status}'")
            else:
                display_message(f"Введен неправильный статус: {new_status}")
        except ValueError as e:
            display_message(str(e))

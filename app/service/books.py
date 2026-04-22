from app.repositories.books import (
    create_book,
    get_book,
    get_all_books,
    update_book,
    delete_book
)
from app.logger import setup_logger

logger = setup_logger()

async def service_create_book(session, title: str, author: str, price: float, stock_quantity: int):
    if not title or not author or price < 0 or stock_quantity < 0:
        logger.warning("Некорректные данные книги.")
        return None

    book = await create_book(session, title, author, price, stock_quantity)
    if book:
        logger.info(f"Успешно создана книга: {book['title']} (ID: {book['id']})")
    return book


async def service_get_book(session, book_id: int):
    book = await get_book(session, book_id)
    if not book:
        logger.warning(f"Книга с ID {book_id} не найдена.")
    return book


async def service_get_all_books(session):
    books = await get_all_books(session)
    logger.debug(f"Получено {len(books)} книг.")
    return books


async def service_update_book(session, book_id: int, title=None, author=None, price=None, stock_quantity=None):
    if not any([title, author, price, stock_quantity]):
        logger.warning("Нечего обновлять.")
        return None

    book = await update_book(session, book_id, title, author, price, stock_quantity)
    if book:
        logger.info(f"Книга {book_id} обновлена: {book}")
    else:
        logger.error(f"Не удалось обновить книгу {book_id}.")
    return book


async def service_delete_book(session, book_id: int):
    success = await delete_book(session, book_id)
    if success:
        logger.info(f"Книга {book_id} удалена.")
    else:
        logger.warning(f"Не удалось удалить книгу {book_id}.")
    return success
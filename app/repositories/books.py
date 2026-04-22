import aiomysql
from app.logger import setup_logger

logger = setup_logger()

async def create_book(conn, title, author, price, stock_quantity):
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "INSERT INTO books_new (title, author, price, stock_quantity) VALUES (%s, %s, %s, %s)",
                (title, author, price, stock_quantity)
            )
            await conn.commit()
            logger.debug(f"Создана новая книга с названием {title}")

            last_id = cursor.lastrowid
            await cursor.execute(
                "SELECT book_id, title, author, price, stock_quantity FROM books_new WHERE book_id = %s",
                (last_id,)
            )
            book = await cursor.fetchone()

            if book:
                return {
                    "id": book["book_id"],
                    "title": book["title"],
                    "author": book["author"],
                    "price": float(book["price"]),
                    "stock_quantity": book["stock_quantity"]
                }
            else:
                logger.error("Не удалось найти книгу после вставки.")
                return None
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при добавлении книги: {e.args}")
        return None

async def get_book(conn, book_id):
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT book_id, title, author, price, stock_quantity FROM books_new WHERE book_id = %s",
                (book_id,)
            )
            book = await cursor.fetchone()

            if book:
                return {
                    "id": book["book_id"],
                    "title": book["title"],
                    "author": book["author"],
                    "price": float(book["price"]),
                    "stock_quantity": book["stock_quantity"]
                }
            return None
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при получении книги: {e.args}")
        return None

async def get_all_books(conn):
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT book_id, title, author, price, stock_quantity FROM books_new"
            )
            books = await cursor.fetchall()
            return [
                {
                    "id": b["book_id"],
                    "title": b["title"],
                    "author": b["author"],
                    "price": float(b["price"]),
                    "stock_quantity": b["stock_quantity"]
                }
                for b in books
            ]
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при получении списка книг: {e.args}")
        return []

async def update_book(conn, book_id, title=None, author=None, price=None, stock_quantity=None):
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            fields = []
            values = []

            if title is not None:
                fields.append("title = %s")
                values.append(title)
            if author is not None:
                fields.append("author = %s")
                values.append(author)
            if price is not None:
                fields.append("price = %s")
                values.append(price)
            if stock_quantity is not None:
                fields.append("stock_quantity = %s")
                values.append(stock_quantity)

            if not fields:
                logger.warning("Нет полей для обновления книги.")
                return None

            values.append(book_id)
            query = f"UPDATE books_new SET {', '.join(fields)} WHERE book_id = %s"
            await cursor.execute(query, values)
            await conn.commit()
            logger.debug(f"Книга {book_id} обновлена")

            return await get_book(conn, book_id)
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при обновлении книги: {e.args}")
        return None

async def delete_book(conn, book_id):
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("DELETE FROM books_new WHERE book_id = %s", (book_id,))
            await conn.commit()
            logger.debug(f"Книга {book_id} удалена")
            return cursor.rowcount > 0
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при удалении книги: {e.args}")
        return False
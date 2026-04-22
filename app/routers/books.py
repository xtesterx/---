from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.databaseSQL import get_session
from app.service.books import (
    service_create_book,
    service_delete_book,
    service_get_all_books,
    service_get_book,
    service_update_book
)
from app.logger import setup_logger

logger = setup_logger()
router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_book(
    title: str,
    author: str,
    price: float,
    stock_quantity: int,
    session=Depends(get_session)
):
    book = await service_create_book(session, title, author, price, stock_quantity)
    if not book:
        raise HTTPException(status_code=400, detail="Не удалось создать книгу. Проверьте данные.")
    return book

@router.get("/{book_id}", response_model=dict)
async def get_book(book_id: int, session=Depends(get_session)):
    book = await service_get_book(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.get("/", response_model=List[dict])
async def get_all_books(session=Depends(get_session)):
    books = await service_get_all_books(session)
    return books

@router.put("/{book_id}", response_model=dict)
async def update_book(
    book_id: int,
    title: str = None,
    author: str = None,
    price: int = None,
    stock_quantity: int = None,
    session=Depends(get_session)
):
    book = await service_update_book(session, book_id, title, author, price, stock_quantity)
    if not book:
        raise HTTPException(status_code=400, detail="Не удалось обновить книгу")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session=Depends(get_session)):
    success = await service_delete_book(session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книга не найдена или не удалена")
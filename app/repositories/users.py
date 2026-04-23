from app.databaseSQL import get_db_connection
import jwt
from app.utils.jwt_utils import create_access_token, verify_access_token

async def create_user(name: str, phone: str, email: str, password_hash: str) -> int:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO users (name, phone, email, password_hash) 
                VALUES (%s, %s, %s, %s);
            """, (name, phone, email, password_hash))
            await conn.commit()
            return cursor.lastrowid 
    finally:
        conn.close()

async def get_user_by_phone(phone: str):
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT * FROM users WHERE phone = %s;
            """, (phone,))
            user = await cursor.fetchone()
            return user
    finally:
        conn.close()

async def create_session_for_user(user_id: int, name: str) -> str:
    user_data = {
        "sub": user_id,
        "name": name
    }
    return create_access_token(user_data)

async def get_user_from_session(session_token: str):
    user_data = verify_access_token(session_token)
    if user_data:
        return await get_user_by_id(user_data['sub'])
    return None

async def get_user_by_id(user_id: int):
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT * FROM users WHERE id = %s;
            """, (user_id,))
            user = await cursor.fetchone()
            return user
    finally:
        conn.close()
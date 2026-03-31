from sanic import Blueprint
from sanic.response import json
from orjson import dumps, loads
from models import Book
import redis_client

bp = Blueprint('books')
CACHE_EXPIRE = 300

@bp.post('/books')
async def add_book(request):
    data = request.json
    book = Book(**data)
    await book.insert()
    await redis_client.redis_client.delete("books:all")
    return json({"message": "Book added", "id": str(book.id)}, status=200, dumps=dumps)

@bp.get('/books')
async def get_books(request):
    cache_key = "books:all"
    cached = await redis_client.redis_client.get(cache_key)
    if cached:
        return json(loads(cached), status=200, dumps=dumps)
    
    books = await Book.find_all().to_list()
    data = [book.model_dump() for book in books]
    await redis_client.redis_client.set(cache_key, dumps(data), ex=CACHE_EXPIRE)
    return json(data, status=200, dumps=dumps)

@bp.get('/books/<book_id:str>')
async def get_book(request, book_id):
    cache_key = f"books:{book_id}"
    cached_book = await redis_client.redis_client.get(cache_key)
    if cached_book:
        return json(loads(cached_book), status=200, dumps=dumps)
    
    book = await Book.get(book_id)
    if not book:
        return json({"error":"Book not Found"}, status=404, dumps=dumps)
    data = book.model_dump()
    await redis_client.redis_client.set(cache_key, dumps(data), ex=CACHE_EXPIRE)
    return json(data, status=200, dumps=dumps)

@bp.delete("/books/<book_id:str>")
async def delete_book(request, book_id):
    book = await Book.get(book_id)
    if not book:
        return json({"error":"Book not Found"}, status=404, dumps=dumps)
    await book.delete()
    await redis_client.redis_client.delete(f"books:all")
    await redis_client.redis_client.delete(f"books:{book_id}")
    return json({"message": "Book deleted"}, status=200, dumps=dumps )


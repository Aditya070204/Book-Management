from sanic import Blueprint
from sanic.response import json
from orjson import dumps
from models import Book

bp = Blueprint('books')

@bp.post('/books')
async def add_book(request):
    data = request.json
    book = Book(**data)
    await book.insert()
    return json({"message": "Book added", "id": str(book.id)}, status=200, dumps=dumps)

@bp.get('/books')
async def get_books(request):
    books = await Book.find_all().to_list()
    return json([book.model_dump() for book in books], status=200, dumps=dumps)

@bp.get('/books/<book_id: str>')
async def get_book(request, book_id):
    book = await Book.get(book_id)
    if not book:
        return json({"error":"Book not Found"}, status=404, dumps=dumps)
    return json(book.model_dump(), status=200, dumps=dumps)

@bp.delete("/books/<book_id:str>")
async def delete_book(request, book_id):
    book = await Book.get(book_id)
    if not book:
        return json({"error":"Book not Found"}, status=404, dumps=dumps)
    await book.delete()
    return json({"message": "Book deleted"}, status=200, dumps=dumps)



from beanie import Document
from pydantic import Field
from typing import Optional

class Book(Document):
    title: str = Field(..., description="The title of the book", max_length=250)
    author: str = Field(..., description="The author of the book", max_length=250)
    year: Optional[int] = None

    class Settings:
        name = "books"
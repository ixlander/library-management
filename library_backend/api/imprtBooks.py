import json
from models import Book, Category

with open('books.json') as f:
    books_data = json.loads(f)

for book_data in books_data[:5]:
    # Получить объект категории из базы данных
    category_name = book_data['Category']
    category = Category.objects.get(name=category_name)

    # Создать экземпляр книги
    book = Book.objects.create(
        title=book_data['Title'],
        author=book_data['Author'],
        year=book_data['Year'],
        publisher=book_data['Publisher'],
        image=book_data['Image'],
        category=category,
        description=book_data['Description']
    )

    # Сохранить книгу в базе данных
    book.save()
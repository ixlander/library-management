import json
from .models import Book, Category

try:
    with open('booksDataset.json') as f:
        books_data = json.load(f)  
    
    for book_data in books_data[:5]:
        category_name = book_data['Category']
        category, created = Category.objects.get_or_create(name=category_name)
    
        book = Book.objects.create(
            title=book_data['Title'],
            author=book_data['Author'],
            year=book_data['Year'],
            publisher=book_data['Publisher'],
            image=book_data['Image'],
            category=category,
            description=book_data['Description']
        )
        
        book.save()
        print(f"Книга '{book.title}' успешно импортирована")
        
    print("Импорт завершен")
except Exception as e:
    print(f"Ошибка импорта: {e}")
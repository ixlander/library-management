from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.id}: {self.name}'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class BookManager(models.Manager):
    def get_books_by_author(self, author):
        return self.filter(author=author)

    def get_books_by_publisher(self, publisher):
        return self.filter(publisher=publisher)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.FloatField(default=0)
    likes = models.IntegerField(default=0)
    link = models.URLField(null=True)
    objects = BookManager()

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f'{self.id}: {self.title}, {self.year}, {self.publisher}, {self.author}, {self.category}, {self.rating}'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'image': self.image,
            'category': self.category.to_json()
        }

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    rating = models.IntegerField()
    comment = models.TextField()

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'Review #{self.id}, {self.book}, {self.user.username if self.user else "Anonymous"}, {self.rating}, {self.comment}'

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.title,
            'user': self.user.username if self.user else "Anonymous",
            'rating': self.rating,
            'comment': self.comment,
            'date': self.date.isoformat() if self.date else None,
        }

class BookShelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    class Meta:
        verbose_name = 'Bookshelf'
        verbose_name_plural = 'Bookshelves'

    def __str__(self):
        return f'Bookshelf #{self.id}, {self.name}, {self.user.username}'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user': self.user.username,
            'books': list(self.books.values_list('id', flat=True)),
        }

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment #{self.id}, {self.book}, {self.user.username if self.user else "Anonymous"}, {self.content}, {self.date}'

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.title,
            'user': self.user.username if self.user else "Anonymous",
            'date': self.date.isoformat(),
            'content': self.content,
        }

class FavBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('book', 'user')
        verbose_name = 'FavBook'
        verbose_name_plural = 'FavBooks'

    def __str__(self):
        return f'FavBook #{self.id}, {self.book}, {self.user.username if self.user else "Anonymous"}'

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.title,
            'user': self.user.username if self.user else "Anonymous",
        }
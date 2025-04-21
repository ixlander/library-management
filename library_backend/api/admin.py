from django.contrib import admin
from .models import Category, Book, Review, BookShelf, Comment, FavBook

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'publisher')
    list_filter = ('category',)
    search_fields = ('title', 'author', 'category__name')

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'content', 'date')
    list_filter = ('book', 'user')
    search_fields = ('book__name', 'user__username')


@admin.register(FavBook)
class FavBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user')
    list_filter = ('book', 'user')
    search_fields = ('book__name', 'user__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'comment')
    list_filter = ('book', 'user')
    search_fields = ('book', 'user')

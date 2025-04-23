from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/',views.get_user),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('newPassword/',views.update_password),
    path('register/',views.register),
    path('bookshelves/',views.get_bookshelves), 
    path('categories/', views.get_categories),
    path('categories/<int:id>', views.get_category),
    path('categories/<int:id>/books', views.get_category_books),
    path('books/', views.BooksAPIView.as_view()),
    path('books/<int:id>', views.BookDetailAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('review-create/', views.ReviewCreateAPIView.as_view()),
    path('review-update/<int:id>', views.ReviewUpdateAPIView.as_view()),
    path('review-delete/<int:id>', views.ReviewDeleteAPIView.as_view()),
    path('comments/', views.CommentListAPIView.as_view()),
    path('comments-create/', views.CommentCreateAPIView.as_view()),
    path('comment-update/<int:id>', views.CommentUpdateAPIView.as_view()),
    path('comment-delete/<int:id>', views.CommentDeleteAPIView.as_view()),
    path('books/<int:id>/comments/', views.get_books_comments),
    path('books/<int:id>/reviews/', views.get_books_reviews),
    path('books-by-publisher/<str:publisher>/', views.get_books_by_publisher),
    path('favbook/', views.FavBookListAPIView.as_view()),
    path('favbook-create/', views.FavBookCreateAPIView.as_view()),
    path('favbook-delete/<int:id>', views.FavBookDeleteAPIView.as_view()),
    path('book/<int:book_id>/like/', views.like_book, name='like_book'),
    path('book/<int:book_id>/undolike/', views.undolike_book, name='like_book')
]
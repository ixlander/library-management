import json
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import CategorySerializer, BookSerializer, ReviewSerializer, BookShelfSerializer, CommentSerializer, UserSerializer, FavBookSerializer
from .models import Category, Book, Review, BookShelf, Comment, FavBook
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from rest_framework.permissions import IsAuthenticated,AllowAny
# def registration(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         if password == confirm_password:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'email is exist')
#                 return redirect(register)
from django.contrib.auth.models import User

User = get_user_model()

@csrf_exempt
@api_view(['GET'])
def get_user(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Check if the email or username already exists in the database
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'})

        # Create the new user object
        user = User.objects.create_user(username=username, email=email, password=password)

        # Return a success message
        return JsonResponse({'success': 'User registered successfully.'})
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def update_password(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    if User.objects.filter(email = email).exists():
        user = User.objects.get(email = email)
        user.set_password(password)
        user.save()
        return JsonResponse({'success': 'Password reset successfully'})
@csrf_exempt
@api_view(['GET', 'POST'])
def get_bookshelves(request):
    if request.method == 'GET':
        bookshelves = BookShelf.objects.all()
        serializer = BookShelfSerializer(bookshelves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Category views
@csrf_exempt
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist as error:
        return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
def get_category_books(request, id):
    if request.method == 'GET':
        needed_category = Category.objects.get(id=id)
        books = Book.objects.filter(category=needed_category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_comments(request, id):
    if request.method == 'GET':
        book = Book.objects.get(id=id)
        comments = Comment.objects.filter(book=book)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_reviews(request, id):
    if request.method == 'GET':
        book = Book.objects.get(id=id)
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Books views
class BooksAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    def get_book(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        book = self.get_book(id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        book = self.get_book(id)
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_book(id)
        book.delete()
        return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)

# class PasswordChange(PasswordChangeView):
#     form_class=''
#     success_url = reverse_lazy()
# def password_success(request):


# Review views
class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

class ReviewRetrieveAPIView(RetrieveAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class ReviewDeleteAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

# BookShelf views

# View for creating a new BookShelf:
class BookShelfCreateView(CreateAPIView):
    serializer_class = BookShelfSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View for retrieving a specific BookShelf:
class BookShelfDetailView(RetrieveAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for updating an existing BookShelf:
class BookShelfUpdateView(UpdateAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for deleting an existing BookShelf:
class BookShelfDeleteView(DestroyAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for listing all BookShelfs owned by a specific user:
class BookShelfListView(ListAPIView):
    serializer_class = BookShelfSerializer

    def get_queryset(self):
        return BookShelf.objects.filter(user=self.request.user)


# Comments views
# List all comments
class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

# Retrieve a specific comment by ID
class CommentRetrieveAPIView(RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'

# Create a new comment
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Update an existing comment
class CommentUpdateAPIView(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
    # lookup_url_kwarg = "id"

# Delete an existing comment
class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'


class FavBookCreateAPIView(CreateAPIView):
    serializer_class = FavBookSerializer
    queryset = FavBook.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavBookDeleteAPIView(DestroyAPIView):
    serializer_class = FavBookSerializer
    queryset = FavBook.objects.all()
    lookup_field = 'id'


class FavBookListAPIView(ListAPIView):
    serializer_class = FavBookSerializer
    queryset = FavBook.objects.all()

# @csrf_exempt
# @api_view(['POST'])
# def add_comment(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     content = request.POST.get('content')
#     comment = Comment.objects.create(book=book, user=request.user, content=content)
#     return Response(comment.to_json())

# @csrf_exempt
# @api_view(['DELETE'])
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     if comment.user == request.user:
#         comment.delete()
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False})

# class CommentCreateAPIView(genericpath.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def perform_create(self, serializer):
#         book_id = self.kwargs.get('book_id')
#         book = get_object_or_404(Book, id=book_id)
#         serializer.save(book=book, user=self.request.user)

# class CommentUpdateAPIView(generic.UpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_object(self):
#         comment_id = self.kwargs.get('comment_id')
#         obj = get_object_or_404(Comment, id=comment_id)
#         if obj.user != self.request.user:
#             raise ValidationError("You don't have permission to edit this comment.")
#         return obj

# class CommentDeleteAPIView(GenericAlias.DestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def get_object(self):
#         comment_id = self.kwargs.get('comment_id')
#         obj = get_object_or_404(Comment, id=comment_id)
#         if obj.user != self.request.user:
#             raise ValidationError("You don't have permission to delete this comment.")
#         return obj

# @csrf_exempt
# @api_view(['GET'])
# def get_comments(request, book_id):
#     comments = Comment.objects.filter(book_id=book_id)
#     comments_json = [comment.to_json() for comment in comments]
#     return JsonResponse(comments_json, safe=False)

# class CommentList(APIView):
#     """
#     Выводит список всех комментариев к книге, либо создает новый комментарий.
#     """
#     def get(self, request, book_id):
#         comments = Comment.objects.filter(book=book_id)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)

#     def post(self, request, book_id):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, book_id=book_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_books_by_author(request, author):
    books = Book.objects.get_books_by_author(author)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_by_publisher(request, publisher):
    books = Book.objects.get_books_by_publisher(publisher)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        user = Token.objects.get(key=token[1]).user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


def like_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.likes += 1
    book.save()
    return JsonResponse({'likes': book.likes})

def undolike_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.likes -= 1
    book.save()
    return JsonResponse({'likes': book.likes})










import json
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import PermissionDenied

from .models import Category, Book, Review, BookShelf, Comment, FavBook
from .serializers import (
    CategorySerializer, BookSerializer, ReviewSerializer, BookShelfSerializer, 
    CommentSerializer, UserSerializer, FavBookSerializer, UserRegistrationSerializer
)

User = get_user_model()

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists.'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'})

            user = User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({'success': 'User registered successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def update_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return JsonResponse({'success': 'Password reset successfully'})
        else:
            return JsonResponse({'error': 'User with this email does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_bookshelves(request):
    if request.method == 'GET':
        bookshelves = BookShelf.objects.filter(user=request.user)
        serializer = BookShelfSerializer(bookshelves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])  # Для доступа к категориям без аутентификации
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': f'Category with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

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
@permission_classes([AllowAny])
def get_category_books(request, id):
    try:
        needed_category = get_object_or_404(Category, id=id)
        books = Book.objects.filter(category=needed_category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        return Response({'error': f'Category with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_books_comments(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        comments = Comment.objects.filter(book=book)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        return Response({'error': f'Book with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_books_reviews(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        return Response({'error': f'Book with ID {id} not found'}, status=status.HTTP_404_NOT_FOUND)

class BooksAPIView(APIView):
    permission_classes = [AllowAny]
    
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
    permission_classes = [AllowAny]
    
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404(f"Book with ID {id} not found")

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)

class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [AllowAny]

class ReviewRetrieveAPIView(RetrieveAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'
    permission_classes = [AllowAny]

class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user == self.request.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this review")

class ReviewDeleteAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete this review")
    
        
class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]

class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentUpdateAPIView(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user == self.request.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this comment")

class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete this comment")

class FavBookCreateAPIView(CreateAPIView):
    serializer_class = FavBookSerializer
    queryset = FavBook.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavBookDeleteAPIView(DestroyAPIView):
    serializer_class = FavBookSerializer
    queryset = FavBook.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete this favorite book")

class FavBookListAPIView(ListAPIView):
    serializer_class = FavBookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavBook.objects.filter(user=self.request.user)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_books_by_author(request, author):
    books = Book.objects.get_books_by_author(author)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_books_by_publisher(request, publisher):
    books = Book.objects.get_books_by_publisher(publisher)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user 
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def like_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        book.likes += 1
        book.save()
        return JsonResponse({'likes': book.likes})
    except Http404:
        return JsonResponse({'error': f'Book with ID {book_id} not found'}, status=404)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def undolike_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        if book.likes > 0:
            book.likes -= 1
        book.save()
        return JsonResponse({'likes': book.likes})
    except Http404:
        return JsonResponse({'error': f'Book with ID {book_id} not found'}, status=404)
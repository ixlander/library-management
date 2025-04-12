from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Book, Review, Favorite, ReadingProgress
from .serializers import (
    UserSerializer, UserRegistrationSerializer, BookSerializer, BookDetailSerializer,
    ReviewSerializer, CreateReviewSerializer, FavoriteSerializer, ReadingProgressSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'genre']
    ordering_fields = ['title', 'author', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        book = self.get_object()
        user = request.user
        
        favorite, created = Favorite.objects.get_or_create(user=user, book=book)
        
        if created:
            return Response({'status': 'book added to favorites'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'book already in favorites'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        book = self.get_object()
        user = request.user
        progress = request.data.get('progress', 0)
        
        if not 0 <= progress <= 100:
            return Response({'error': 'Progress must be between 0 and 100'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        reading_progress, created = ReadingProgress.objects.update_or_create(
            user=user, book=book,
            defaults={'progress': progress}
        )
        
        serializer = ReadingProgressSerializer(reading_progress)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateReviewSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReadingProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
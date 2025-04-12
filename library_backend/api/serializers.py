from rest_framework import serializers
from .models import User, Book, Review, Favorite, ReadingProgress

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'is_admin']
        read_only_fields = ['user_id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'genre', 'description', 'average_rating']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None

class BookDetailSerializer(BookSerializer):
    reviews = serializers.SerializerMethodField()
    
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['reviews']
    
    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['review_id', 'rating', 'comment', 'user', 'book', 'created_at']
        read_only_fields = ['review_id', 'created_at']
    
    def get_user(self, obj):
        return obj.user.username

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['book', 'rating', 'comment']
    
    def create(self, validated_data):
        user = self.context['request'].user
        review = Review.objects.create(
            user=user,
            **validated_data
        )
        return review

class FavoriteSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['favorite_id', 'book', 'book_details']
        read_only_fields = ['favorite_id']

class ReadingProgressSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    
    class Meta:
        model = ReadingProgress
        fields = ['progress_id', 'book', 'progress', 'updated_at', 'book_details']
        read_only_fields = ['progress_id', 'updated_at']
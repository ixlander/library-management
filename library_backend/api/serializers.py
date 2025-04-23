from rest_framework import serializers
from .models import Category, Book, Review, BookShelf, Comment, FavBook
from django.contrib.auth.models import User
from django.db import IntegrityError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'year', 'publisher', 'image', 
                 'category', 'category_id', 'description', 'rating', 'likes', 'link']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'username', 'rating', 'comment', 'date']

class BookShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookShelf
        fields = ['id', 'name', 'user', 'books']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'username', 'content', 'date']

class FavBookSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = FavBook
        fields = ['id', 'book', 'user', 'username']

    def create(self, validated_data):
        try:
            fav_book = FavBook.objects.create(**validated_data)
            return fav_book
        except IntegrityError:
            raise serializers.ValidationError("This book is already in your favorites.")
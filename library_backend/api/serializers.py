from rest_framework import serializers
from .models import Category, Book, Review, BookShelf, Comment, FavBook
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

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

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    publisher = serializers.CharField(max_length=255)
    image = serializers.URLField()
    category = CategorySerializer()
    description = serializers.CharField()
    rating = serializers.FloatField()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(id=category_data['id'])
        return Book.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(id=category_data['id'])
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.year = validated_data.get('year', instance.year)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.image = validated_data.get('image', instance.image)
        instance.category = category
        instance.description = validated_data.get('description', instance.description)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance



class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'username', 'rating', 'comment', 'date']

class BookShelfSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookShelf
        fields = ['id', 'name', 'user', 'books']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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



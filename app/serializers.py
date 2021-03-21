from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = ['id', 'username', 'reputation']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnswerCategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerCategoryNode
        fields = ['id', 'description', 'answer_type']


class AnswerCategorySerializer(serializers.ModelSerializer):
    category_nodes = AnswerCategoryNodeSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False)
    class Meta:
        model = AnswerCategory
        fields = ['id', 'rank', 'category', 'category_nodes']


class AnswerSerializer(serializers.ModelSerializer):
    reviewed_categories = AnswerCategorySerializer(many=True, read_only=True) 
    rank = serializers.FloatField(source='get_answer_rank')
    author = ProfileSerializer(many=False)
    class Meta:
        model = Answer
        fields = ['id', 'author', 'created', 'is_top_answer', 'description', 'rank', 'reviewed_categories']
 
#serializer dla POST/PUT
class AnswerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'author', 'description', 'post']
        read_only_fields = ['is_top_answer']
 

class LastActivitySerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.user.username')
    class Meta:
        model = Answer
        fields = ['author', 'created']



#obiekt posta wraz z informacja o odpowiedziach
class PostDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    answers = AnswerSerializer(many=True)
    author = ProfileSerializer(many=False)
    rank = serializers.FloatField(source='get_post_rank')
    class Meta:
        model = Post
        fields = ['id', 'visits', 'rank', 'author', 'created', 'description', 'title', 'repo_link', 'page_link', 'has_top_answer', 'categories', 'answers']


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'created', 'description', 'title', 'repo_link', 'page_link', 'has_top_answer', 'categories']

#obiekt posta bez dodatkowych informacji
class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    number_of_answers = serializers.IntegerField(source="get_answer_count")
    last_activity = LastActivitySerializer(source="get_last_activity")
    author = ProfileSerializer(many=False)
    rank = serializers.FloatField(source='get_post_rank')
    class Meta:
        model = Post
        fields = ['id', 'visits', 'rank', 'last_activity', 'author', 'created', 'description', 'title', 'repo_link', 'page_link', 'has_top_answer', 'categories', 'number_of_answers']


import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from ..models import Post, Profile, User, Category
from ..serializers import PostSerializer, PostDetailSerializer

client = APIClient()

class GetAllPostsTest(APITestCase):

    def setUp(self):
        user = User.objects.create(username='test', password='123456')
        profile = Profile.objects.create(user=user, reputation=100)
        categories = Category.objects.all()
        post = Post.objects.create(
            author=profile,
            description='Test post description',
            title='Test post',
            repo_link='http://www.google.com',
            page_link='http://www.google.com'
        )
        post.categories.set(categories)

        post2 = Post.objects.create(
            author=profile,
            description='Test post description2',
            title='Test post2',
            repo_link='http://www.google.com',
            page_link='http://www.google.com'
        )
        post2.categories.set(categories)

    def test_get_all_posts(self):
        response = client.get('/api/posts/', follow=True)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePostTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='123456')
        profile = Profile.objects.create(user=user, reputation=100)
        categories = Category.objects.all()
        self.post = Post.objects.create(
            author=profile,
            description='Test post description',
            title='Test post',
            repo_link='http://www.google.com',
            page_link='http://www.google.com'
        )
        self.post.categories.set(categories)
    
    def test_get_valid_single_post(self):
        response = client.get(f'/api/posts/{self.post.pk}/')
        post = Post.objects.get(pk=self.post.pk)
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_invalid_single_post(self):
        response = client.get(f'/api/posts/{1000000}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPostTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='123456')
        profile = Profile.objects.create(user=user, reputation=100)
        category = Category.objects.create(name="SEO")
        self.valid_payload = {
            "author": profile.pk,
            "description": "Test post description",
            "title": "Test post",
            "repo_link": "http://www.google.com",
            "page_link": "http://www.google.com",
            "has_top_answer": False,
            "categories": [category.pk]
        }
        self.invalid_payloads = [
            {
                "author": None,
                "description": "Test post description",
                "title": "Test post",
                "repo_link": "http://www.google.com",
                "page_link": "http://www.google.com",
                "has_top_answer": False,
                "categories": [category.pk]
            },
            {
                "author": profile.pk,
                "description": None,
                "title": "Test post",
                "repo_link": "http://www.google.com",
                "page_link": "http://www.google.com",
                "has_top_answer": False,
                "categories": [category.pk]
            },
            {
                "author": profile.pk,
                "description": "Test post description",
                "title": None,
                "repo_link": "http://www.google.com",
                "page_link": "http://www.google.com",
                "has_top_answer": False,
                "categories": [category.pk]
            },
            {
                "author": profile.pk,
                "description": "Test post description",
                "title": "Test post description",
                "repo_link": None,
                "page_link": "http://www.google.com",
                "has_top_answer": False,
                "categories": []
            },
            {
                "author": profile.pk,
                "description": "Test post description",
                "title": None,
                "repo_link": "http://www.google.com",
                "page_link": "http://www.google.com",
                "has_top_answer": None,
                "categories": []
            }
        ]
    
    def test_valid_create_post(self):
        response = client.post(
            '/api/posts/',
            content_type='application/json',
            data=json.dumps(self.valid_payload)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_post(self):
        for payload in self.invalid_payloads:
            response = client.post(
                '/api/posts/',
                content_type='application/json',
                data=json.dumps(payload)
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeletePostTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='123456')
        profile = Profile.objects.create(user=user, reputation=100)
        categories = Category.objects.all()
        self.post = Post.objects.create(
            author=profile,
            description='Test post description',
            title='Test post',
            repo_link='http://www.google.com',
            page_link='http://www.google.com',
            has_top_answer=False)
        self.post.categories.set(categories)

    def test_valid_delete_post(self):
        response = client.delete(f'/api/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_invalid_delete_post(self):
        response = client.delete(f'/api/posts/{10000000}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class UpdatePostTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test', password='123456')
        profile = Profile.objects.create(user=user, reputation=100)
        categories = Category.objects.all()
        category = Category.objects.create(name="SEO")
        self.post = Post.objects.create(
            author=profile,
            description='Test post description',
            title='Test post',
            repo_link='http://www.google.com',
            page_link='http://www.google.com',
            has_top_answer=False)

        self.valid_payload = {
            "author": profile.pk,
            "description": "Test2 desc",
            "title": "Test2 post",
            "repo_link": "http://www.google.com/test",
            "page_link": "http://www.google.com/test",
            "has_top_answer": True,
            "categories": [category.pk]
        }
        self.invalid_payload = {
            "author": profile.pk,
            "description": "Test2 desc",
            "title": "Test2 post",
            "repo_link": "http://www.google.com/test",
            "page_link": "",
            "has_top_answer": None,
            "categories": [category.pk]
        }

    
    def test_valid_update_post(self):
        response = client.put(
            f'/api/posts/{self.post.pk}/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    def test_invalid_update_post(self):
        response = client.put(
            f'/api/posts/{self.post.pk}/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.put(
            f'/api/posts/{10000000}/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
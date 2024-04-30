"""
Test the recipe APIs.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """
    Return recipe detail URL.
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    """
    Create and return a sample recipe.
    """
    defaults = {
        'title': 'Sample recipe',
        'description': 'Sample description',
        'price': Decimal('5.00'),
        'time_minutes': 22,
        'link': 'https://www.sample.com',
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicRecipeApiTests(TestCase):
    """
    Test unauthenticated recipe API requests.
    """
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required.
        """
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test authenticated recipe API requests.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='test1234',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """
        Test retrieving a list of recipes.
        """
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """
        Test retrieving recipes is limited to authenticated user's recipes.
        """
        user2 = create_user(
            email='other@example.com',
            password='test1234',
        )
        create_recipe(user=user2)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """
        Test retrieving a recipe detail.
        """
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """
        Test creating a recipe.
        """
        payload = {
            'title': 'Chocolate cheesecake',
            # 'description': 'Tasty chocolate cheesecake',
            'price': Decimal('10.00'),
            'time_minutes': 30,
        }
        res = self.client.post(RECIPES_URL, payload) # /api/recipes/<recipe-id>

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """
        Test updating a recipe with PATCH.
        """
        original_link = 'https://www.example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Original title',
            link=original_link,
        )
        payload = {
            'title': 'Updated title',
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update_of_recipe(self):
        """
        Test updating a recipe with PUT.
        """
        recipe = create_recipe(
            user=self.user,
            title='Original title',
            description='Original description',
            link='https://www.example.com/recipe.pdf',
        )
        payload = {
            'title': 'Updated title',
            'description': 'Updated description',
            'link':'https://www.example.com/recipe.pdf',
            'price': Decimal('10.00'),
            'time_minutes': 30,
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """
        Test updating the user field returns an error.
        """
        new_user = create_user(
            email='user2@example.com',
            password='test1234',
        )
        recipe = create_recipe(user=self.user)

        payload = {
            'user': new_user.id,
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """
        Test deleting a recipe succesful.
        """
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

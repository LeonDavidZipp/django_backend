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

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


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
        self.user = get_user_model().objects.create_user(
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
        user2 = get_user_model().objects.create_user(
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
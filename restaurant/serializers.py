from django.contrib.auth.models import User
from rest_framework import serializers


class ChefSerializer(serializers.Serializer):
    cd_chef = serializers.UUIDField()
    name = serializers.CharField()


class RecipeSerializer(serializers.Serializer):
    #TODO: Trocar chef por cd_chef
    cd_recipe = serializers.UUIDField()
    title = serializers.CharField()
    chef_id = serializers.CharField(required=False)
    chef__name = serializers.CharField()

    def validate_title(self, data):
        return data

    def validate_chef(self, data):
        return data



class IngredientSerializer(serializers.Serializer):
    description = serializers.CharField()


class FoodPreparationSerializer(serializers.Serializer):
    step_number = serializers.IntegerField()
    step_description = serializers.CharField()
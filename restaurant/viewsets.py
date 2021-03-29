from rest_framework.response import Response
from rest_framework import viewsets, permissions
from restaurant.models import Recipe, Chef, RecipeIngredient, Ingredient, FoodPreparation
from restaurant.serializers import (
    RecipeSerializer, ChefSerializer, IngredientSerializer, FoodPreparationSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

class ChefViewSet(viewsets.ViewSet):

    def create(self, request):
        pass

    def retrieve(self, request, cd_chef):
        try:
            chef = Chef.objects.get(cd_chef=cd_chef)
        
        except ObjectDoesNotExist:
            return Response("Resource doesn't exists", status=404)
        except Exception:
            return Response("A error occurred.", status=500)

        serializer = ChefSerializer(chef)
        
        return Response(serializer.data)
    
    def list(self, request):
        try:
            queryset = Chef.objects.all()
            serializer = ChefSerializer(queryset, many=True)
        except Exception:
            return Response({"message": "A error occurred."}, status=500)

        return Response(serializer.data, status=200)

    def create_recipe(self, request, cd_chef):
        with transaction.atomic():
            try:
                chef = Chef.objects.get(cd_chef=cd_chef)
                recipe = Recipe.objects.create(title=request.data["title"], chef=chef)
                recipe.save()
            except ObjectDoesNotExist:
                return Response({"message": "Object doesn't exists"}, status=404)
            except Exception as e:
                return Response({"message": "A error occurred."}, status=500)

            return Response({"message": "Recipe has been created. "}, status=201)

    def get_recipes(self, request, cd_chef):
        recipes = Recipe.objects.prefetch_related("recipeingredient_set").all()
        recipes = recipes.prefetch_related("recipeingredient_set__ingredient")
        recipes = recipes.prefetch_related("foodpreparation_set")
        recipes = recipes.select_related("chef")
        result = []
            
        for recipe in recipes:
            obj = {
                "cd_recipe": recipe.cd_recipe,
                "title": recipe.title,
                "chef": recipe.chef.name,
                "ingredient": [],
                "food_preparation": []
            }
            for recipe_ingredient in recipe.recipeingredient_set.all():
                obj["ingredient"].append(
                    {
                        "description": recipe_ingredient.ingredient.description,
                        "quantity": recipe_ingredient.quantity
                    }
                )

            for food_preparation in recipe.foodpreparation_set.all():
                obj["food_preparation"].append(
                    {
                        "step_number": food_preparation.step_number,
                        "step_description": food_preparation.step_description
                    }
                )
            result.append(obj)
        return Response(result)
      
    def create_recipe_ingredients(self, request, cd_chef, cd_recipe):
        with transaction.atomic():
            try:
                chef = Chef.objects.get(cd_chef=cd_chef)
                recipe = Recipe.objects.get(cd_recipe=cd_recipe)
            except Exception:
                return Response({"message": "Chef or recipe not found"}, status=404)

            ingredients = request.data["ingredient"]
            serializer = IngredientSerializer(data=ingredients, many=True)

            if not serializer.is_valid():
                return Response({"mensagem": "Error in data validation"}, status=422)

            try:
                list_ingredients = []
                list_recipe_ingredients = []
                
                for obj in ingredients:
                    ingredient = Ingredient(description=obj["description"]) 
                    recipe_ingredient = RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=obj["quantity"]
                    )

                    list_ingredients.append(ingredient)
                    list_recipe_ingredients.append(recipe_ingredient)

                Ingredient.objects.bulk_create(list_ingredients)
                RecipeIngredient.objects.bulk_create(list_recipe_ingredients)
            except Exception:
                return Response({"message": "A error occurred."}, status=500)
            
            return Response({"message": "Ingredients has been added to the recipe"}, 201)

    def create_recipe_food_preparation(self, request, cd_chef, cd_recipe):
        with transaction.atomic():
            try:
                recipe = Recipe.objects.get(cd_recipe=cd_recipe)
                food_preparation_steps = request.data["food_preparation"]
                list_steps = []

                serializer = FoodPreparationSerializer(data=food_preparation_steps, many=True)
                
                if not serializer.is_valid():
                    return Response({"mensagem": "Error in data validation"}, status=422)

                for step in food_preparation_steps:
                    obj = FoodPreparation(**step, recipe=recipe)
                    list_steps.append(obj)

                FoodPreparation.objects.bulk_create(list_steps)
            
            except ObjectDoesNotExist:
                return Response({"message": "Chef or Recipe not found"}, status=404)
            except Exception:
                return Response({"message": "A error occurred."}, status=500)
            

        return Response({"message": "Food preparation has been added to the recipe"}, status=201)


class RecipeViewSet(viewsets.ViewSet):
    def create(self, request):
        pass

    def get(self, request, cd_recipe):
        try:
            recipe = Recipe.objects.get(cd_recipe=cd_recipe)
        except ObjectDoesNotExist:
            return Response({"message": "Recipe doesn't exists"}, status=404)
        except Exception:
            return Response({"message": "A error occurred"}, status=500)

        obj = {
            "cd_recipe": recipe.pk,
            "title": recipe.title,
            "chef": recipe.chef.name
        }
    
        return Response(obj, status=200)

    def list(self, request):
        query_chef = request.query_params.get("chef", "")
        query_title = request.query_params.get("recipe", "")
        queryset = Recipe.objects.all()

        try:
            if query_chef != "":
                queryset = Recipe.objects.filter(
                    chef__name__icontains=query_chef, 
                )
            if query_title != "":
                queryset = Recipe.objects.filter(
                    title__icontains=query_title
                )
            
            queryset = queryset.select_related("chef").values("cd_recipe", "title", "chef_id", "chef__name")
        
        except KeyError:
            queryset = Recipe.objects.all()
            queryset = queryset.select_related("chef").values("cd_recipe", "title", "chef_id", "chef__name")

        except Exception as e:
            return Response({"message": "A error occurred"}, status=500)

        serializer = RecipeSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def destroy(self, request, cd_recipe):
        try:
            Recipe.objects.get(cd_recipe=cd_recipe).delete()
        except ObjectDoesNotExist:
            return Response({"message": "Recipe doesn't exists "}, status=404)
        except Exception:
            return Response({"message": "A error occurred"}, status=500)

        return Response({"message": "Recipe deleted"}, status=204)


class IngredientViewSet(viewsets.ViewSet):

    def create(self, request):
        pass

    def list(self, request):
        try:
            ingredients = Ingredient.objects.all()
        except Exception as e:
            return Response("A error occurred", status=500)

        serializer = IngredientSerializer(ingredients, many=True)
        
        return Response(serializer.data, status=200)
            
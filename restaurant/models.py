from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator


class Chef(models.Model):
    cd_chef= models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column="cd_chef")
    name = models.CharField("Name", max_length=100, db_column="nm_chef")

    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "Chef"
        verbose_name_plural = "Chefs"
        db_table = "tb_chef"


class Recipe(models.Model):
    cd_recipe = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column="cd_recipe")
    title = models.CharField("Title", max_length=100, db_column="ds_title")
    chef = models.ForeignKey("Chef", on_delete=models.CASCADE, db_column="cd_chef")


    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        db_table = "tb_recipe"


class Ingredient(models.Model):
    cd_ingredient = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column="cd_ingredient")
    description = models.CharField("Description", max_length=60, db_column="ds_ingredient")


    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        db_table = "tb_ingredient"


class RecipeIngredient(models.Model):
    cd_recipe_ingredient = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column="cd_recipe_ingredient")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, db_column="cd_recipe")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, db_column="cd_ingredient")
    quantity = models.IntegerField("Quantity", validators=[MinValueValidator(1)], db_column="quantity")


    class Meta:
        verbose_name = "Recipe and Ingredient"
        verbose_name_plural = "Recipes and Ingredients"
        db_table = "tb_recipe_ingredient"


class FoodPreparation(models.Model):
    cd_food_preparation = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column="cd_food_preparation")
    step_number = models.IntegerField(validators=[MinValueValidator(1)])
    step_description = models.CharField("Description", max_length=120, db_column="ds_step")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, db_column="cd_recipe")
 
    
    class Meta:
        verbose_name = "Food Preparation"
        verbose_name_plural = "Food Preparations"
        db_table = "tb_food_preparation"

# Generated by Django 3.1.7 on 2021-03-29 02:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('cd_chef', models.UUIDField(db_column='cd_chef', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nm_chef', max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Chef',
                'verbose_name_plural': 'Chefs',
                'db_table': 'tb_chef',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('cd_ingredient', models.UUIDField(db_column='cd_ingredient', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='ds_ingredient', max_length=60, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'db_table': 'tb_ingredient',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('cd_recipe', models.UUIDField(db_column='cd_recipe', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='ds_title', max_length=100, verbose_name='Title')),
                ('chef', models.ForeignKey(db_column='cd_chef', on_delete=django.db.models.deletion.CASCADE, to='restaurant.chef')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'db_table': 'tb_recipe',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('cd_recipe_ingredient', models.UUIDField(db_column='cd_recipe_ingredient', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(db_column='quantity', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity')),
                ('ingredient', models.ForeignKey(db_column='cd_ingredient', on_delete=django.db.models.deletion.CASCADE, to='restaurant.ingredient')),
                ('recipe', models.ForeignKey(db_column='cd_recipe', on_delete=django.db.models.deletion.CASCADE, to='restaurant.recipe')),
            ],
            options={
                'verbose_name': 'Recipe and Ingredient',
                'verbose_name_plural': 'Recipes and Ingredients',
                'db_table': 'tb_recipe_ingredient',
            },
        ),
        migrations.CreateModel(
            name='FoodPreparation',
            fields=[
                ('cd_food_preparation', models.UUIDField(db_column='cd_food_preparation', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('step_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('step_description', models.CharField(db_column='ds_step', max_length=120, verbose_name='Description')),
                ('recipe', models.ForeignKey(db_column='cd_recipe', on_delete=django.db.models.deletion.CASCADE, to='restaurant.recipe')),
            ],
            options={
                'verbose_name': 'Food Preparation',
                'verbose_name_plural': 'Food Preparations',
                'db_table': 'tb_food_preparation',
            },
        ),
    ]
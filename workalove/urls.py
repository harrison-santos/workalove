"""workalove URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from restaurant.viewsets import RecipeViewSet, ChefViewSet, IngredientViewSet
from django.views.generic import TemplateView

"""router = routers.DefaultRouter()
router.register(r'chef', ChefViewSet)
router.register(r'dish', DishViewSet)
"""

#re_guide = r"(?P<cd_chef>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
re_guide = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

urlpatterns = [
    #path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/ingredient',
        IngredientViewSet.as_view({"get": "list"})
    ),
    path('api/recipe',
        RecipeViewSet.as_view({"get": "list"}), name = "recipe"
    ),
    re_path(rf'^api/recipe/(?P<cd_recipe>{re_guide})$',
        RecipeViewSet.as_view({"get": "get", "delete": "destroy"})
    ),
    path('api/chef',
        ChefViewSet.as_view({"get": "list"}), name = "chef"
    ),
    re_path(rf'^api/chef/(?P<cd_chef>{re_guide})$',
        ChefViewSet.as_view({"get": "retrieve"})
    ),
    re_path(rf"^api/chef/(?P<cd_chef>{re_guide})/recipe$",
        ChefViewSet.as_view({"get": "get_recipes", "post": "create_recipe"})
    ),
    re_path(rf"^api/chef/(?P<cd_chef>{re_guide})/recipe/(?P<cd_recipe>{re_guide})$",
        ChefViewSet.as_view({"delete": "delete_recipe"})
    ),
    re_path(rf"^api/chef/(?P<cd_chef>{re_guide})/recipe/(?P<cd_recipe>{re_guide})/ingredient$",
        ChefViewSet.as_view({"post": "create_recipe_ingredients"})
    ),
    re_path(rf"^api/chef/(?P<cd_chef>{re_guide})/recipe/(?P<cd_recipe>{re_guide})/foodpreparation$",
        ChefViewSet.as_view({"post": "create_recipe_food_preparation"})
    )
    path(
        "docs",
        TemplateView.as_view(
            template_name="redoc.html",
            extra_content={"schema_url": "docs/api.yaml"}
        ),
        name="api_docs"
    )
]

from django.urls import path
from . import views

# URL food_recommend
urlpatterns = [
    path("", views.display, name="main"),
    path("search_api/", views.search, name="search"),
    path("adding/", views.add_food, name="adding"),
    path("admin_food/", views.admin_func, name="admin_food")
]

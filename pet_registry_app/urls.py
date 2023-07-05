from django.urls import path
from .views import add_pet, get_pet

urlpatterns = [
    path("add_pet/", add_pet),
    path("get_pet/<int:pet_id>/", get_pet),
]

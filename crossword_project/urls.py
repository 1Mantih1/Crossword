from django.contrib import admin
from django.urls import path
from crossword import views

urlpatterns = [
    path('api/get-cross/', views.get_cross),
    path('api/check-data/', views.check_answer),
    path('admin/get-data/', views.get_data),
    path('admin/add_solution/', views.add_solution),
]

from django.contrib import admin
from django.urls import path
from crossword import views

urlpatterns = [
    path('api/get-cross/', views.get_cross),
    path('api/check-data/', views.check_answer),
    path('admin/get-data/', views.get_data),
    path('admin/add-solution/', views.add_solution),  # Добавление нового решения
    path('admin/update-solution/', views.update_solution),  # Обновление существующего решения
    path('admin/delete-solution/', views.delete_solution),  # Удаление решения
    path('admin/get-data/', views.get_solution_data),  # Получение всех решений
]

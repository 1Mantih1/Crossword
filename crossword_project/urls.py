from django.contrib import admin
from django.urls import path
from crossword import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-data/', views.get_data, name='get_data'),
    path('api/check-data/', views.check_answer, name='check_data'),
]

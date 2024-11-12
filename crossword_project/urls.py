from django.contrib import admin
from django.urls import path
from crossword import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-cross/', views.get_data),
    path('api/check-data/', views.check_answer)
    path('admin/get-data', views.)
]

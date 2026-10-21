from django.urls import path
from . import views

urlpatterns = [
    path('top_commenters/', views.top_commenters,
            name='analytics.top_commenters'),
]
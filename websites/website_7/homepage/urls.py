from django.urls import path # path function is used to define url patterns
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'), # when someone visits the '' on our website, call the views.homepage function (views is a part of this app), name is just a label
    path('search/', views.search_view, name='search'),
]
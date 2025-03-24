# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('members/', views.members, name='members'),
# ]
from django.urls import path # path function is used to define url patterns
from . import views

urlpatterns = [
    path('members/', views.members, name='members'), # when someone visits the members/ on our website, call the views.members function (views is a part of this app), name is just a label
]
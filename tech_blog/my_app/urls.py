from django.contrib import admin
from django.urls import path
from . import views

app_name = "my_app"

urlpatterns = [
    path('', views.PublishedBlogListView.as_view(), name='index'),
    path('login/', views.user_login, name="login" ),
    path('logout/', views.user_logout, name="logout"),
    path('new_post/', views.BlogCreateView.as_view(), name="new_post"),
    path('drafts/', views.DraftBlogListView.as_view(), name='drafts'),
    path('detail/<int:pk>', views.BlogDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.BlogUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', views.BlogDeleteView.as_view(), name="delete"),

]


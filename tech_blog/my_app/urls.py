from django.contrib import admin
from django.urls import path
from . import views

app_name = "my_app"

urlpatterns = [
    path('', views.PublishedBlogListView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('new_post/', views.BlogCreateView.as_view(), name="new_post"),
    # Change these to blog/...
    path('drafts/', views.DraftBlogListView.as_view(), name='drafts'),
    path('detail/<int:pk>', views.BlogDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.BlogUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', views.BlogDeleteView.as_view(), name="delete"),
    path('blog/<int:pk>/publish', views.blog_publish, name="blog_publish"),
    # path('comment/create', views.create_comment, name='create_comment'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/reject', views.comment_reject, name='comment_reject'),


]


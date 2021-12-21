from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (TemplateView, ListView, DeleteView, CreateView, DetailView, UpdateView)
from django.http import HttpResponse, HttpResponseRedirect, request
from .models import Blog, Comment
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
#This ensures that user is logged in in order to create new database entry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone, dateformat
from datetime import datetime
from .forms import CommentForm, BlogForm

# Create your views here.

class AboutView(TemplateView):
    template_name = 'my_app/about.html'

class PublishedBlogListView(ListView):
    model = Blog
    template_name = 'my_app/index.html'

    # def get_context_data(self, **kwargs):
    #     self.object = self.get_object()
    #     approved_count = self.object.comments
    #     return context

    def get_queryset(self):
        return Blog.objects.filter(state__exact=True)

class DraftBlogListView(LoginRequiredMixin, ListView):
    # This should be done whenever LoginRequiredMixin is inherited. login_url is url to display if user is not 
    # logged in, redirect_field is url to display after they login
    # NB: must have LoginRequiredMixin before Listview
    login_url = '/login/'
    #This does not work
    redirect_field_name = 'my_app/drafts.html'
    
    model = Blog
    template_name = 'my_app/drafts.html'

    # This function overides the original. It has been modified to filter out all objects with state equal to False before ListView displays all.
    # https://docs.djangoproject.com/en/3.2/ref/class-based-views/
    # https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#listview
    # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups  search field lookups
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#field-lookups

    def get_queryset(self):
        return Blog.objects.filter(state__exact=False)

    #Dont need to pass user object in with context dictionary. user object is already available in template as 'user'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     #Can pass objects into templates!!!
    #     context['current_user'] = user
    #     return context


class BlogCreateView(LoginRequiredMixin ,CreateView):
    login_url = '/login/'
    redirect_field_name = 'my_app/new_post.html'

    #I believe the default success_url is the blog details page 
    # fields = ['title', 'content']
    # https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin
    form_class = BlogForm
    model = Blog
    template_name = 'my_app/new_post.html'
    # success_url = "my_app/"

    #This is function sets the field/form parameters not passed to the template
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.state = False
        # print(self.request.user)
        return super().form_valid(form)

class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'my_app/detail.html'

    # This is for injecting data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        # print(self.request.POST)
        form = CommentForm(self.request.POST)
        print(form)
        if form.is_valid():
            # comment_author = form.cleaned_data["author"]
            # comment_text = form.cleaned_data["content"]
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.create_date = timezone.now()
            comment.status = False
            print("create date:", comment.create_date)
            # blog = self.get_object()
            comment.save()

            # comment_object, created = Comment.objects.get_or_create(author=comment_author, content=comment_text, status=False, blog=blog, create_date=create_date)
            # if created:
            #     print("comment created")
            # else:
            #     print("Comment already exists")
            # comment_object.save()
        return HttpResponseRedirect(reverse('my_app:detail', args=(comment.blog.pk,)))

    #I believe this function is called when http POST request occurs, it then gets the object this view is operating on and updates it 
    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#view
    #https://stackoverflow.com/questions/41203730/updating-a-single-object-field-in-django-view
    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin

    # def post(self, *args, **kwargs):
    #     print("post method called")
    #     if self.request.POST.get("submit_publish"):
    #         print("Publish button pressed")
    #         self.object = self.get_object()
    #         self.object.state = True
    #         print(self.object.publish_date)
    #         # self.object.publish_date = dateformat.format(timezone.now(), "M. d, Y, h:i a")
    #         self.object.publish_date = timezone.now()
    #         print(self.object.publish_date)
    #         self.object.save(update_fields=('state', 'publish_date',))
    #         return HttpResponseRedirect(reverse('my_app:index'))

    #     elif self.request.POST.get("submit_comment"):
    #         #Create and save new comment object to database:
    #         print("comment button pressed")

    #         #Create a form instance from form data
    #         blog = self.get_object()
    #         comment_author = self.request.POST.get("author")
    #         comment_text = self.request.POST.get("comment_text")

    #         comment_object, created = Comment.objects.get_or_create(author=comment_author, content=comment_text, status=False, blog=blog)
    #         if created:
    #             print("comment created")
    #         comment_object.save()
    #         return HttpResponseRedirect(reverse('my_app:detail', args=(blog.pk,)))
        
    #     else:
    #         print('else executed')
    #         #https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update
    #         self.object = self.get_object()
    #         print(self.object)
    #         print(self.request.POST)

    #         for val in self.request.POST:
    #             if val[0] == '$':
    #                 print("doller sign found")
    #                 comment_pk = val[2:]
    #                 print("comment_pk =", comment_pk)
    #                 comment_cmd = val[1]

    #         comment_queryset = self.object.comments.filter(pk=comment_pk)
    #         print(self.object.comments.filter(pk=comment_pk))

    #         if comment_cmd == 'a':
    #             print("command is approve")
    #             #change state of comment
    #             comment_queryset.update(status=True)

    #         elif comment_cmd =='r':
    #             print("command is reject")
    #             comment_queryset.delete()
            
    #         return HttpResponseRedirect(reverse('my_app:detail', args=(self.object.pk,)))
                    

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'my_app/new_post.html'

    form_class = BlogForm
    model = Blog
    template_name = 'my_app/new_post.html'

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Blog
    # template_name = 'my_app/blog_confirm_delete.html'
    #Reverse_lazy will ensure that blog object is deleted before url redirect occurs
    success_url = reverse_lazy('my_app:index')

# class CommentCreateView(CreateView):
#     model = comment
#     fields = ['content']
#     template_name = 'my_app/detail.html'
    

# def user_login(request):
    
#     #If user has sent data to server
#     if request.method == 'POST':
#         print("user has posted")
#         #Get info from form
#         user_name = request.POST["user_name"]
#         password = request.POST["password"]

#         #Authenticate user
#         user = authenticate(username=user_name, password=password)

#         if user != None:
#             print("Logging in user")
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('my_app:index'))
#             else:
#                 return HttpResponse("User not active")
#         else:
#             #Should keep on login page and use template tagging to say credentials not valid
#             print("Error in credentials")
#             return HttpResponse("Error in credentials")

#     # else:
#         # user_form =UserForm()

#     return render(request, 'my_app/login.html')

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('my_app:index'))

# Blog handlers
def blog_publish(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.publish()
    return HttpResponseRedirect(reverse('my_app:detail', args=(blog.pk,)))

# Comment-handling views

# Grab form data and create new comment object. Can also be done in post method of class
# def create_comment(request):
#     if request.method == 'POST':
#         form = request.POST
#         print(form)
#     # return HttpResponseRedirect("")

@login_required
def comment_approve(request, pk):
    '''
    Handles the approval of comments.
    '''
    #Gets the comment object corresponding to the given pk value. The comment pk value is passed from the template
    comment = get_object_or_404(Comment, pk=pk)
    print(comment.status)
    comment.approve()
    print(comment.status)

    return HttpResponseRedirect(reverse('my_app:detail', args=(comment.blog.pk,)))

@login_required
def comment_reject(request, pk):
    '''Handles the removal of comment objects from DB'''
    comment = get_object_or_404(Comment, pk=pk)
    blog_pk = comment.blog.pk
    comment.delete()
    return HttpResponseRedirect(reverse('my_app:detail', args=(blog_pk,)))


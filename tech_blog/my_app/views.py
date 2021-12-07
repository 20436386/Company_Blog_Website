from django.db import models
from django.db.models import fields
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DeleteView, CreateView, DetailView, UpdateView)
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Comment
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
#This ensures that user is logged in in order to create new database entry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin

# Create your views here.

class PublishedBlogListView(ListView):
    model = Blog
    template_name = 'my_app/index.html'

class DraftBlogListView(ListView):
    model = Blog
    template_name = 'my_app/drafts.html'


class BlogCreateView(LoginRequiredMixin ,CreateView):
    #I believe the default success_url is the blog details page 
    model = Blog
    fields = ['title', 'content']
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

    #I believe this function is called when http POST request occurs, it then gets the object this view is operating on and updates it 
    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#view
    #https://stackoverflow.com/questions/41203730/updating-a-single-object-field-in-django-view
    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin

    def post(self, *args, **kwargs):
        if self.request.POST.get("submit_publish"):
            print("Publish button pressed")
            self.object = self.get_object()
            self.object.state = True
            self.object.save(update_fields=('state', ))
            return HttpResponseRedirect(reverse('my_app:index'))
        elif self.request.POST.get("submit_comment"):
            #Create and save new comment object to database:
            print("comment button pressed")

            #Create a form instance from form data
            blog = self.get_object()
            comment_author = self.request.POST.get("author")
            comment_text = self.request.POST.get("comment_text")

            comment_object, created = Comment.objects.get_or_create(author=comment_author, content=comment_text, status=False, blog=blog)
            if created:
                print("comment created")
            comment_object.save()
            return HttpResponseRedirect(reverse('my_app:detail'))

    # This is for injecting data
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'my_app/new_post.html'

class BlogDeleteView(DeleteView):
    model = Blog
    # template_name = 'my_app/blog_confirm_delete.html'
    success_url = reverse_lazy('my_app:index')

# class CommentCreateView(CreateView):
#     model = comment
#     fields = ['content']
#     template_name = 'my_app/detail.html'
    

def user_login(request):
    
    #If user has sent data to server
    if request.method == 'POST':
        print("user has posted")
        #Get info from form
        user_name = request.POST["user_name"]
        password = request.POST["password"]

        #Authenticate user
        user = authenticate(username=user_name, password=password)

        if user != None:
            print("Logging in user")
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('my_app:index'))
            else:
                return HttpResponse("User not active")
        else:
            #Should keep on login page and use template tagging to say credentials not valid
            print("Error in credentials")
            return HttpResponse("Error in credentials")

    # else:
        # user_form =UserForm()

    return render(request, 'my_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('my_app:index'))



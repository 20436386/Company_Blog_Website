from django import forms
from django import forms
from .models import Blog, Comment

class BlogForm(forms.ModelForm):
    # NB: Meta has to be capitalized
    class Meta:
        model = Blog
        fields = ("title", "content",)

    # From django docs
    # https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'textinputclass'})
        self.fields['content'].widget.attrs.update({'class': 'editable medium-editor-textarea blog_content'})

    # # From udemy:
    # widgets = {
    #     'title': forms.TextInput(attrs={'class':'textinputclass'}),
    #     'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
    # }
    


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("author","content",)

    # From django docs
    # https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs.update({'class': 'textinputclass'})
        self.fields['content'].widget.attrs.update({'class': 'editable medium-editor-textarea'})

    # # From udemy:
    # widgets = {
    #     'author': forms.TextInput(attrs={'class':'textinputclass'}),
    #     'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
    # }
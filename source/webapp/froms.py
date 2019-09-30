from django import forms
from django.forms import widgets
from webapp.models import Article


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Заголовок')
    text = forms.CharField(max_length=3000, required=True, label='Текст статьи', widget=widgets.Textarea)
    author = forms.CharField(max_length=40, required=False, label='Автор', empty_value="Unknown")


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Article', empty_label=None)
    author = forms.CharField(max_length=40, required=False, label='Автор', initial='Аноним')
    text = forms.CharField(max_length=400, required=True, label='Текст статьи', widget=widgets.Textarea)

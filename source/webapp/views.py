from webapp.froms import ArticleForm, CommentForm
from webapp.models import Article, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={'title': article.title, 'text': article.text, 'author': article.author})
        return render(request, 'update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form,  'todo': article.pk})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article.delete()
        return redirect('index')


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comments/create_comments.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                article=form.cleaned_data['article'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
            )
            return redirect('comment_view', pk=comment.pk)
        else:
            return render(request, 'comments/create_comments.html', context={'form': form})


class CommentsView(TemplateView):
    template_name = 'comments/comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        return context


class CommentView(TemplateView):
    template_name = 'comments/commentview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = kwargs.get('pk')
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        print(comment)
        return render(request, 'comments/comment_delete.html', context={'comment': comment})

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        comment.delete()
        return redirect('comments')


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(data={'text': comment.text, 'author': comment.author})
        return render(request, 'comments/comment_update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        if form.is_valid():
            # comment.article = form.cleaned_data['article']
            comment.text = form.cleaned_data['text']
            comment.author = form.cleaned_data['author']
            comment.save()
            return redirect('comment_view', pk=comment.pk)
        else:
            return render(request, 'comments/comment_update.html', context={'form': form,  'comment': comment.pk})

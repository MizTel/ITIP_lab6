from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Article
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as logouts
from typing import Self

def archive(request):
  return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
  try:
    post = Article.objects.get(id=article_id)
    return render(request, 'article.html', {"post": post})
  except Article.DoesNotExist:
    raise Http404
def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form['title']):
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Такая статья уже существует"
                    return render(request, 'create_post.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def create_user(request):
    if not request.user.is_anonymous:
        raise Http404
    if request.method == 'POST':
        form = {
            'username': request.POST['username'],
            'mail': request.POST['mail'],
            'password': request.POST['password']
        }
        fields = (form['username'], form['mail'], form['password'])
        if None in fields or '' in fields:
            form['errors'] = u'Не все поля заполнены'
            return render(request, 'register.html', {'form': form})
        try:
            User.objects.get(username=form['username'])
            form['errors'] = u'Указанное имя пользователя занято'
            return render(request, 'register.html', {'form': form})
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(username=form['username'], email=form['mail'], password=form['password'])
        if user is None:
            form['errors'] = u'При регистрации произошла ошибка'
            return render(request, 'register.html', {'form': form})
        return redirect(archive)
    else:
        return render(request, 'register.html')
    
def input_user(request):
    if request.method == "POST":
        form = {
            'username': request.POST[ "username" ],
            'password': request.POST["password"]
        }
        if form["username"] and form["password"]:
            user = authenticate(request,username=form[ "username" ], password=form[ "password" ])
            if user is None:
                form[ 'errors'] = u"Такой пользователь не зарегестрирован! "
                return render(request, 'autoris.html', {'form': form})
            else:
                login(request, user)
            return redirect(archive)
        else:
            form['errors'] = u"Не заполнены все поля"
            return render(request, 'autoris.html', {'form': form})
    else:
        return render(request, 'autoris.html', {})
    
def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect ('home')





# Create your views here.

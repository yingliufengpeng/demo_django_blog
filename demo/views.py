from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from demo import form
from demo.models import User, Article
import uuid
from django.conf import settings
# Create your views here.


def index(request):
    # request.session.setdefault('wangpeng', 'default')
    # request.session.setdefault('xiaoxiao', 'default')

    print(request.session.get('user_id'))

    if request.session.get('user_id'):
        return render(request, 'index.html', locals())
    else:
        return render(request, 'failure.html', {'reason': '该用户未登录或者没有注册'})


def encode_password(username, salt, password):
    # 对密码进行加盐操作
    import hashlib
    md5 = hashlib.md5()
    md5.update((username + salt + password).encode('utf-8'))
    return md5.hexdigest()


# 在session中注册已经登录的用户
def create_user_info(request, user_id):
    request.session['user_id'] = user_id


def register(request):
    try:
        if request.method == 'POST':
            reg_form = form.RegForm(request.POST)
            print(reg_form.data)
            if reg_form.is_valid():
                username = reg_form.cleaned_data["username"]
                password = reg_form.cleaned_data["password"]
                user = User.objects.filter(username=username).first()
                print('user' + str(user))
                # 如果用户存在就不需要注册
                if not user:
                    # 注册
                    salt = str(uuid.uuid1()).replace('-', '')
                    user = User.objects.create(username=username,
                                        password=encode_password(username, salt, password),
                                        salt=salt)

                    # 创建相关用户的session信息
                    create_user_info(request, user.id)

                    user.save()
                    return redirect('index')
                else:
                    return render(request, 'failure.html', {'reason': '该用户已经存在!!!'})


            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = form.RegForm()
            return render(request, 'register.html', locals())
    except Exception as e:
        logging.error(e)
        return render(request, 'register.html', locals())

def logout(request):
    request.session.delete(request.session.session_key)
    return redirect('login')

def login(request):
    try:
        login_form = form.LoginForm(request.POST)
        print(login_form.data)
        if request.method == 'POST':
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = User.objects.filter(username=username).first()
                print('user: ' + str(user))
                if user:
                    salt = user.salt
                    if encode_password(username, salt, password) == user.password:
                        # 登录验证成功，重新设定session信息
                        create_user_info(request, user.id)
                        return redirect('index')
                else:
                    print('难道不会走这个路径???')
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = form.LoginForm()
            return render(request, 'login.html', locals())
    except Exception as e:
        logging.error(e)
        return render(request, 'login.html', locals())


def home(request):
    print(request.GET)
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first()
    print('user is ' + str(user))
    article_list = user.article_set.all()
    return render(request, 'home.html', locals())


def article(request):
    article_id = request.GET.get('article_id')
    print('article_id = ' + article_id)
    article = Article.objects.filter(id=article_id).first()
    return render(request, 'article.html', locals())


def add_article(request):
    article_form = form.Article()
    return render(request, 'add_article.html', locals())


def write(file, imgdir):
    import uuid
    import os
    filename = str(uuid.uuid1()).replace('-', '') + '.png'
    path = os.path.join(imgdir, filename)

    with open(path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    return settings.IMGURL + '/' + filename


@csrf_exempt
def upload_img(request):
    print(request.FILES)
    # print(request.FILES[0].field_name)
    import json
    result = {}
    result['errno'] = 0
    imgfilename = request.FILES['imgfile'].name

    file = request.FILES['imgfile']
    # 返回的结果用于回馈给客户端
    imgsrc = write(file, settings.IMGDIR)

    print('filetype' + str(type(file)))

    # print(request.scheme)
    imgs = [imgsrc]
    # print(imgfilename)


    result['data'] = imgs
    print(imgs)
    return HttpResponse(json.dumps(result))

    # return render(request, 'test.html', locals())


# 以POST提交的方式来做
def article_ajax_add(request):
    user_id = request.session.get('user_id')
    print('user_id = ' + str(user_id))
    print(request.GET.get('content'))
    if user_id:
        title = request.POST['title']
        content = request.POST['content']
        print(title)
        print(content)
        article = Article.objects.create(title=title, content=content, user_id=user_id)
        article.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error , 用户未登录或者没有注册!!!')


def modify_article(request):
    print('修改博客!!!')
    article_id = request.GET.get('article_id')
    print('article_id' + article_id)
    user_id = request.session.get('user_id')
    if user_id and article_id:
        article = Article.objects.filter(id=article_id).first()
        return render(request, 'modify_article.html', locals())
    else:
        return HttpResponse('error , 用户未登录或者没有注册!!!')


# 修改博客
def article_ajax_modify(request):
    print('提交修改的博客!!!')
    article_id = request.POST.get('article_id')
    user_id = request.session.get('user_id')
    print(str(article_id))
    print(str(user_id))
    if user_id and article_id:
        article = Article.objects.filter(id=article_id).first()
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error , 用户未登录或者没有注册!!!')


def article_ajax_delete(request):
    print('删除博客!!!')
    article_id = request.GET.get('article_id')
    user_id = request.session.get('user_id')
    print(str(article_id))
    print(str(user_id))
    if user_id and article_id:
        article = Article.objects.filter(id=article_id).first()
        article.delete()
        return HttpResponse('ok')
    else:
        return HttpResponse('error , 用户未登录或者没有注册!!!')
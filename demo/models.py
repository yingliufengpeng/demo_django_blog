from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=30, blank=True, null=True, verbose_name='邮箱')
    password = models.CharField(max_length=20, blank=True, null=True, verbose_name='密码')
    salt = models.CharField(max_length=20, blank=True, null=True, verbose_name='salt')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        # ordering = ['-id']

    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True, verbose_name='标题')
    content = models.TextField(verbose_name='文章内容')
    user = models.ForeignKey(User, verbose_name='用户')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Test(models.Model):
    username = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='用户名')


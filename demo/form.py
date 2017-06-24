
from django import forms


class RegForm(forms.Form):
    '''
    注册表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})

    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required", }),
                             max_length=50, error_messages={"required": "email不能为空", })

    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                                                      max_length=20, error_messages={"required": "password不能为空", })

    password_again = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })

class LoginForm(forms.Form):
    '''
    登录表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                               max_length=50, error_messages={"required": "username不能为空", })
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })


class Article(forms.Form):
    '''
        提交新的博客
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "标题", "required": "required", }),
                               max_length=50, error_messages={"required": "username不能为空", })

    content = forms.CharField(widget=forms.Textarea())

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginForms(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForms, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.PasswordInput(attrs={"class":"form-control"})

    username = forms.CharField(
        min_length=4,
        max_length=10
    )
    password = forms.CharField(
        min_length=6,
        max_length=20
    )

class RegisterForms(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RegisterForms, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={"class":"form-control"})
        self.fields['password'].widget = forms.PasswordInput(attrs={"class":"form-control"})
        self.fields['repassword'].widget = forms.PasswordInput(attrs={"class":"form-control"})
        self.fields['email'].widget = forms.EmailInput(attrs={"class":"form-control"})


    username = forms.CharField(
        min_length=4,
        max_length=10
    )
    password = forms.CharField(
        min_length=6,
        max_length=20
    )
    repassword = forms.CharField(
        min_length=6,
        max_length=20,
    )
    email = forms.EmailField(
        min_length=5,
        max_length=50
    )


    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise ValidationError("账号已经存在")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("邮箱已经存在")
        return email

    def clean(self):
        # print(self.cleaned_data.get('password'), self.cleaned_data.get('repassword'))
        if self.cleaned_data.get('password') != self.cleaned_data.get('repassword'):
            self.add_error('repassword',"两次密码不一致")
            raise ValidationError("两次密码不一致")
        return self.cleaned_data


class UserInfo(forms.Form):
    # username = forms.CharField(
    #     min_length=4,
    #     max_length=10
    # )
    # password = forms.CharField(
    #     min_length=6,
    #     max_length=20
    # )
    # email = forms.EmailField(
    #     min_length=5,
    #     max_length=50
    # )
    avatar = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__(*args, **kwargs)
        # self.fields['username'].widget = forms.TextInput(attrs={"class":"form-control"})
        # self.fields['password'].widget = forms.PasswordInput(attrs={"class":"form-control"})
        # self.fields['email'].widget = forms.PasswordInput(attrs={"class":"form-control"})
        self.fields['avatar'].widget.attrs["class"]="form-control"
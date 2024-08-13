from django import forms
from django.contrib.auth.models import User

from online_shop.models import Comment, Order, Product


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product',)

    def clean_body(self):
        negative_messages = ['salom', 'kam', 'qimmat', 'yaxshimas', 'q']
        body = self.data.get('body')
        my_list1 = body.split(',')
        my_list2 = body.split(' ')
        if negative_messages in my_list1 or negative_messages in my_list2:
            raise forms.ValidationError('Mahsulot yaxshi negative bo\'lma😒')
        return body


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if not User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Invalid username')
    #     return username


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} is already exists')
        return username

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user

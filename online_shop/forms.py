from django import forms

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

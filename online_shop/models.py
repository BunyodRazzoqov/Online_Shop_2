from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'Categories'


class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,
                                              null=True)
    discount = models.PositiveSmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)

        return self.price

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Products'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    class Meta:
        db_table = 'Orders'


class Comment(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    body = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    is_provide = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}-{self.created_at}'

    class Meta:
        db_table = 'Comments'

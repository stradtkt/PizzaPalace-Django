from __future__ import unicode_literals
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType



class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be 2 or more characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be 2 or more characters"
        if len(postData['first_name']) > 30:
            errors['first_name'] = "First name needs to be less then 30 characters"
        if len(postData['last_name']) > 30:
            errors['last_name'] = "Last name needs to be less then 30 characters"
        if not postData['first_name'].isalpha():
            errors['first_name'] = "First name needs to be only letters"
        if not postData['last_name'].isalpha():
            errors['last_name'] = "Last name needs to be only letters"
        if len(postData['street_address']) < 3:
            errors['street_address'] = "Your street address must contain more characters than that" 
        if len(postData['street_address']) > 50:
            errors['street_address'] = "Your street address can be no longer than 50 characters"
        if len(postData['city']) < 3:
            errors['city'] = "Your street address must contain 3 or more characters" 
        if len(postData['city']) > 50:
            errors['city'] = "Your city can be no longer than 50 characters"
        if len(postData['zip_code']) < 5:
            errors['zip_code'] = "Your street address must contain 5 or more characters" 
        if len(postData['zip_code']) > 9:
            errors['zip_code'] = "Your city can be no longer than 9 characters"
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = "Your email is not valid"
        else:
            if User.objects.filter(email=postData['email']):
                errors['email'] = "This email already exists"
        if len(postData['password']) < 4:
            errors['password'] = "Please enter a longer password, needs to be four or more characters"
        if postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Passwords must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    street_address = models.CharField(max_length=500)
    apt_ste_floor = models.CharField(max_length=255, default=None)
    number = models.IntegerField(default=0)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    nickname = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class DeliveryTempAddressManager(models.Manager):
    def validate_temp_address(self, postData):
        errors = {}
        if len(postData['street_address']) < 3:
            errors['street_address'] = "Your street address must contain more characters than that" 
        if len(postData['street_address']) > 50:
            errors['street_address'] = "Your street address can be no longer than 50 characters"
        if len(postData['city']) < 3:
            errors['city'] = "Your street address must contain 3 or more characters" 
        if len(postData['city']) > 50:
            errors['city'] = "Your city can be no longer than 50 characters"
        if len(postData['zip_code']) < 5:
            errors['zip_code'] = "Your street address must contain 5 or more characters" 
        if len(postData['zip_code']) > 9:
            errors['zip_code'] = "Your city can be no longer than 9 characters"
        return errors

class DeliveryTempAddress(models.Model):
    street_address = models.CharField(max_length=500)
    apt_ste_floor = models.CharField(max_length=255, default=None)
    number = models.IntegerField(default=0)
    zip_code = models.CharField(max_length=20)
    objects = DeliveryTempAddressManager()



class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name="creation date", auto_now_add=True)
    checked_out = models.BooleanField(default=False, verbose_name=('checked out'))

    class Meta:
        verbose_name="cart"
        verbose_name_plural="carts"
        ordering=('-creation_date',)
        
class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    qty = models.PositiveIntegerField(verbose_name=('quantity'))
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=('price'))
    cart = models.ForeignKey(Cart, related_name="cart", on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content Type"), on_delete=models.CASCADE)
    def get_total_price(self):
        return self.price * self.qty
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_models(type(product))
        self.object_id = product.pk
    product = property(get_product, set_product)


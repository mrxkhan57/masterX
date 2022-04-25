from django.db import models
import random
from datetime import datetime
from django.db.models.fields import BLANK_CHOICE_DASH
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

class Ads(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField()
    spcategory = models.ForeignKey('SuperCategory', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="ADS/%y/%m/%d", blank=True, null=True)
    
    def __str__(self):
        return self.name

class AboutUs(models.Model):
    website = models.CharField(max_length=500, blank=True, null=True, default=None)
    email = models.EmailField(max_length=300, blank=True, null=True, default=None)
    phone1 = models.CharField(max_length=12, blank=True, null=True, default=None)
    phone2 = models.CharField(max_length=12, blank=True, null=True, default=None)
    phone3 = models.CharField( max_length=12, blank=True, null=True, default=None)

    def __str__(self):
        return self.website

class Client(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    number = models.CharField(max_length=12, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class ClientIPLogList(models.Model):
    date = models.TimeField(auto_now_add=True)
    client_ip = models.GenericIPAddressField(null=True)

    def __str__(self):
        return "{}".format(self.client_ip)

class ClientCodeGen(models.Model):
    phone_number = models.CharField(max_length=12, blank=True)
    code = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.phone_number
    
    def save(self, *args, **kwargs):
        if self.phone_number:
            number_list = [x for x in range(10)]
            code_items = []

            for i in range(6):
                num = random.choice(number_list)
                code_items.append(num)

            code_string = "".join(str(item) for item in code_items)
            self.code = code_string
            super().save(*args, **kwargs)

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=300, blank=True, null=True)
    admin_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True, unique=True)
    passwd = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to='Vendor/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.photo:
            imageTemproary = Image.open(self.photo)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (200,200) ) 
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=100)
            outputIoStream.seek(0)
            self.photo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 
                                                'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Vendor, self).save(*args, **kwargs)

class SuperCategory(models.Model):
    ai = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(upload_to='SuperCategory/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    ai = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    super = models.ForeignKey('SuperCategory', related_name='category', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Category/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey('Category', related_name='subcategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(upload_to = 'SubCategory/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(upload_to='Brand/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.photo:
            imageTemproary = Image.open(self.photo)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (190,140) ) 
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=100)
            outputIoStream.seek(0)
            self.photo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 
                                                'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Brand, self).save(*args, **kwargs)

class Gender(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Update(models.Model):
    update_product = models.BooleanField(default=False)
    
class Visited(models.Model):
    visit = models.IntegerField(default=0)

class Location(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user_phone = models.CharField(max_length=12, blank=True, null=True)
    user_email = models.EmailField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.user_phone

class Exchange(models.Model):
    exchange = models.FloatField()

    def __str__(self):
        return str(self.exchange)

class Discount(models.Model):
    discount = models.FloatField()

    def __str__(self):
        return str(self.discount)

class Product(models.Model):
    supercategory = models.ForeignKey('SuperCategory', related_name='products' ,on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE)
    vendor_name = models.ForeignKey('Vendor', related_name='products', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=300, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(null=True)
    stock_number = models.IntegerField(default=0)
    visited = models.IntegerField(default=0)
    in_dollar = models.FloatField(blank=True, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    discounted_price = models.FloatField(blank=True, null=True)
    new_price = models.FloatField(blank=True, null=True)
    calc_dollar = models.BooleanField(default=False)
    calc_discount = models.BooleanField(default=False)
    color = models.ForeignKey('Color', related_name='products', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', related_name='products', on_delete=models.CASCADE)
    gender = models.ForeignKey('Gender', related_name='products', on_delete=models.CASCADE)
    new = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=False)
    barcode = models.CharField(max_length=500, null=True, blank=True)
    photo1 = models.ImageField(upload_to = 'Photo_1/%y/%m/%d', blank=True, null=True)
    photo2 = models.ImageField(upload_to = 'Photo_2/%y/%m/%d', blank=True, null=True)
    photo3 = models.ImageField(upload_to = 'Photo_3/%y/%m/%d', blank=True, null=True)
    photo4 = models.ImageField(upload_to = 'Photo_4/%y/%m/%d', blank=True, null=True)
    ip_pro = models.GenericIPAddressField(null=True)

    def save(self, *args, **kwargs):
        if self.calc_dollar is True and self.in_dollar is not None:
            self.new_price = self.in_dollar * float(self.exchange.exchange)
            self.price = 0
        else:
            self.new_price = 0
        if self.calc_discount is True and self.price is not None:
            self.discounted_price = (self.price * float(self.discount.discount))/100
            self.new_price = self.price - self.discounted_price
        else:
            self.discounted_price = 0
        if self.calc_discount is False and self.calc_dollar is False:
            self.new_price = self.price
        if self.price is None:
            self.price = 0
        if self.new_price is None:
            self.new_price = 0
        if self.in_dollar is None:
            self.in_dollar = 0
        if self.calc_discount is False:
            self.discounted_price = None
        if self.discounted_price is None:
            self.discounted_price = 0
        if self.calc_discount is True and self.calc_dollar is True:
            self.price = self.in_dollar * float(self.exchange.exchange)
            self.discounted_price = (self.price * float(self.discount.discount))/100
            self.new_price = self.price - self.discounted_price
        if self.name:
            date_ap = []
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
            date_ap.append(dt_string)
            date_string = "".join(str(item) for item in date_ap)
            self.date = date_string
        self.in_dollar = round(self.in_dollar, 2)
        self.price = round(self.price, 2)
        self.new_price = round(self.new_price, 2)
        self.discounted_price = round(self.discounted_price, 2)
        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(max_length=300, blank=True, null=True)
    name_order = models.CharField(max_length=300, blank=True, null=True)
    vendor_name = models.CharField(max_length=300, blank=True, null=True)
    adress = models.CharField(max_length=500, blank=True, null=True)
    user_name = models.CharField(max_length=300, blank=True, null=True)
    user_email = models.EmailField(max_length=300, blank=True, null=True, default=None)
    user_phone = models.CharField(max_length=300, blank=True, null=True)
    order_note = models.CharField(max_length=1000, blank=True, null=True)
    completed = models.BooleanField(default=False)
    in_process = models.BooleanField(default=False)
    color = models.CharField(max_length=500, blank=True, null=True)
    size = models.CharField(max_length=500, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True)
    price_order = models.FloatField()
    quantity = models.FloatField()
    result = models.FloatField(blank=True, null=True)
    photo = models.CharField(max_length=1000, blank=True, null=True)
    file_xlsx = models.FileField()
    
    def save(self, *args, **kwargs):
        date_ap = []
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
        date_ap.append(dt_string)
        date_string = "".join(str(item) for item in date_ap)
        self.date = date_string
        if self.quantity:
            self.result = self.price_order * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_order
class Meta:
    db_table = 'Order'
    

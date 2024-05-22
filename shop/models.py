from django.db import models
import datetime as dt
import os
from django.contrib.auth.models import User
def getfile(instance, filename):
    nowtime = dt.datetime.now().strftime("%y%m%d:%H:%M:%S")  # Corrected the format string
    newname = "%s%s" % (nowtime, filename)
    return os.path.join('uploads/', newname)

class Catageory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getfile, null=True, blank=True)  # Fixed function name
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    catageory = models.ForeignKey(Catageory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=getfile, null=True, blank=True)  # Fixed function name
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-show,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
        


class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
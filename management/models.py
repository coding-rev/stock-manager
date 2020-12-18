from django.db import models
from PIL import Image
from django.contrib.auth.models import User

from django.forms import ModelForm
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Sum


#Customers Arena
CUSTOMER_CHOICES =[
    ('WHOLESALER','WHOLESALER'),
    ('AGENT','AGENT'),
    ('BOOKSHOP','BOOKSHOP'),
    ('SPECIALIZED CUSTOMER','SPECIALIZED CUSTOMER'),
    ('RETAIL','RETAIL'),
    ('SCHOOL','SCHOOL'),
    ('OTHERS','OTHERS'),
 ]   

DISCOUNT_CHOICES =[
	(5, 5),
	(10, 10),
	(15, 15),
	(20, 20),
	(25, 25),
	(30, 30),
	(35, 35),
	(40, 40),
	(45, 45),
	(50, 50),
	(100, 100),
]

class Customer(models.Model):
	name = models.CharField(max_length=50, unique=True)
	image = models.ImageField(upload_to='customers_pics', default='default-user.png')
	phone = models.CharField(max_length=11)
	email = models.EmailField(blank=True, null=True)
	group = models.CharField(choices=CUSTOMER_CHOICES, max_length=100)
	discount = models.IntegerField(default=0,choices=DISCOUNT_CHOICES ,blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
	#book_received = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)	
	amount_paid = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	class Meta:
		verbose_name_plural = 'CUSTOMERS'
    
	def __str__(self):
		return self.name


#Customers Ends here  


class Category(models.Model):
	category = models.CharField(max_length=200, unique=True)
	class Meta:
		verbose_name_plural = 'CATEGORY'
    
	def __str__(self):
		return self.category



class Stock(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='books')
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	price = models.IntegerField(default='0')
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50,blank=True, null=True)
	receive_from = models.CharField(max_length=100, blank=True, null=True)
	receive_cost = models.IntegerField(default='0', blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.ForeignKey(Customer ,on_delete=models.CASCADE, blank=True, null=True)
	issue_cost = models.IntegerField(default='0', blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50,blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	export_to_CSV = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
	amount_paid = models.IntegerField(default='0', blank=True, null=True)

	class Meta:
		verbose_name_plural = 'BOOKS'
    
	def __str__(self):
		return self.item_name


class StockHistory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	price = models.IntegerField(default='0')
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	receive_from = models.CharField(max_length=100, blank=True, null=True)
	receive_cost = models.IntegerField(default='0', blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.ForeignKey(Customer ,on_delete=models.CASCADE, blank=True, null=True)
	issue_cost = models.IntegerField(default='0', blank=True, null=True)
	amount_paid = models.IntegerField(default='0', blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	export_to_CSV = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	#Dealing with Totals
	#total_issue_price = models.IntegerField(default='0', blank=True, null=True)
	#total_receive_price = models.IntegerField(default='0', blank=True, null=True)

	class Meta:
		verbose_name_plural = 'STOCK HISTORY'
		ordering = ['-last_updated']





class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    class Meta:
        verbose_name_plural = 'CHAT'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
    




class CustomerHistory(models.Model):
	name = models.CharField(max_length=50)
	book_received = models.CharField(max_length=300)
	book_price = models.PositiveIntegerField(default='0', blank=True, null=True)
	quantity_collected = models.PositiveIntegerField(default='0', blank=True, null=True)
	total_cost_price = models.PositiveIntegerField(default='0', blank=True, null=True)
	discount = models.IntegerField(default=0, choices=DISCOUNT_CHOICES ,blank=True, null=True)
	debt = models.PositiveIntegerField(default='0', blank=True, null=True)	
	amount_paid = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
		
	class Meta:
		verbose_name_plural = "CUSTOMER'S HISTORY"

	@property
	def debt(self):
		return self.total_cost_price-self.amount_paid
        




	
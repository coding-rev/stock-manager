from django import forms
from .models import Stock, Category, Customer, CustomerHistory, StockHistory

#Customers
class CustomerCreateForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['image','name','phone','email','group']

	
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if not name:
			raise forms.ValidationError('This field is required')
		return name


	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if not phone:
			raise forms.ValidationError('This field is required')
		return phone

	def clean_group(self):
		group = self.cleaned_data.get('group')
		if not group:
			raise forms.ValidationError('This field is required')
		return group

class CustomerHistoryUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomerHistory
		fields = ['amount_paid']


class CustomerSearchForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name']

#For multiple search

#class CustomerSearchForm(forms.ModelForm):
#	class Meta:
#		model = Customer
#		fields = ['name', 'phone']





#Stock alert
class ReorderLevelForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	class Meta:
		model = Stock
		fields = ['category', 'item_name']
		

class StockSearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	class Meta:
		model = Stock
		fields = ['item_name','export_to_CSV']

class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	class Meta:
		model = StockHistory
		fields = ['issue_by','export_to_CSV']

class StockCreateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name','image' ,'price' ,'quantity','created_by']

	
	def clean_category(self):
		category = self.cleaned_data.get('category')
		if not category:
			raise forms.ValidationError('This field is required')
		return category


	def clean_item_name(self):
		item_name = self.cleaned_data.get('item_name')
		if not item_name:
			raise forms.ValidationError('This field is required')
		return item_name


class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'image']

	
#==========================================================
#Real calculations
#==========================================================

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'amount_paid','issue_to']
	
	def compare(self):
		issue_quantity = self.cleaned_data.get('issue_quantity')
		quantity = Stock.objects.get('quantity')
		if issue_quantity > quantity:
			raise forms.ValidationError('Issue Quantity greater than Quantity left in stock')
		return issue_quantity


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_from']


#==========================================================
# Adding Class and category field
#==========================================================
class CatetoryCreateForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['category']

	def block_duplicate(self):
		for instance in Category.objects.all():
			if instance.category == category:
				raise forms.ValidationError(str(category) + ' is already created')
		return category

	def clean_category(self):
		category = self.cleaned_data.get('category')
		if not category:
			raise forms.ValidationError('This field is required')
		return category

#=============================================================
# Summary Filter
#=============================================================

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Stock, StockHistory, Comment, CommentForm, Customer, CustomerHistory, Category
from .forms import CustomerHistoryUpdateForm, StockHistorySearchForm, CustomerSearchForm, CustomerCreateForm,StockCreateForm, StockUpdateForm, StockSearchForm, IssueForm, ReceiveForm, ReorderLevelForm, CatetoryCreateForm
from django.db.models import Q

from django.http import HttpResponse
import csv

#Admin Area Template Modification view
@login_required
def home(request):
	title = 'Welcome: This is the Home Page'
	stocks = Stock.objects.all()
	customers = Customer.objects.all()
	categories = Category.objects.all()
	users = User.objects.all()
	customer_history = CustomerHistory.objects.all()

	context = {
	"title": title,
	"stocks":stocks,
	"customers":customers,
	"categories":categories,
	"users":users,
	"customer_history":customer_history,
	}
	return render(request, "management/index.html",context)

@login_required
def chat(request):
    comments= Comment.objects.all().order_by('-create_at')
    all_users = get_user_model().objects.all()
    context ={
        'comments':comments,
        'allusers':all_users,
    }
    return render(request, 'management/chat.html', context)


@login_required
def addcomment(request):
    url = request.META.get('HTTP_REFERER')
    #return HttpResponse(url)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            return HttpResponseRedirect(url)
        else:
            messages.info(request, "Poor Internet Connection")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@login_required
def list_item(request):
	title = 'List of Items'
	queryset = Stock.objects.all().order_by('category')
	form = StockSearchForm(request.POST or None)
	if form['export_to_CSV'].value() == True:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
		writer = csv.writer(response)
		writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
		instance = queryset
		for stock in instance:
			writer.writerow([stock.category, stock.item_name, stock.quantity])
		return response
	else:
		if request.method == 'POST':
			queryset = Stock.objects.filter(
				item_name__icontains=form['item_name'].value()
				)

	context = {
		"form":form,
		"title": title,
		"queryset": queryset,
	}
	return render(request, "management/list_item.html", context)


#Stock reorder alert
@login_required
def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "management/add_items.html", context)


@login_required
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "management/stock_detail.html", context)


@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_items')
        		
	
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "management/add_items.html", context)

@login_required
def add_category(request):
	form = CatetoryCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_items')
	
	context = {
		"form": form,
		"title": "Add Category",
	}
	return render(request, "management/add_category.html", context)

@login_required
def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Item Deleted Successfully')
		return redirect('/list_items')
	return render(request, 'management/delete_items.html')


@login_required
def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, request.FILES or None,instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Item Updated Successfully')
			return redirect('/list_items')

	context = {
		'form':form
	}
	return render(request, 'management/update_item.html', context)

#===============================================================
# Dealing with  issuance and receive
#===============================================================
#current_user = request.user
#            data.user_id = current_user.id

@login_required
def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	customer = Customer.objects.all()
	existing_quantity = queryset.quantity
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		if instance.issue_quantity > instance.quantity:
			messages.info(request, "Failed!. Quantity left in store is "+str(existing_quantity))
			url = request.META.get('HTTP_REFERER')
			return HttpResponseRedirect(url)
		else:
			if instance.issue_to.discount != None:
				#Calculating for discount
				get_customer_discount = instance.issue_to.discount 
				instance.issue_to.discount = instance.issue_to.discount / 100
				instance.issue_to.discount = (instance.price * instance.issue_quantity)*instance.issue_to.discount 
				instance.issue_to.discount = (instance.price * instance.issue_quantity)-instance.issue_to.discount
				#Discount calculation ended
				instance.receive_quantity = 0
				instance.quantity -= instance.issue_quantity
				instance.receive_cost = instance.quantity * instance.price
				instance.issue_by = str(request.user)
				instance.issue_to = instance.issue_to
				instance.amount_paid = instance.amount_paid
				instance.item_name = instance.item_name
				instance.price = instance.price
				instance.issue_cost = instance.issue_to.discount
				instance.save()

				if instance.amount_paid > instance.issue_cost:
					messages.info(request, "Failed!!! Can't pay more than cost. Please try again. Total cost is GHc "+str(instance.issue_cost))
					url = request.META.get('HTTP_REFERER')
					return HttpResponseRedirect(url)
				else:
					messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + " Books now left in Store")
					customer_history = CustomerHistory(
						name = instance.issue_to,
						book_received = instance.item_name,
						book_price = instance.price,
						total_cost_price = instance.issue_cost,
						discount = get_customer_discount,
						quantity_collected= instance.issue_quantity,
						amount_paid = instance.amount_paid,
						)
					customer_history.save()

					issue_history = StockHistory(
						last_updated = instance.last_updated,
						category_id = instance.category_id,
						item_name = instance.item_name,
						price = instance.price, 
						quantity = instance.quantity, 
						issue_to = instance.issue_to, 
						issue_by = instance.issue_by, 
						issue_quantity = instance.issue_quantity, 
						issue_cost = instance.issue_cost,
						amount_paid = instance.amount_paid
						)
					issue_history.save()

			else:
				instance.issue_to.discount
				instance.receive_quantity = 0
				instance.quantity -= instance.issue_quantity
				instance.receive_cost = instance.quantity * instance.price
				instance.issue_by = str(request.user)
				instance.issue_to = instance.issue_to
				instance.amount_paid = instance.amount_paid
				instance.item_name = instance.item_name
				instance.price = instance.price
				instance.issue_cost = instance.price * instance.issue_quantity
				instance.save()

				if instance.amount_paid > instance.issue_cost:
					messages.info(request, "Failed!!! Can't pay more than cost. Please try again. Total cost is GHc "+str(instance.issue_cost))
					url = request.META.get('HTTP_REFERER')
					return HttpResponseRedirect(url)
				else:
					messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + " Books now left in Store")
					customer_history = CustomerHistory(
						name = instance.issue_to,
						book_received = instance.item_name,
						book_price = instance.price,
						total_cost_price = instance.issue_cost,
						quantity_collected= instance.issue_quantity,
						amount_paid = instance.amount_paid,
						)
					customer_history.save()

					issue_history = StockHistory(
						last_updated = instance.last_updated,
						category_id = instance.category_id,
						item_name = instance.item_name,
						price = instance.price, 
						quantity = instance.quantity, 
						issue_to = instance.issue_to, 
						issue_by = instance.issue_by, 
						issue_quantity = instance.issue_quantity, 
						issue_cost = instance.issue_cost,
						amount_paid = instance.amount_paid
						)
					issue_history.save()


			return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "management/issue_item.html", context)


@login_required
def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.issue_cost = 0
		instance.quantity += instance.receive_quantity
		instance.receive_by = str(request.user)
		instance.receive_from = instance.issue_to
		instance.item_name = instance.item_name
		instance.price = instance.price
		instance.receive_cost = instance.price * instance.receive_quantity
		instance.save()
		receive_history = StockHistory(
			last_updated = instance.last_updated,
			category_id = instance.category_id,
			item_name = instance.item_name,
			price = instance.price, 
			quantity = instance.quantity, 
			receive_quantity = instance.receive_quantity, 
			receive_by = instance.receive_by,
			receive_from = instance.receive_from,
			receive_cost = instance.receive_cost
			)
		receive_history.save()

		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "management/receive_item.html", context)



#================================================================
@login_required
def list_history(request):
	header = 'LIST OF ITEMS'
	queryset = StockHistory.objects.all()
	
	form = StockHistorySearchForm(request.POST or None)
	if form['export_to_CSV'].value() == True:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="Excellence Stock History.csv"'
		writer = csv.writer(response)

		writer.writerow([
			'CATEGORY', 'ITEM NAME',
			'QUANTITY IN STORE', 'ISSUE QUANTITY', 
			'RECEIVE QUANTITY', 'LAST UPDATED',
			'ISSUE BY','ISSUE TO', 'ISSUE COST (Ghc)',
			'AMOUNT PAID','RECEIVE BY', 'RECEIVE FROM', 'RECEIVE COST (Ghc)',
			])
		instance = queryset
		for stockhistory in instance:
			writer.writerow([
				stockhistory.category, stockhistory.item_name, 
				stockhistory.quantity,stockhistory.issue_quantity,
				stockhistory.receive_quantity, stockhistory.last_updated,
				stockhistory.issue_by, stockhistory.issue_to,
				stockhistory.issue_cost, stockhistory.amount_paid, 
				stockhistory.receive_by,
				stockhistory.receive_from, stockhistory.receive_cost,
				])
		return response
	else:
		if request.method == 'POST':
			queryset = StockHistory.objects.filter(
				issue_by__icontains=form['issue_by'].value()
				)

	context = {
		"form":form,
		"header": header,
		"queryset": queryset,
	}
	return render(request, "management/list_history.html",context)



@login_required
def base(request):
    return render(request, 'management/base.html')





#Customer Fields
@login_required
def list_customers(request):
	title = 'List of Items'
	queryset = Customer.objects.all().order_by('name')
	form = CustomerSearchForm(request.POST or None)
	if request.method == 'POST':
		queryset = Customer.objects.filter(
			name__icontains=form['name'].value()
			)

	context = {
		"form":form,
		"title": title,
		"queryset": queryset,
	}
	return render(request, "management/list_customer.html", context)
#LOGIC FOR MULTIPLE SEARCH

#if request.method == 'POST':
#		queryset = Customer.objects.filter(
#			name__icontains=form['name'].value(),
#			phone__icontains = form['phone'].value()
#			)


@login_required
def customer_detail(request, pk):
	queryset = Customer.objects.get(id=pk)
	customer_history = CustomerHistory.objects.filter(name=queryset.name).order_by('-last_updated')
	context = {
		"title": queryset.name,
		"queryset": queryset,
		"customer_history":customer_history,
	}
	return render(request, "management/customer_details.html", context)


@login_required
def update_customer_history(request, pk):
	queryset = CustomerHistory.objects.get(id=pk)
	existing_amount_paid = queryset.amount_paid
	existing_debt = queryset.debt
	form = CustomerHistoryUpdateForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		if instance.amount_paid > instance.total_cost_price:
			messages.info(request, "Failed!!! Can't pay more than cost. You've already paid " +str(existing_amount_paid) + ". Amount left is GHc" + str(existing_debt) )
			url = request.META.get('HTTP_REFERER')
			return HttpResponseRedirect(url)
		else:	
			form.save()
			messages.success(request, 'Payment Successfull. '+ str(queryset.name) )
			return redirect('/list_customers')

	context = {
		'form':form
	}
	return render(request, 'management/update_item.html', context)


@login_required
def add_customer(request):
	form = CustomerCreateForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Customer created Successfully!')
		return redirect('/list_customers')
       		
	
	context = {
		"form": form,
	}
	return render(request, "management/add_items.html", context)




#======================================================
# category page
#======================================================
@login_required
def list_categories(request):
	title = 'List of Items'
	queryset = Category.objects.all()
	
	context = {
		"title": title,
		"queryset": queryset,
	}
	return render(request, "management/list_categories.html", context)




#==================================================================
# Manager's summary view
#==================================================================
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manager_summary(request):
	totals = CustomerHistory.objects.all().order_by('-last_updated')
	
	if request.method == 'POST':
		fromdate=request.POST.get('fromdate')
		todate=request.POST.get('todate')
		
		if fromdate == todate:
			totals = CustomerHistory.objects.filter(last_updated__icontains=fromdate)
			#Calculating Total income   
			income_list = []
			for i in totals:
				numbers = i.amount_paid
				income_list.append(numbers)
			
			#Calculating Total Debt
			debt_list = []
			for i in totals:
				numbers = i.debt
				debt_list.append(numbers)
			
			#Calculating Purchased Books Quantity
			books_sold_list = []
			for i in totals:
				numbers = i.quantity_collected
				books_sold_list.append(numbers)
			
			#End of post filters
			context = {
			"income_list":sum(income_list),
			"debt_list":sum(debt_list),
			"books_sold_list":sum(books_sold_list),
			"fromdate":fromdate,
			"todate":todate,
			"totals":totals,
			}

			return render(request, "management/summary.html", context)
		else:
			totals = CustomerHistory.objects.filter(last_updated__range=[fromdate, todate])

			#Calculating Total income   
			income_list = []
			for i in totals:
				numbers = i.amount_paid
				income_list.append(numbers)
			
			#Calculating Total Debt
			debt_list = []
			for i in totals:
				numbers = i.debt
				debt_list.append(numbers)
			
			#Calculating Purchased Books Quantity
			books_sold_list = []
			for i in totals:
				numbers = i.quantity_collected
				books_sold_list.append(numbers)
			
			#End of post filters
			context = {
			"income_list":sum(income_list),
			"debt_list":sum(debt_list),
			"books_sold_list":sum(books_sold_list),
			"fromdate":fromdate,
			"todate":todate,
			"totals":totals,
			}

			return render(request, "management/summary.html", context)

	else:
		#All Filter
		#Calculating Total income   
		income_list = []
		for i in totals:
			numbers = i.amount_paid
			income_list.append(numbers)
		
		#Calculating Total Debt
		debt_list = []
		for i in totals:
			numbers = i.debt
			debt_list.append(numbers)
		
		#Calculating Purchased Books Quantity
		books_sold_list = []
		for i in totals:
			numbers = i.quantity_collected
			books_sold_list.append(numbers)
		

		context = {
			"income_list":sum(income_list),
			"debt_list":sum(debt_list),
			"books_sold_list":sum(books_sold_list),
			"totals":totals,
		}

		return render(request, "management/summary.html", context)
from django.urls import path
from .import views


app_name='management'

urlpatterns = [
	path('', views.home, name='home'),
	path('chat-sending/', views.addcomment, name='addcomment'),
	path('chat/', views.chat, name='chat'),
	path('list_items/', views.list_item, name='list_items'),
	path('list_customers/', views.list_customers, name='list_customers'),
	path('list_categories/', views.list_categories, name='list_categories'),
	path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
	path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
	path('customer_detail/<str:pk>/', views.customer_detail, name="customer_detail"),
	path('add_items/', views.add_items, name='add_items'),
	path('add_customer/', views.add_customer, name='add_customer'),
	path('add_category/', views.add_category, name='add_category'),
	#path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
	#path('update_items/<str:pk>/', views.update_items, name="update_items"),
	path('update_customer_history/<str:pk>/', views.update_customer_history, name="update_customer_history"),
	path('list_history/', views.list_history, name='list_history'),
	path('base/', views.base, name='base'),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
	path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),

	path('stock_summary/', views.manager_summary, name='manager_summary'),
 
]
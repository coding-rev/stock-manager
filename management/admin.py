from django.contrib import admin
from .models import Stock, Category, StockHistory, Comment, Customer, CustomerHistory #Summary
from .forms import StockCreateForm, CatetoryCreateForm

class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['item_name', 'category', 'price','quantity']
   form = StockCreateForm
   list_filter = ['category']
   search_fields = ['category', 'item_name']

class StockHistoryAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'price','issue_by', 'issue_cost', 'amount_paid','issue_quantity', 'receive_from','receive_cost','receive_quantity','last_updated']
   list_filter = ['last_updated','issue_to' ,'category','item_name','issue_by','receive_by']
   search_fields = ['issue_by','receive_by','last_updated']

class CustomerHistoryAdmin(admin.ModelAdmin):
   list_display = ['name','book_received', 'book_price', 'total_cost_price','quantity_collected','debt','amount_paid', 'last_updated']
   list_filter = ['book_received','last_updated','name']
   search_fields = ['name','book_received']

class CategoryCreateAdmin(admin.ModelAdmin):
   list_display = ['category']
   form = CatetoryCreateForm
   
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment','create_at']
    list_filter = ['user']
    random_fields = ('comment', 'ip', 'user')

class CustomerAdmin(admin.ModelAdmin):
   list_display = ['name','discount']
   list_filter = ['name','discount']

  

admin.site.site_header = 'EXCELLENCE PUBLICATION AND STATIONERY LIMITED - SUPERUSER'
admin.site.site_title = 'EXCELLENCE CPANEL'

#How to unregister Default fields( Eg: Group)
from django.contrib.auth.models import Group
admin.site.unregister(Group)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerHistory, CustomerHistoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category, CategoryCreateAdmin)
admin.site.register(StockHistory, StockHistoryAdmin)
#admin.site.register(Summary)
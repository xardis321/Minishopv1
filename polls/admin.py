from django.contrib import admin
from .models import Inventory, Suppliers, Customers, Invoice, PurchaseOrder, CustomerItems, SupplierItems

# Rejestracja modeli w panelu administracyjnym

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'description', 'quantity', 'purchasePrice', 'salePrice')

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ('sName',)

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('cName',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'iPubDate', 'iTotal', 'iComplete')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'pubDate', 'total', 'complete')

@admin.register(CustomerItems)
class CustomerItemsAdmin(admin.ModelAdmin):
    list_display = ('cItem', 'amount')

@admin.register(SupplierItems)
class SupplierItemsAdmin(admin.ModelAdmin):
    list_display = ('sItem', 'amount')

# Dodatkowe dostosowanie panelu administracyjnego

admin.site.site_header = "Minishop Admin"
admin.site.site_title = "Minishop Admin Panel"
admin.site.index_title = "Welcome to Minishop Admin Panel"

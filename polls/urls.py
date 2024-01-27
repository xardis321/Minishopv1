from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.InvoiceOfSalesView.as_view(), name="invoice_of_sales"),
    path("invoice-of-sales/", views.InvoiceOfSalesView.as_view(), name="invoice_of_sales"),
    path("purchase-order/", views.PurchaseOrderView.as_view(), name="purchase_order"),
    path("income-and-expenditure/", views.IncomeAndExpenditureView.as_view(), name="income_and_expenditure"),
    path("reports/", views.ReportsView.as_view(), name="reports"),
    path("add-item/", views.AddItemView.as_view(), name="add_item"),
    path("save_customer_items/", views.SaveCustomerItemsView.as_view(), name="save_customer_items"),
    path("check_customer_exists/", views.CheckCustomerExistsView.as_view(), name="check_customer_exists"),
    path("add_customer/", views.AddCustomerView.as_view(), name="add_customer"),
    path("save_supplier_items/", views.SaveSupplierItemsView.as_view(), name="save_supplier_items"),
    path("check_supplier_exists/", views.CheckSupplierExistsView.as_view(), name="check_supplier_exists"),
    path("add_supplier/", views.AddSupplierView.as_view(), name="add_supplier"),
    path("api/mark_invoice_complete/<int:invoice_id>/", views.MarkInvoiceComplete.as_view(), name="mark_invoice_complete"),
    path("api/mark_purchase_order_complete/<int:purchase_order_id>/", views.MarkPurchaseOrderComplete.as_view(), name='mark_purchase_order_complete'),
]

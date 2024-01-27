from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Inventory, Customers, Invoice, CustomerItems, Suppliers, SupplierItems, PurchaseOrder
from datetime import datetime
from django.core.exceptions import ValidationError
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class InvoiceOfSalesView(View):
    def get(self, request):
        inventory_data = Inventory.objects.all()
        customers = Customers.objects.all()
        current_date = datetime.now().strftime("%Y-%m-%d")
        return render(request, 'polls/invoice_of_sales.html', {'inventory_data': inventory_data, 'customers': customers, 'current_date': current_date})
    
class SaveCustomerItemsView(View):
    def post(self, request):
        data = json.loads(request.body)
        customer_name = data.get('customer')
        invoice_date = data.get('iPubDate')
        total_amount = data.get('iTotal')
        items = data.get('items')

        if not customer_name:
            return JsonResponse({'error': 'Please provide a customer name.'}, status=400)

        if not invoice_date:
            return JsonResponse({'error': 'Please provide an invoice date.'}, status=400)

        if not total_amount:
            return JsonResponse({'error': 'Please provide a total amount.'}, status=400)

        customer, created = Customers.objects.get_or_create(cName=customer_name)

        invoice = Invoice(customer=customer, iPubDate=invoice_date, iTotal=total_amount, iComplete=False)
        invoice.save()

        # First, save all items to CustomerItems
        if items:
            self.save_customer_items(invoice, items)

        # Then, update the quantity of items in Inventory
        self.update_inventory_quantity(items)

        return JsonResponse({'message': 'Customer items saved successfully.'})

    def save_customer_items(self, invoice, items):
        for item_data in items:
            item_id = item_data.get('item_id')
            amount = item_data.get('amount')

            if item_id and amount and amount >= 1:
                try:
                    item = Inventory.objects.get(id=item_id)
                except Inventory.DoesNotExist:
                    # The item doesn't exist in the Inventory, so we'll skip it
                    continue

                # Save the item in CustomerItems
                customer_item = CustomerItems(invoice=invoice, cItem=item, amount=amount, invoice_item=True)
                customer_item.save()
                print('Saved item in CustomerItems.')

    def update_inventory_quantity(self, items):
        for item_data in items:
            item_id = item_data.get('item_id')
            amount = item_data.get('amount')

            if item_id and amount and amount >= 1:
                try:
                    item = Inventory.objects.get(id=item_id)
                except Inventory.DoesNotExist:
                    # The item doesn't exist in the Inventory, so we'll skip it
                    continue

                # Update the quantity of the item in Inventory
                item.quantity -= amount
                item.save()
                print('Updated item quantity in Inventory.')

class AddCustomerView(View):
    def post(self, request):
        data = json.loads(request.body)
        customer_name = data.get('customer')

        if not customer_name:
            return JsonResponse({'error': 'Please provide a customer name.'}, status=400)

        customer, created = Customers.objects.get_or_create(cName=customer_name)

        return JsonResponse({'message': 'Customer added successfully.', 'customer_id': customer.id})

class CheckCustomerExistsView(View):
    def get(self, request):
        customer_name = request.GET.get('name')
        
        if not customer_name:
            return JsonResponse({'error': 'Please provide a customer name.'}, status=400)

        try:
            customer = Customers.objects.get(cName=customer_name)
        except Customers.DoesNotExist:
            return JsonResponse({'exists': False})

        return JsonResponse({'exists': True, 'customer_id': customer.id})
    
class PurchaseOrderView(View):
    def get(self, request):
        inventory_data = Inventory.objects.all()
        suppliers = Suppliers.objects.all()
        current_date = datetime.now().strftime("%Y-%m-%d")
        return render(request, 'polls/purchase_order.html', {'inventory_data': inventory_data, 'suppliers': suppliers, 'current_date': current_date})

# Define the function to get item information from the source (placeholder implementation)
def get_item_info_from_source(item_id):
    # Replace this with your actual logic to fetch item information
    try:
        item_info = Inventory.objects.get(id=item_id)
        return {
            'description': item_info.description,
            'quantity': item_info.quantity,
            'purchase_price': item_info.purchase_price,
        }
    except Inventory.DoesNotExist:
        # Item with the given ID does not exist in the source
        return None

class SaveSupplierItemsView(View):
    def post(self, request):
        data = json.loads(request.body)
        supplier_name = data.get('supplier')
        pub_date = data.get('pubDate')
        total_amount = data.get('total')
        items = data.get('items')

        if not supplier_name:
            return JsonResponse({'error': 'Please provide a supplier name.'}, status=400)

        if not pub_date:
            return JsonResponse({'error': 'Please provide an invoice date.'}, status=400)

        if not total_amount:
            return JsonResponse({'error': 'Please provide a total amount.'}, status=400)

        supplier, created = Suppliers.objects.get_or_create(sName=supplier_name)
        pub_date = datetime.strptime(pub_date, "%d-%m-%Y").strftime("%Y-%m-%d")

        invoice = PurchaseOrder(supplier=supplier, pubDate=pub_date, total=total_amount, complete=False)
        invoice.save()

        # First, save all items to SupplierItems
        if items:
            self.save_supplier_items(invoice, items)

        # Then, add missing items to Inventory (if not already present)
        self.add_missing_items_to_inventory(items)

        return JsonResponse({'message': 'Supplier items saved successfully.'})

    def save_supplier_items(self, invoice, items):
        for item_data in items:
            item_id = item_data.get('item_id')
            amount = item_data.get('amount')

            if item_id and amount and amount >= 1:
                try:
                    item = Inventory.objects.get(id=item_id)
                except Inventory.DoesNotExist:
                    # The item doesn't exist in the Inventory, so we'll create it
                    item_info = self.get_item_info_from_source(item_id)
                    if item_info:
                        item = Inventory(
                            item=item_info['description'],
                            description=item_info['description'],
                            quantity=amount,
                            purchasePrice=item_info['purchase_price'],
                            salePrice=0.00
                        )
                        item.save()
                        print('Added new item to Inventory.')

                order_item = True
                # Save the item in SupplierItems
                supplier_item = SupplierItems(
                    purchase=invoice,
                    sItem=item,
                    amount=amount,
                    order_item=order_item
                )
                supplier_item.save()

                # Update the quantity of the item in Inventory
                item.quantity += amount
                item.save()
                print('Saved item in SupplierItems.')
                print('Updated item quantity in Inventory.')

    def item_exists_in_inventory(self, item_id):
        try:
            Inventory.objects.get(id=item_id)
            return True
        except Inventory.DoesNotExist:
            return False

    def add_missing_items_to_inventory(self, items):
        for item_data in items:
            item_id = item_data.get('item_id')
            amount = item_data.get('amount')

            if item_id and amount and amount >= 1:
                if not self.item_exists_in_inventory(item_id):
                    # Dodaj nowy element do Inventory
                    item_info = self.get_item_info_from_source(item_id)
                    if item_info:
                        new_inventory_item = Inventory(
                            item=item_info['description'],
                            description=item_info['description'],
                            quantity=0,
                            purchasePrice=item_info['purchase_price'],
                            salePrice=0.00
                        )
                        new_inventory_item.save()
                        print('Saved new item in Inventory.')
                        print('Item id:', item_id, 'Amount:', amount)

    # Placeholder function to get item information from the source (replace with actual logic)
    def get_item_info_from_source(self, item_id):
        try:
            item_info = Inventory.objects.get(id=item_id)
            return {
                'description': item_info.description,
                'quantity': item_info.quantity,
                'purchase_price': item_info.purchasePrice,
            }
        except Inventory.DoesNotExist:
            # Item with the given ID does not exist in the source
            return None
        
class AddSupplierView(View):
    def post(self, request):
        data = json.loads(request.body)
        supplier_name = data.get('supplier')

        if not supplier_name:
            return JsonResponse({'error': 'Please provide a supplier name.'}, status=400)

        supplier, created = Suppliers.objects.get_or_create(sName=supplier_name)

        return JsonResponse({'message': 'Supplier added successfully.', 'Supplier_id': supplier.id})

class CheckSupplierExistsView(View):
    def get(self, request):
        supplier_name = request.GET.get('name')
        
        if not supplier_name:
            return JsonResponse({'error': 'Please provide a supplier name.'}, status=400)

        try:
            supplier = Suppliers.objects.get(sName=supplier_name)
        except Suppliers.DoesNotExist:
            return JsonResponse({'exists': False})

        return JsonResponse({'exists': True, 'supplier_id': supplier.id})

class AddItemView(View):
    def get(self, request):
        return render(request, 'polls/add_item.html')

    def post(self, request):
        data = request.POST
        item_name = data.get('item_name')
        item_description = data.get('item_description')
        item_quantity = data.get('item_quantity')
        item_purchase_price = data.get('item_purchase_price')

        if not item_name or not item_description or not item_quantity or not item_purchase_price:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            new_item = Inventory(
                item_name=item_name,
                description=item_description,
                quantity=int(item_quantity),
                purchase_price=float(item_purchase_price),
                sale_price=0.00
            )
            new_item.save()

            # Przekierowanie do strony invoice_of_sales.html po zapisaniu
            return JsonResponse({'message': 'Item added successfully.', 'redirect_url': '/invoice_of_sales/'})
        except IntegrityError:
            return JsonResponse({'error': 'Item already exists.'}, status=400)
        
class IncomeAndExpenditureView(View):
    def get(self, request):
        # Fetch all the invoices and purchase orders
        invoices = Invoice.objects.all()
        purchase_orders = PurchaseOrder.objects.all()

        # Fetch the corresponding customer items and supplier items for each invoice and purchase order
        invoice_data = []
        for invoice in invoices:
            total_amount = invoice.iTotal
            items = CustomerItems.objects.filter(invoice=invoice)
            invoice_data.append({'invoice': invoice, 'items': items, 'total_amount': total_amount})

        purchase_order_data = []
        for purchase_order in purchase_orders:
            total_amount = purchase_order.total
            items = SupplierItems.objects.filter(purchase=purchase_order)
            purchase_order_data.append({'purchase_order': purchase_order, 'items': items, 'total_amount': total_amount})

        return render(request, 'polls/income_and_expenditure.html', {'invoice_data': invoice_data, 'purchase_order_data': purchase_order_data})

class MarkInvoiceComplete(APIView):
    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.iComplete = request.data.get("is_completed", False)
            invoice.save()

            if invoice.iComplete:
                customer_items = CustomerItems.objects.filter(invoice=invoice)
                for item in customer_items:
                    if item.invoice_item:
                        inventory_item = item.cItem
                        inventory_item.quantity -= item.amount
                        inventory_item.save()

            return Response(status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class MarkPurchaseOrderComplete(APIView):
    def post(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
            purchase_order.complete = request.data.get("is_completed", False)
            purchase_order.save()

            # Aktualizacja ilości produktów w Inventory na podstawie zamówienia
            if purchase_order.complete:
                supplier_items = SupplierItems.objects.filter(purchase=purchase_order)
                for item in supplier_items:
                    if item.order_item:
                        inventory_item = item.sItem
                        inventory_item.quantity += item.amount
                        inventory_item.save()

            return Response(status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ReportsView(View):
    def get(self, request):
        return render(request, 'polls/reports.html')
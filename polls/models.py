from django.db import models
from django.core.validators import MinValueValidator

class Inventory(models.Model):
    item = models.TextField(max_length=40, null=False, blank=False)
    description = models.TextField(max_length=300, null=False, blank=False)
    quantity = models.IntegerField(default=0, null=False, blank=False, validators=[MinValueValidator(0)])
    purchasePrice = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.01)])
    salePrice = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.01)])

    @classmethod
    def create_new_item(cls, item_name, description, purchase_price):
        new_item = cls(item=item_name, description=description, quantity=0, purchasePrice=purchase_price, salePrice=0.00)
        new_item.save()
        return new_item

    def __str__(self):
        return self.item

class Suppliers(models.Model):
    sName = models.TextField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.sName

class Customers(models.Model):
    cName = models.TextField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.cName

class Invoice(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    iPubDate = models.DateField("date published")
    iTotal = models.FloatField(default=0.00, null=False, validators=[MinValueValidator(0.01)])
    iComplete = models.BooleanField()

    def __str__(self):
        return f"Invoice for {self.customer} - {self.iPubDate}"

class CustomerItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    cItem = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    invoice_item = models.BooleanField(default=False)

    def __str__(self):
        return f"Amount: {self.amount}"

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    pubDate = models.DateField("date published")
    total = models.FloatField(default=0, null=False, validators=[MinValueValidator(0.01)])
    complete = models.BooleanField()

    def __str__(self):
        return f"Purchase Order for {self.supplier} - {self.pubDate}"

class SupplierItems(models.Model):
    purchase = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    sItem = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    order_item = models.BooleanField(default=False)

    def __str__(self):
        return f"Amount: {self.amount}"

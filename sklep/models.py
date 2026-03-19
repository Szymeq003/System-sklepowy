from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa")
    description = models.TextField(blank=True, null=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Kategoria")
    name = models.CharField(max_length=200, verbose_name="Nazwa")
    description = models.TextField(blank=True, null=True, verbose_name="Opis")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena")
    stock = models.IntegerField(default=0, verbose_name="Stan magazynowy")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Oczekujące'),
        ('Completed', 'Zrealizowane'),
        ('Cancelled', 'Anulowane'),
    )
    customer_name = models.CharField(max_length=200, verbose_name="Imię i nazwisko klienta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Całkowita kwota")

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

    def __str__(self):
        return f"Zamówienie #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Zamówienie")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    quantity = models.IntegerField(default=1, verbose_name="Ilość")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena jednostkowa")

    class Meta:
        verbose_name = "Pozycja zamówienia"
        verbose_name_plural = "Pozycje zamówienia"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

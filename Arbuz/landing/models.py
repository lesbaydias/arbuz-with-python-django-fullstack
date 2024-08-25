from django.db import models
from django.contrib.auth.models import User


class ItemTable(models.Model):
    fruits = 'fruits'
    vegetables = 'vegetables'
    drinks = 'drinks'
    CATEGORY = [
        (fruits, 'Fruits'),
        (vegetables, 'Vegetables'),
        (drinks, 'Drinks'),
    ]

    name = models.CharField(max_length=255)
    image_field = models.ImageField(upload_to="images/")
    category = models.CharField(max_length=255,choices=CATEGORY, default=fruits)
    price = models.IntegerField()
    country = models.CharField(max_length=255)

    def _str_(self):
        return f"{self.name}:{self.image_field}:{self.category}:{self.price}:{self.country}"


class UsersTable(models.Model):
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)

    age = models.IntegerField(max_length=30)
    country = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    birthday_date = models.DateTimeField()

    def _str_(self):
        return f"{self.email}:{self.username}:{self.password}:{self.password2}:{self.age}:{self.country}:{self.gender}:{self.birthday_date}"


class BasketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.item.price


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)


class PurchaseItem(models.Model):
    item = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    def subtotal(self):
        return self.quantity * self.item.price


class Payment_Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_cards')
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16, primary_key=True)
    expiration_year = models.IntegerField()
    expiration_month = models.IntegerField()
    balance = models.IntegerField()
    cvv = models.CharField(max_length=4)

    def str(self):
        return f'{self.cardholder_name}\'s Card ({self.card_number[-4:]})'

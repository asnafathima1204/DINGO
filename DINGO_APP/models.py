from django.db import models
from django.contrib.auth.models import User

size_choice ={
    1: [("S", "Small"), ("M", "Medium"), ("L", "Large")],
    2: [("Q", "Quarter"), ("H", "Half"), ("F", "Full")],
    3: [("R", "Regular"), ("L", "Large")],

}

category_choice = [
    (1, "Category1(S,M,L)"),
    (2, "Category2(Quarter,Half,Full)"),
    (3, "Category3(regular,large)")
]


address_choice =(
    (1,"permanent"),
    (2,"temporary")
)


# Create your models here.
class Item(models.Model):
    item_id = models.CharField(max_length=10,null=True,blank=True,unique=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    category_type = models.IntegerField(choices=category_choice, null=True, blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_size_choices(self):
        # Fetch sizes based on the category_type (integer)
        return size_choice.get(self.category_type, [])


from decimal import Decimal
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    total_price=models.DecimalField(max_length=10,decimal_places=2,null=True,blank=True)

    def total_price(self):
        base_price = self.item.price
        size_factor = self.get_size_price_factor()
        return base_price * size_factor * self.quantity

    def get_size_display(self):
        size_choices = self.item.get_size_choices()
        return dict(size_choices).get(self.size, "Unknown")

    def get_size_price_factor(self):
        size_mapping = {
            "S": Decimal("1.0"),  # Small → Half price
            "M": Decimal("1.5"),  # Medium → Normal price
            "R": Decimal("1.0"),  # Regular → Normal price
            "L": Decimal("2.0"),  # Large → Double price
            "F": Decimal("2.0"),  # Full → Double price
            "H": Decimal("1.5"),
            "Q": Decimal("1.0"),  # Quarter → Half price
        }
        # Return price factor, default to normal price if size not found
        return size_mapping.get(self.size, Decimal("1.0"))

    def shipping_charge(self):
        total_price = self.total_price()
        return Decimal("50.00") if total_price > Decimal("500.00") else Decimal("10.00") 

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=6,null=True,blank=True)
    address_type = models.IntegerField(choices=address_choice,null=True,blank=True)


    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    tax = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    shipping = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    

    def __str__(self):
        return self.order_id
    
    def shipping_charge(self):
        total_price = self.total or Decimal("0.00")
        return Decimal("50.00") if total_price > Decimal("500.00") else Decimal("10.00")

    def add_tax(self):
        total_price = self.total or Decimal("0.00")
        return Decimal("21.99") if total_price > Decimal("500.00") else Decimal("0.00")
    
    
           
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    size_oriented_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)


    def get_size_price_factor(self):
        size_mapping = {
            "S": Decimal("1.0"),  # Small → Half price
            "M": Decimal("1.5"),  # Medium → Normal price
            "R": Decimal("1.0"),  # Regular → Normal price
            "L": Decimal("2.0"),  # Large → Double price
            "F": Decimal("2.0"),  # Full → Double price
            "H": Decimal("1.5"),
            "Q": Decimal("1.0"),  # Quarter → Half price
        }
        # Return price factor, default to normal price if size not found
        return size_mapping.get(self.size, Decimal("1.0"))

    def __str__(self):
        return self.id






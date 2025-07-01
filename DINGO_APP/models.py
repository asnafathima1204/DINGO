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

status_choice = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
)

reservation_choice = (
        ('pending', 'Pending'),
        ('confirmed', 'confirmed'),
        ('cancelled', 'Cancelled'),
)

time_choice = (
    ('08:00 AM to 10:00 AM', '08:00 AM to 10:00 AM'),
    ('10:00 AM to 12:00 PM', '10:00 AM to 12:00 PM'),
    ('12:00 PM to 02:00 PM', '12:00 PM to 02:00 PM'),
    ('02:00 PM to 04:00 PM', '02:00 PM to 04:00 PM'),
    ('04:00 PM to 06:00 PM', '04:00 PM to 06:00 PM'),
    ('06:00 PM to 08:00 PM', '06:00 PM to 08:00 PM'),
    ('08:00 PM to 10:00 PM', '08:00 PM to 10:00 PM'),
    ('10:00 PM to 12:00 AM', '10:00 PM to 12:00 AM'),
)


# Create your models here.
class Item(models.Model):
    item_id = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    category_type = models.IntegerField(choices=category_choice,default=13)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    exclusive_item = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name) if self.name else "Unnamed Item" 

    def get_size_choices(self):
        # Fetch sizes based on the category_type (integer)
        return size_choice.get(self.category_type, [])


from decimal import Decimal
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def calculate_total_price(self):
        base_price = self.item.price
        print("Base price",base_price)
        size_factor = self.get_size_price_factor()
        return base_price * size_factor * self.quantity

    def get_size_display(self):
        size_choices = self.item.get_size_choices()
        return dict(size_choices).get(self.size, "Unknown")

    def get_size_price_factor(self):
        size_mapping = {
            "S": Decimal("0.25"),
            "M": Decimal("0.5"),
            "R": Decimal("0.5"), 
            "L": Decimal("1.0"), 
            "F": Decimal("1.0"), 
            "H": Decimal("0.5"),
            "Q": Decimal("0.25"), 
        }
        # Return price factor, default to normal price if size not found
        return size_mapping.get(self.size, Decimal("1.0"))
    

    def shipping_charge(self):
        total_price = self.calculate_total_price()
        return Decimal("50.00") if total_price > Decimal("500.00") else Decimal("10.00") 
    
    def __str__(self):
        return self.user.first_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=6,null=True,blank=True)
    address_type = models.IntegerField(choices=address_choice,null=True,blank=True)


    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    ordered_date = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    shipping = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status = models.CharField(max_length=100,choices=status_choice,default='pending')
    

    def shipping_charge(self):
        total_price = self.total or Decimal("0.00")
        return Decimal("50.00") if total_price > Decimal("500.00") else Decimal("10.00")

    def add_tax(self):
        total_price = self.total or Decimal("0.00")
        return Decimal("21.99") if total_price > Decimal("500.00") else Decimal("0.00")
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}" 
           
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    size_oriented_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)


    def get_size_price_factor(self):
        size_mapping = {
            "S": Decimal("0.25"),
            "M": Decimal("0.5"),
            "R": Decimal("0.5"), 
            "L": Decimal("1.0"), 
            "F": Decimal("1.0"), 
            "H": Decimal("0.5"),
            "Q": Decimal("0.25"), 
        }
        # Return price factor, default to normal price if size not found
        return size_mapping.get(self.size, Decimal("1.0"))

    def __str__(self):
        return self.item.name
class Chef(models.Model):
    chef_id=models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    experience = models.IntegerField()  # in years
    image = models.ImageField(upload_to='chefs/')  # for profile picture
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    guest = models.IntegerField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.CharField(choices=time_choice,max_length=100)
    note = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=100,choices=reservation_choice,default='pending')

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"
    
class Contact(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    phone = models.CharField(max_length=155)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.name} - {self.email}"


from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import time_choice  # Import the choices from models
from datetime import date, datetime
from django.db.models import Q


# Create your views here.
def not_found(request,exception):
    return render(request,'404.html',status=404)

def index(request):
    exclusive_item = Item.objects.filter(exclusive_item=True)
    chefs=Chef.objects.all()
    selected_category = request.GET.get('category', 'All')  # Default to 'All' if no category is selected
    all_categories = Item.objects.values_list('category', flat=True).distinct().order_by('category')

    for i in all_categories:
        print(i)
    food_items = Item.objects.all()
    half_length = len(food_items) // 2
    if (len(food_items)) % 2 == 0:
        half_length = half_length
        print(half_length)
    else:
        half_length += 1
        print(half_length)
    # for i in food_items:
    #     print(i.name)
    # using dict format : each data items pass as dictionaries
    # return render(request,'food_menu.html',{'food_items':food_items})
    # using locals() : automatically pass all variables into html
    time_choice = Reservation._meta.get_field('time').choices

    return render(request, 'index.html',locals())

def items_filter(request,category):
    selected_category = request.GET.get('category', category)  # Default to 'All' if no category is selected
    selected_items = Item.objects.filter(category=category)  # Get food items from the database
    all_categories = Item.objects.values_list('category', flat=True).distinct().order_by('category')

    half_length = len(selected_items) // 2
    if (len(selected_items)) % 2 == 0:
        half_length = half_length
        print(half_length)
    else:
        half_length += 1
        print(half_length)
    return render(request, 'index.html', locals())


def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        created_at = request.POST.get("created_at")

        contacts=Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            created_at=created_at
        )
        
    return render(request,'contact.html')


def chefs(request):
    chefs=Chef.objects.all()
    return render(request,'chefs.html',locals())


def food_menu(request):
    search = request.GET.get('search','')
    if search:
        food_items=Item.objects.filter(Q(name__icontains=search)|Q(category__icontains=search))
    else:
        food_items = Item.objects.all()
    # method to retrieve data
    # # select * from
    # food_items = Item.objects.all()
    # # select * from ... where <condition>
    # food_items = Item.objects.filter(item_id='DG011')
    # # get()
    # food_items = Item.objects.get(item_id='DG011')
    # fetching all data in item table
    selected_category = request.GET.get('category', 'All')  # Default to 'All' if no category is selected
    all_categories = Item.objects.values_list('category', flat=True).distinct().order_by('category')

    for i in all_categories:
        print(i)
    
    half_length = len(food_items) // 2
    if (len(food_items)) % 2 == 0:
        half_length = half_length
        print(half_length)
    else:
        half_length += 1
        print(half_length)
    # for i in food_items:
    #     print(i.name)
    # using dict format : each data items pass as dictionaries
    # return render(request,'food_menu.html',{'food_items':food_items})
    # using locals() : automatically pass all variables into html
    return render(request, 'food_menu.html', locals())


def item_filter(request,category):
    selected_category = request.GET.get('category', category)  # Default to 'All' if no category is selected
    selected_items = Item.objects.filter(category=category)  # Get food items from the database
    all_categories = Item.objects.values_list('category', flat=True).distinct().order_by('category')

    half_length = len(selected_items) // 2
    if (len(selected_items)) % 2 == 0:
        half_length = half_length
        print(half_length)
    else:
        half_length += 1
        print(half_length)
    return render(request, 'food_menu.html', locals())


def exclusive_item(request):
    # Filter exclusive items
    exclusive_item = Item.objects.filter(exclusive_item=True)
    return render(request, 'index.html', {'exclusive_item': exclusive_item})

def view_item(request,id):
    exclusive_item = Item.objects.get(id=id)
    return render(request,'view_item.html',locals())



# ---------admin module----------------------------
from django.db.models import Sum

@login_required
def dashboard(request):
    items=Item.objects.all().count()
    users=User.objects.all().count()
    c_orders=Order.objects.all().count()
    c_reservations=Reservation.objects.all().count()
    
    orders_year = Order.objects.filter(
        Q(ordered_date__year=date.today().year) & Q(status='delivered')
       
        ).aggregate(total_sum=Sum('total'))['total_sum'] or 0.00
    
    orders_month = Order.objects.filter(
        Q(ordered_date__month=date.today().month) & Q(status='delivered')
        ).aggregate(total_sum=Sum('total'))['total_sum'] or 0.00
    earn_year=date.today().year
    earn_month=date.today().strftime('%B')

    print(orders_year)
    orders = Order.objects.filter(
        ordered_date__date=date.today(),
        status__in=['shipped', 'delivered']
    )
    reservations=Reservation.objects.filter(
        Q(date=date.today()) & Q(status="confirmed")
        )


    print(orders)
    print(reservations)
    return render(request,'dashboard.html',locals())


@login_required
def admin_fooditems(request):
    # food_items = Item.objects.all()
    food_items = Item.objects.all().order_by('item_id')  
    context = {
        'food_items': food_items
    }
    return render(request,'admin_fooditems.html',context)

@login_required
def admin_additems(request):
    if request.method=="POST":
        item_id = request.POST.get("item_id")
        name = request.POST.get("name").title()
        category = request.POST.get("category").title()
        category_type = request.POST.get("category_type")
        price = request.POST.get("price").title()
        description = request.POST.get("description")
        image = request.FILES.get("image")
        exclusive_item = request.POST.get('exclusive_item')

        item_exists = Item.objects.filter(item_id=item_id).exists()

        if item_exists:
            messages.warning(request, "Item already exists..!")
            return redirect(admin_fooditems)
        else:

            data = Item.objects.create(item_id=item_id,
                                      name=name,
                                      category=category,
                                      category_type=category_type,
                                      price=price,
                                      description=description,
                                      image=image,
                                      exclusive_item=exclusive_item
                                      )

            data.save()
            messages.success(request, "Item added")
            return redirect(admin_fooditems)

    else:
        messages.warning(request, "Something went wrong")
        return redirect(admin_fooditems)



@login_required
def admin_viewitems(request,id):
    food_item = Item.objects.filter(id=id)
    return render(request,'admin_viewitems.html',{'food_item': food_item})


@login_required
def admin_edititems(request, id):
    instance = get_object_or_404(Item, id=id)  # Fetch the existing item

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        name = request.POST.get("name").title()
        category = request.POST.get("category").title()
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        exclusive_item = request.POST.get('exclusive_item')

        # Check if an item with the same item_id already exists (excluding current item)
        existing_item = Item.objects.filter(item_id=item_id).exclude(id=id).first()
        if existing_item:
            messages.warning(request, "Item with this ID already exists..!")
            return redirect(admin_fooditems)

        # Update item fields
        instance.item_id = item_id
        instance.name = name
        instance.category = category
        instance.price = price
        instance.description = description
        instance.exclusive_item = exclusive_item


        if image:
            print("Image updated!")
            instance.image = image  # Assign new image

        instance.save()  # Save changes

        messages.success(request, "Item Updated Successfully!")
        return redirect(admin_viewitems,id)

    messages.warning(request, "Something went wrong")
    return redirect(admin_fooditems)


@login_required
def admin_deleteitems(request,id):
    if request.method == "POST":
            data = Item.objects.filter(id=id)
            data.delete()
            messages.success(request, "Item deleted successfully!")
            return redirect(admin_fooditems)


@login_required
def admin_order(request):
    order=Order.objects.all()
    return render(request,'admin_order.html',locals())

@login_required
def admin_vieworder(request,id):
    order=Order.objects.get(id=id)
    order_items=OrderItem.objects.filter(order_id=order.id)
    for i in order_items:
      i.size_oriented_price=i.item.price*i.get_size_price_factor()
      i.total_price = i.size_oriented_price * i.quantity
    subtotal = sum(i.total_price for i in order_items)
    return render(request,'admin_vieworder.html',locals())


@login_required
def admin_user(request):
    users = User.objects.filter(is_superuser = False)
    return render(request,'admin_user.html',{'users':users})

def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Toggle the is_active status
    user.is_active = not user.is_active  
    user.save()

    return redirect('admin_user') 

@login_required
def admin_chef(request):
    chefs=Chef.objects.all()
    return render(request,'admin_chef.html',locals())

@login_required
def admin_viewchef(request,id):
    chef=Chef.objects.get(id=id)
    return render(request,'admin_viewchef.html',locals())


@login_required
def admin_addchef(request):
    if request.method=="POST":
        chef_id = request.POST.get("chef_id")
        name = request.POST.get("name")
        specialty = request.POST.get("specialty")
        experience = request.POST.get("experience")
        image = request.FILES.get("image")
        bio = request.POST.get("bio")

        chef_exists = Chef.objects.filter(chef_id=chef_id).exists()

        if chef_exists:
            messages.warning(request, "Chef already exists..!")
            return redirect(admin_chef)
        else:

            chefs = Chef.objects.create(chef_id=chef_id,
                                        name=name,
                                        specialty=specialty,
                                        experience=experience,
                                        image=image,
                                        bio=bio
                                       )

            chefs.save()
            messages.success(request, "Chef added")
            return redirect(admin_chef)

    else:
        messages.warning(request, "Something went wrong")
        return redirect(admin_chef)

@login_required
def admin_editchef(request, id):
    chef = Chef.objects.get(id=id)  # Get the existing chef instance
    print(chef.id)

    if request.method == 'POST':
        chef.chef_id = request.POST.get('chef_id')
        chef.name = request.POST.get('name')
        chef.specialty = request.POST.get('specialty')
        chef.experience = request.POST.get('experience')
        chef.bio = request.POST.get('bio')

        # Only update image if a new image is uploaded
        new_image = request.FILES.get('image')
        if new_image:  
            chef.image = new_image  

        chef.save()  # Save the updated details
        return redirect('admin_viewchef', chef.id)

    return redirect('admin_chef', chef.id)

@login_required
def admin_deletechef(request,id):
    if request.method == "POST":
            chef = Chef.objects.filter(id=id)
            chef.delete()
            messages.success(request, "Chef deleted successfully!")
            return redirect(admin_chef)

@login_required
def admin_reservation(request):
    reservation = Reservation.objects.all().order_by('date')
    if request.method == "POST":
        # Handle form submission
        reservation_id = request.POST.get('reservation_id')
        new_status = request.POST.get('status')
        
        try:
            reserve = Reservation.objects.get(id=reservation_id)
            reserve.status = new_status
            reserve.save()
            print(reserve.status)
            messages.success(request, f"Reservation {reservation_id} status updated to {new_status}.")
        except Order.DoesNotExist:
            messages.error(request, "Reservation not found.")
            return redirect('dashboard')
    return render(request,"admin_reservation.html",locals())

def admin_contact(request):
    contacts = Contact.objects.all()
    print(contacts)
    return render(request,'admin_contact.html',{'contacts':contacts})


# ------user module -------------------

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    item_count = cart_items.count()
    item_sizes = {}
    total_cart_price = sum(item.calculate_total_price() for item in cart_items)  # Recalculate total price

    for cart_item in cart_items:
        item_category = cart_item.item.category
        item_sizes[cart_item.item.id] = size_choice.get(item_category, [])
    # Calculate shipping charge
    shipping_charge = Decimal("50.00") if total_cart_price > Decimal("500.00") else Decimal("10.00")

    # Calculate tax (if needed, or set to 0)
    tax_amount = Decimal("21.99") if total_cart_price > Decimal("500.00") else Decimal("00.00")  # Or calculate dynamically

    # Calculate the final total
    grand_total = total_cart_price + shipping_charge + tax_amount


    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'item_count': item_count,
        'total_cart_price': total_cart_price,
        'shipping_charge': shipping_charge,
        'tax_amount': tax_amount,
        'grand_total': grand_total,

    })


@login_required
def add_cart(request, id):
    food_items = Item.objects.get(id=id)
    user = request.user 
    size = 'DefaultSize'
    if food_items.category_type == 1:
        size = 'L'
    elif food_items.category_type == 2:
        size = 'F'
    elif food_items.category_type == 3:
        size = 'L'

        
    cart_item, created = Cart.objects.get_or_create(
        item=food_items,
        user=user,
        defaults={'quantity': 1, 'size': size}
    )
    cart_item.shipping_charge()
    cart_item.total_price = cart_item.calculate_total_price()
    cart_item.save()
    
    if not created:
        cart_item.quantity += 1 
        cart_item.save()
        messages.success(request, "Item quantity updated in cart!")
    else:
        messages.success(request, "Item successfully added to cart!")
        

    return redirect(food_menu)


@login_required
#updating quantity
def increment_quantity(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.quantity += 1
    cart_item.total_price=cart_item.calculate_total_price()
    cart_item.save()
    return redirect(cart)  # Redirect to your cart page or another view


@login_required
def decrement_quantity(request, id):
    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price=cart_item.calculate_total_price()
        cart_item.save()
    else:
        messages.warning(request, "Quantity cannot be less than 1!")

    return redirect(cart)


def update_size(request, id):
    if request.method == 'POST':
        new_size = request.POST.get('size')
        cart_item = get_object_or_404(Cart, id=id, user=request.user)
        cart_item.size = new_size
        cart_item.total_price = cart_item.calculate_total_price()
        cart_item.save()
    return redirect('cart')


@login_required
def remove_cart(request,id):
    if request.method == "POST":
            data = Cart.objects.get(id=id)
            data.delete()
            messages.success(request, "Cart Item Removed successfully!")
            return redirect(cart)

    else:
        messages.success(request, "Something went wrong")
        return redirect(cart)

@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user_id=request.user)
    details = Address.objects.filter(user_id=request.user)
    item_count = cart_items.count()
    item_sizes = {}
    total_cart_price = sum(item.calculate_total_price() for item in cart_items)  # Recalculate total price

    for cart_item in cart_items:
        item_category = cart_item.item.category
        item_sizes[cart_item.item.id] = size_choice.get(item_category, [])
    # Calculate shipping charge
    shipping_charge = Decimal("50.00") if total_cart_price > Decimal("500.00") else Decimal("10.00")

    # Calculate tax (if needed, or set to 0)
    tax_amount = Decimal("21.99") if total_cart_price > Decimal("500.00") else Decimal(
        "00.00")  # Or calculate dynamically

    # Calculate the final total
    grand_total = total_cart_price + shipping_charge + tax_amount

    return render(request, 'user_checkout.html', {
        'cart_items': cart_items,
        'item_count': item_count,
        'total_cart_price': total_cart_price,
        'shipping_charge': shipping_charge,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'details':details

    })

@login_required
def confirmation_page(request):
    order = Order.objects.last()  # Get the most recent order
    return render(request, 'order_confirmation.html', {'order': order})
    

@login_required
def order_confirmation(request):
    if request.method == 'POST':
        address=request.POST.get('address')
        total_quantity=0
        total_cart_price=0
        if address:
            user=request.user
            print(address)
            cart_item=Cart.objects.filter(user=user)
            if not cart_item.exists():
                messages.error(request, "Your cart is empty!")
            order=Order.objects.create(
                    user=user,
                    ordered_date=timezone.now(),
                    address=address
                )

            for i in cart_item:
                print(i.quantity)
                # print(i.id)
                OrderItem.objects.create(order=order,item=i.item, quantity=i.quantity, size=i.size)
                # total_price=total_price+(i.item.price*i.quantity)
                # print(total_price)
                total_quantity=total_quantity+i.quantity
            
            total_cart_price = sum(item.calculate_total_price() for item in cart_item)  # Recalculate total price
            order.total=total_cart_price
            order.quantity=total_quantity
            order.total += order.shipping_charge()
            order.total += order.add_tax()
            order.shipping=order.shipping_charge()
            order.tax=order.add_tax()
            order.save()
            cart_item.delete()
            return redirect('confirmation_page')
        
        else:
            messages.error(request,'Please add address to your profile')
    return redirect('checkout_view')


@login_required
def buy_now(request,id):
    food_items = Item.objects.get(id=id)
    user = request.user

    size = 'DefaultSize'
    if food_items.category_type == 1:
        size = 'L'
    elif food_items.category_type == 2:
        size = 'F'
    elif food_items.category_type == 3:
        size = 'L'

    cart_item, created = Cart.objects.get_or_create(
        item=food_items,
        user=user,
        defaults={'quantity': 1, 'size': size}
    )
    cart_item.shipping_charge()
    cart_item.total_price = cart_item.calculate_total_price()
    cart_item.save()
    cart_item.shipping_charge()
    cart_item.total_price = cart_item.calculate_total_price()
    cart_item.save()

    return redirect(cart)




@login_required
def user_home(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        guest=request.POST.get('guest')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        time=request.POST.get('time')
        note=request.POST.get('note')
        print("Date",date)
        user=request.user
        if date:
            date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")  # Convert MM/DD/YYYY to YYYY-MM-DD
        reservation = Reservation.objects.create(
                name=name,
                email=email,
                guest=guest,
                phone=phone,
                date=date,
                time=time,
                note=note,
                user=user
            )

        reservation.save()
        print(reservation)
        messages.success(request,"Reservation successful!")
        return redirect('user_home')
    

        

    exclusive_item = Item.objects.filter(exclusive_item=True)
    chefs=Chef.objects.all()
    selected_category = request.GET.get('category', 'All')  # Default to 'All' if no category is selected
    all_categories = Item.objects.values_list('category', flat=True).distinct().order_by('category')

    for i in all_categories:
        print(i)
    food_items = Item.objects.all()
    half_length = len(food_items) // 2
    if (len(food_items)) % 2 == 0:
        half_length = half_length
        print(half_length)
    else:
        half_length += 1
        print(half_length)


    # for i in food_items:
    #     print(i.name)
    # using dict format : each data items pass as dictionaries
    # return render(request,'food_menu.html',{'food_items':food_items})
    # using locals() : automatically pass all variables into html
    time_choice = Reservation._meta.get_field('time').choices

    return render(request, 'user_home.html', locals())

@login_required
def user_invoice(request,id):
    order=Order.objects.get(id=id)
    order_item=OrderItem.objects.filter(order_id=order.id)
    for i in order_item:
      i.size_oriented_price=i.item.price*i.get_size_price_factor()
      i.total_price = i.size_oriented_price * i.quantity
    superuser = User.objects.filter(is_superuser=True).first()
    subtotal = sum(i.total_price for i in order_item)

    return render(request,'user_invoice.html',locals())

@login_required
def user_order(request):
    orders=Order.objects.filter(user=request.user)
    print(orders)
    return render(request,'user_order.html',locals())


def cancel_order(request,id):
    order=Order.objects.get(id=id)
    order.status="cancelled"
    order.save()
    return redirect(user_order)

def admin_order_list(request):
     # Display orders with status
    orders = Order.objects.all().order_by('ordered_date')
    if request.method == "POST":
        # Handle form submission
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            messages.success(request, f"Order {order_id} status updated to {new_status}.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        
        return redirect('admin_order_list')

   
    
    return render(request, 'admin_order.html', {'order': orders})

@login_required
def user_reservation(request):
    reservation=Reservation.objects.filter(user=request.user)
    return render(request,'user_reservation.html',locals())

def cancel_reservation(request,id):
    reservation=Reservation.objects.get(id=id)
    reservation.status="cancelled"
    reservation.save()
    return redirect(user_reservation)

@login_required
def user_profile(request):
    user_details=request.user
    order=Order.objects.filter(user=user_details).order_by('-ordered_date').first()
    order_item=OrderItem.objects.filter(order=order)
    for i in order_item:
      i.size_oriented_price=i.item.price*i.get_size_price_factor()
    #   i.total_price = i.size_oriented_price * i.quantity
      i.price_per_items=i.item.price* i.quantity*i.get_size_price_factor()
    try:
        user_address = Address.objects.filter(user=request.user.id)
    except:
        user_address = None  # Assign None to avoid reference errors in the template
        messages.error(request, "Something Wrong")

    return render(request, 'user_profile.html', locals())




@login_required
def save_address(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        street = request.POST.get("street").title()
        city = request.POST.get("city").title()
        district = request.POST.get("district").title()
        zipcode = request.POST.get("zipcode")
        address_type = request.POST.get("address_type")

        print(request.POST)  # Debugging: See the received data

        user = User.objects.get(id=request.user.id)
        data = Address.objects.create(phone_number=phone_number,
                                      district=district,
                                      street=street,
                                      city=city,
                                      user = user,
                                      address_type=address_type,
                                      zipcode=zipcode
                                            )
        data.save()
        messages.success(request,"Address added")
        return redirect(user_profile)
    else:
        messages.warning(request, "Invalid")
        return redirect(user_profile)

    # If GET request, fetch the existing address data
    # user_address = Address.objects.all()

    return render(request, "user_profile.html")

@login_required
def edit_address(request,id):
    address=Address.objects.get(id=id)
    return render(request,'edit_address.html',locals())


@login_required
def update_address(request,id):
    address = Address.objects.get(id=id)
    if request.method == "POST":
        address.phone_number = request.POST.get("phone_number")
        address.street = request.POST.get("street").title()
        address.city = request.POST.get("city").title()
        address.district = request.POST.get("district").title()
        address.zipcode = request.POST.get("zipcode")
        address.address_type = request.POST.get("address_type")
        address.save()

        
        # user = User.objects.get(id=request.user.id)
        # mydata = Address.objects.filter(user=user).update(phone_number=address.phone_number,
        #                               district=address.district,
        #                               street=address.street,
        #                               city=address.city,
        #                               address_type=address.address_type,
        #                               zipcode=address.zipcode)
        # mydata.save()
        messages.success(request,"Address updated!")
        return redirect(user_profile)
        # except:
        #     messages.error(request,"Something wrong")
        #     return redirect('edit_address',id)
    else:
        messages.warning(request, "Invalid")
        return redirect(user_profile)


@login_required
def delete_address(request,id):
    if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            data = Address.objects.filter(user=user, id=id)
            data.delete()
            messages.success(request, "Address deleted successfully!")
            return redirect(user_profile)



def user_registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            User.objects.get(username=email)
            messages.error(request, "Username already exists. Please login..!")
            return redirect(index)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            first_name=fname,
                                            last_name=lname,
                                            email=email,
                                            is_superuser=0,
                                            is_staff=0
                                            )
            user.set_password(password)
            user.save()
            messages.success(request, "Account created successfully! Please login with your credential")
            return redirect(index)
    else:
        messages.warning(request,"Invalid credentials")
        return redirect(index)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email,password=password)
        
        if user is not None:
            
            if user.is_superuser:
                    # admin module
                login(request,user)
                return redirect(dashboard)
                
            else:
                #user module
                login(request,user)
                return redirect(user_home)
        else:
            if not User.objects.filter(username=email).exists():
                messages.warning(request,"You are not registered yet. Please register..!")
                return redirect(index)
            else:
                messages.warning(request,"Invalid Password!!")
                return redirect(index)
    else:
        messages.error(request,"Invalid credentials")
        return redirect(index)

@login_required
def user_logout(request):
    logout(request)
    return redirect(index)






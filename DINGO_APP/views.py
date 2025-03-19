from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone



# Create your views here.

def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')


def chefs(request):
    return render(request,'chefs.html')


def elements(request):
    return render(request,'elements.html')


def food_menu(request):

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


def blog(request):
    return render(request,'blog.html')


def single_blog(request):
    return render(request,'single-blog.html')



# ---------admin module----------------------------

@login_required
def dashboard(request):
    return render(request,'dashboard.html')


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
                                      image=image
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


        if image:
            print("Image updated!")
            instance.image = image  # Assign new image

        instance.save()  # Save changes

        messages.success(request, "Item Updated Successfully!")
        return redirect(admin_fooditems)

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
    users = User.objects.all()
    return render(request,'admin_user.html',{'users':users})

def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Toggle the is_active status
    user.is_active = not user.is_active  
    user.save()

    return redirect('admin_user') 


# ------user module -------------------

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    item_count = cart_items.count()

    item_sizes = {}
    total_cart_price = sum(item.total_price() for item in cart_items)  # Recalculate total price

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
    # Check if the item already exists in the cart
    cart_item, created = Cart.objects.get_or_create(
        item=food_items,
        user=user,
        defaults={'quantity': 1,'size':1}  # Initial values for new item
    )
    cart_item.shipping_charge()
    
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
    cart_item.save()
    return redirect(cart)  # Redirect to your cart page or another view


@login_required
def decrement_quantity(request, id):
    cart_item = Cart.objects.get(id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.warning(request, "Quantity cannot be less than 1!")

    return redirect(cart)


@login_required
def update_size(request, id):
    size = request.GET.get('size')
    cart_data = Cart.objects.get(id=id)
    cart_data.size = size
    cart_data.save()
    print(size)
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
    total_cart_price = sum(item.total_price() for item in cart_items)  # Recalculate total price

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
            
            total_cart_price = sum(item.total_price() for item in cart_item)  # Recalculate total price
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

    # Check if the item already exists in the cart
    cart_item, created = Cart.objects.get_or_create(
        item=food_items,
        user=user,
        defaults={'quantity': 1, 'size': 1}  # Initial values for new item
    )
    cart_item.shipping_charge()
    cart_item.save()

    return redirect(cart)




@login_required
def user_home(request):
    return render(request,'user_home.html')

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
    return render(request,'user_order.html')


@login_required
def user_profile(request):
    user_details = User.objects.filter(id=request.user.id)
    # for i in user_details:
    #     print(i.first_name)
    #     print(i.last_name)
    #     print(i.email)
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
            if user.is_staff == 1:
                if user.is_superuser == 1:
                    # admin module
                    login(request,user)
                    return redirect(dashboard)
                else:
                    #staff module
                    pass
            else:
                #user module
                login(request,user)
                return redirect(user_home)
        else:
            messages.warning(request,"You are not registered yet. Please register..!")
            return redirect(index)
    else:
        messages.error(request,"Invalid credentials")
        return redirect(index)

@login_required
def user_logout(request):
    logout(request)
    return redirect(index)






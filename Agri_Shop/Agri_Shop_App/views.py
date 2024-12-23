from .models import HighQualitySeed, OrganicFertilizer, SafePesticide, FarmEquipment, AnimalFeed, AgriElectronicsTool,Cart,Contact_Info,Subscribe
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import RegistrationForm ,UserUpdationForm,get_product_form
from django.http import HttpResponse,request
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count,Q
from django.contrib import messages
from django.conf import settings
from.models import registration
from decimal import Decimal
import qrcode
import base64
import io

Seed = HighQualitySeed.objects.all()
fertilizers = OrganicFertilizer.objects.all()
pesticides = SafePesticide.objects.all()
equipment = FarmEquipment.objects.all()
feed = AnimalFeed.objects.all()
electronics_tools = AgriElectronicsTool.objects.all()

MODEL_MAPPING = {
    'high_quality_seed': HighQualitySeed,
    'organic_fertilizer': OrganicFertilizer,
    'safe_pesticide': SafePesticide,
    'farm_equipment': FarmEquipment,
    'animal_feed': AnimalFeed,
    'agri_electronics_tool': AgriElectronicsTool,
}

def index(request):
    return redirect('main/')

def main(request):
    return render(request,"main.html")

def products(request):
    context = {
        'seeds': Seed,
        'fertilizers': fertilizers,
        'pesticides': pesticides,
        'equipment': equipment,
        'feed': feed,
        'electronics_tools': electronics_tools,
    }
    return render(request, 'products.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f'Contact Form Submission from {name}'
        body = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            ['myemail@gmail.com'], 
            fail_silently=False,
        )
        return redirect('/main/') 
    return render(request, 'contact.html')
    
def about(request):
    return render(request,"about.html")

def subscribe_all(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            if not Subscribe.objects.filter(email=email).exists():
                sub = Subscribe(email=email)
                sub.save()  
        except Exception as e:
            print(e)
    return redirect("/main/")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.username == "Admin_main":
                return redirect('/Admin_page/')   
            else:
                request.session['user_id'] = user.id
                return redirect('/main_user/')
        else:
            messages.error(request, 'Invalid email or password') 
            print("Invalid Details")
    return render(request, 'sign_in_out/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/login/')
        else:
            print('Invalid email or password')
            print("-------------------Error--------------------------")
    else:
        form = RegistrationForm()
    return render(request, 'sign_in_out/register.html', {'form': form})

@login_required
def main_user(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    return render(request, "User/main_user.html" , {'user_id':user_id})

@login_required
def profile(request, user_id):
    users = get_object_or_404(User, id=user_id)
    contact = get_object_or_404(Contact_Info, user_id=user_id)
    return render(request, "User/profile.html", {'user':users, 'contact':contact})


@login_required
def edit_pf(request):
    contact_info = Contact_Info.objects.filter(user=request.user).first()
    if request.method=='POST':
        fname= request.POST.get('first_name')
        lname= request.POST.get('last_name')
        email= request.POST.get('email')
        contact_number = request.POST.get('contact') 
        try:
            user = request.user 
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            if contact_info:
                contact_info.contact = contact_number
                contact_info.save()
            else:
                Contact_Info.objects.create(user=user, contact=contact_number)
            return redirect('/main_user/')
        except Exception as e:
            print(e)
    return render(request, 'User/edit_pf.html', {'user': request.user, 'contact_info': contact_info})
 
@login_required
def contact_user(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f'Contact Form Submission from {name}'
        body = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            ['myemail@gmail.com'], 
            fail_silently=False,
        )
        return redirect('/main_user/') 
    return render(request, 'User/contact_user.html', {"user":user})

@login_required
def about_user(request):
    user = request.user
    return render(request, 'User/about_user.html', {"user":user})

@login_required
def products_user(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    context = {
        'seeds': Seed,
        'fertilizers': fertilizers,
        'pesticides': pesticides,
        'equipment': equipment,
        'feed': feed,
        'electronics_tools': electronics_tools,
        'user_id':user_id    }
    return render(request, 'User/product_user.html', context)

@login_required
def moreinfo(request,product_type, product_id):
    if product_type == 'High-Quality Seeds':
        product = get_object_or_404(HighQualitySeed, id=product_id)
    elif product_type == 'Organic Fertilizers':
        product = get_object_or_404(OrganicFertilizer, id=product_id)
    elif product_type == 'Safe Pesticides':
        product = get_object_or_404(SafePesticide, id=product_id)
    elif product_type == 'Farm Equipment':
        product = get_object_or_404(FarmEquipment, id=product_id)
    elif product_type == 'Animal Feed':
        product = get_object_or_404(AnimalFeed, id=product_id)
    elif product_type == 'Agri Electronics & Tools':
        product = get_object_or_404(AgriElectronicsTool, id=product_id)
    else:
        messages.error(request, 'Invalid product type')
        return redirect('/products_user/')
    return render(request, "User/more_info.html", {"product": product})

@login_required
def add_to_cart(request, product_type, product_id):
    if product_type == 'High-Quality Seeds':
        product = get_object_or_404(HighQualitySeed, id=product_id)
    elif product_type == 'Organic Fertilizers':
        product = get_object_or_404(OrganicFertilizer, id=product_id)
    elif product_type == 'Safe Pesticides':
        product = get_object_or_404(SafePesticide, id=product_id)
    elif product_type == 'Farm Equipment':
        product = get_object_or_404(FarmEquipment, id=product_id)
    elif product_type == 'Animal Feed':
        product = get_object_or_404(AnimalFeed, id=product_id)
    elif product_type == 'Agri Electronics & Tools':
        product = get_object_or_404(AgriElectronicsTool, id=product_id)
    else:
        messages.error(request, 'Invalid product type')
        return redirect('/products_user/')
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        product_id=product.id,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.name} quantity increased in your cart.")
    else:
        cart_item.quantity = 1
        cart_item.save()
        messages.success(request, f"{product.name} added to your cart.")
    
    return redirect("/products_user/")

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = Decimal('0.00')
    items_with_details = []
    for item in cart_items:
        product = None
        product_type = item.product_type  
        try:
            if item.product_type == 'High-Quality Seeds':
                product = HighQualitySeed.objects.get(id=item.product_id)
            elif item.product_type == 'Organic Fertilizers':
                product = OrganicFertilizer.objects.get(id=item.product_id)
            elif item.product_type == 'Safe Pesticides':
                product = SafePesticide.objects.get(id=item.product_id)
            elif item.product_type == 'Farm Equipment':
                product = FarmEquipment.objects.get(id=item.product_id)
            elif item.product_type == 'Animal Feed':
                product = AnimalFeed.objects.get(id=item.product_id)
            elif item.product_type == 'Agri Electronics & Tools':
                product = AgriElectronicsTool.objects.get(id=item.product_id)
            if product:
                product_price = Decimal(product.price)
                quantity = int(item.quantity)
                item_total = product_price * quantity
                total_price += item_total
                items_with_details.append({
                    'product': product,
                    'quantity': item.quantity,
                    'item_total': item_total,
                    'product_type': product_type 
                })
        except (HighQualitySeed.DoesNotExist, OrganicFertilizer.DoesNotExist, 
                SafePesticide.DoesNotExist, FarmEquipment.DoesNotExist, 
                AnimalFeed.DoesNotExist, AgriElectronicsTool.DoesNotExist):
            pass  
    context = {
        'items_with_details': items_with_details,
        'total_price': total_price,
    }
    return render(request, 'User/cart.html', context)

@login_required
def remove_one_from_cart(request, product_type, product_id):
    try:
        if product_type == 'High-Quality Seeds':
            product = get_object_or_404(HighQualitySeed, id=product_id)
        elif product_type == 'Organic Fertilizers':
            product = get_object_or_404(OrganicFertilizer, id=product_id)
        elif product_type == 'Safe Pesticides':
            product = get_object_or_404(SafePesticide, id=product_id)
        elif product_type == 'Farm Equipment':
            product = get_object_or_404(FarmEquipment, id=product_id)
        elif product_type == 'Animal Feed':
            product = get_object_or_404(AnimalFeed, id=product_id)
        elif product_type == 'Agri Electronics & Tools':
            product = get_object_or_404(AgriElectronicsTool, id=product_id)
        else:
            messages.error(request, 'Invalid product type')
            return redirect('/cart/')
        cart_item = Cart.objects.filter(user=request.user, product_type=product_type, product_id=product.id).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, f"One unit of {product.name} has been removed from your cart.")
            else:
                cart_item.delete()
                messages.success(request, f"{product.name} has been removed from your cart.")
        else:
            messages.error(request, 'This product is not in your cart.')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return redirect('/cart/')

@login_required
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            if not Subscribe.objects.filter(email=email).exists():
                sub = Subscribe(email=email)
                sub.save()
        except Exception as e:
            print(e)
    return redirect("/main_user/")

@login_required
def subscribe_product(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            if not Subscribe.objects.filter(email=email).exists():
                sub = Subscribe(email=email)
                sub.save()
        except Exception as e:
            print(e)
    return redirect("/products_user/")

@login_required
def admin(request):
    if request.user.is_superuser or request.user.username == "Admin_main":
        Seeds = HighQualitySeed.objects.all()
        fertilizerss = OrganicFertilizer.objects.all()
        pesticidess = SafePesticide.objects.all()
        equipments = FarmEquipment.objects.all()
        feeds = AnimalFeed.objects.all()
        electronics_toolss = AgriElectronicsTool.objects.all()
        def truncate_description(queryset):
            for obj in queryset:
                words = obj.description.split()
                image = obj.image.url
                obj.truncated_description = ' '.join(words[:6]) + ('...' if len(words) > 6 else '')
                obj.truncated_image = ''.join(image[:-10]) + ('...' if len(image) > 10 else '')
            return queryset
        context = {
            'HighQualitySeed': truncate_description(Seeds),
            'OrganicFertilizer': truncate_description(fertilizerss),
            'SafePesticide': truncate_description(pesticidess),
            'FarmEquipment': truncate_description(equipments),
            'AnimalFeed': truncate_description(feeds),
            'AgriElectronicsTool': truncate_description(electronics_toolss),
            'Total_Seed': Seeds.count(),
            'Total_fertilizer': fertilizerss.count(),
            'Total_pesticide': pesticidess.count(),
            'Total_equipment': equipments.count(),
            'total_feed': feeds.count(),
            'Total_tool': electronics_toolss.count(),
        }
        return render(request, 'Admin/admin.html', context)
    else:
        messages.error(request, "You are not authorized to access the admin page.")
        return redirect('login')


@login_required
def add_product(request):
    if request.method == "POST":
        model_type = request.POST.get("model")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        image = request.FILES.get('image')
        rating = "⭐" * int(rating) if rating.isdigit() and 1 <= int(rating) <= 5 else "⭐"
        model_mapping = {
            "HighQualitySeed": HighQualitySeed,
            "OrganicFertilizer": OrganicFertilizer,
            "SafePesticide": SafePesticide,
            "FarmEquipment": FarmEquipment,
            "AnimalFeed": AnimalFeed,
            'AgriElectronicsTool': AgriElectronicsTool,
        }
        if model_type in model_mapping:
            try:
                product = model_mapping[model_type](
                    name=name,
                    description=description,
                    price=price,
                    rating=rating,
                    image=image
                )
                product.save()
                return redirect('/Admin_page/')
            except Exception as e:
                return render(request, 'Admin/add_product.html', {
                    'error_message': 'Error saving the product. Please try again.',
                    'model': model_type
                })
    model_type = request.GET.get("model")
    return render(request, 'Admin/add_product.html', {'model': model_type})

MODEL_MAPPING_update = {
        'HighQualitySeed': HighQualitySeed,
        'OrganicFertilizer': OrganicFertilizer,
        'SafePesticide': SafePesticide,
        'FarmEquipment': FarmEquipment,
        'AnimalFeed': AnimalFeed,
        'AgriElectronicsTool': AgriElectronicsTool,
    }

@login_required
def update_product(request, product_type, product_id): 
    ProductForm = get_product_form(product_type)
    product_model = MODEL_MAPPING_update[product_type]
    product_instance = get_object_or_404(product_model, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_instance)
        if form.is_valid():
            rating = request.POST.get('rating')
            star_rating = "⭐" * int(rating) if rating.isdigit() and 1 <= int(rating) <= 5 else "⭐"
            product = form.save(commit=False)
            product.rating = star_rating
            product.save()
            messages.success(request, f'Product {product_instance.name} updated successfully with rating: {star_rating}')
            return redirect('/Admin_page/')
    else:
        form = ProductForm(instance=product_instance)
    if product_instance.rating:
        product_instance.rating=len(product_instance.rating)
    return render(request, 'Admin/update_product.html', {
        'form': form,
        'product_instance': product_instance,
        'product_type': product_type,
        'rating': product_instance.rating,
    })

@login_required
def delete_product(request, product_type, product_id):
    try:
        product_model = MODEL_MAPPING_update[product_type]
        product_instance = get_object_or_404(product_model, id=product_id)
        product_instance.delete()
        messages.success(request, f'Product {product_type} deleted successfully!')
        print("deleted successfully!")
        return redirect('/Admin_page/')
    except Exception as e:
        print(e)

@login_required
def filter_seed(request):
    fil = HighQualitySeed.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(rating__icontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'OrganicFertilizer': fertilizers,
        'SafePesticide': pesticides,
        'FarmEquipment': equipment,
        'AnimalFeed': feed,
        'AgriElectronicsTool': electronics_tools,
        'HighQualitySeed': fil,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def filter_Fertilizer(request):
    fil = OrganicFertilizer.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(ratingicontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'HighQualitySeed': Seed,
        'SafePesticide': pesticides,
        'FarmEquipment': equipment,
        'AnimalFeed': feed,
        'AgriElectronicsTool': electronics_tools,
        'OrganicFertilizer': fil,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def filter_pesticide(request):
    fil = SafePesticide.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(ratingicontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'HighQualitySeed': Seed,
        'FarmEquipment': equipment,
        'AnimalFeed': feed,
        'AgriElectronicsTool': electronics_tools,
        'OrganicFertilizer': fertilizers,
        'SafePesticide': fil,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def filter_equipment(request):
    fil = FarmEquipment.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(ratingicontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'HighQualitySeed': Seed,
        'FarmEquipment': fil,
        'AnimalFeed': feed,
        'AgriElectronicsTool': electronics_tools,
        'OrganicFertilizer': fertilizers,
        'SafePesticide': pesticides,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def filter_feed(request):
    fil = AnimalFeed.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(ratingicontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'HighQualitySeed': Seed,
        'FarmEquipment': equipment,
        'AnimalFeed': fil,
        'AgriElectronicsTool': electronics_tools,
        'OrganicFertilizer': fertilizers,
        'SafePesticide': pesticides,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def filter_tools(request):
    fil = AgriElectronicsTool.objects.all()
    filterid_query = request.GET.get('id')
    filterName_query  = request.GET.get('name')
    filterRating_query  = request.GET.get('rating')
    filterPrice_query  = request.GET.get('price')
    if filterid_query:
        fil = fil.filter(id__icontains= filterid_query)
    if filterName_query:
        fil = fil.filter(name__icontains= filterName_query)
    if filterRating_query:
        fil = fil.filter(ratingicontains= filterRating_query)
    if filterPrice_query:
        fil = fil.filter(price__icontains= filterPrice_query)
    context = {
        'HighQualitySeed': Seed,
        'FarmEquipment': equipment,
        'AnimalFeed': feed,
        'AgriElectronicsTool': fil,
        'OrganicFertilizer': fertilizers,
        'SafePesticide': pesticides,
    }
    return render(request, 'Admin/admin.html', context)

@login_required
def admin_users(request):
    if request.user.is_superuser or request.user.username == "Admin_main":
        users = User.objects.all()
        total_users = len(users)
        totals = users.aggregate(total_superuser=Count('id', filter=Q(is_superuser=True)),total_staff=Count('id', filter=Q(is_staff=True)),total_active=Count('id', filter=Q(is_active=True)))
        return render(request, 'Admin/admin_user.html', {'users':  users, 'total_users':total_users , 'total_staff':totals['total_staff'], 'total_superuser':totals['total_superuser'], 'total_active':totals['total_active'],})
    else:
        return redirect("/login/")
@login_required
def user_filter(request):
        users = User.objects.all()
        Users = User.objects.all()
        q_join = request.GET.get('date_joined')
        q_fname  = request.GET.get('fname')
        q_lname  = request.GET.get('lname')
        q_username = request.GET.get('username')
        q_email  = request.GET.get('email')
        q_is_superuser  = request.GET.get('is_superuser')
        q_is_staff  = request.GET.get('is_staff')
        q_is_active  = request.GET.get('is_active')
        if q_join:
            users = users.filter(date_join__icontains= q_join)
        if q_fname:
            users = users.filter(first_name__icontains= q_fname)
        if q_lname:
            users = users.filter(last_name__icontains= q_lname)
        if q_username:
            users = users.filter(username__icontains= q_username)
        if q_email:
            users = users.filter(email__icontains= q_email)
        if q_is_superuser:
            users = users.filter(is_superuser__icontains= q_is_superuser)
        if q_is_staff:
            users = users.filter(is_staff__icontains= q_is_staff)
        if q_is_active:
            users = users.filter(is_active__icontains= q_is_active)
        total_users = len(Users)
        totals = Users.aggregate(total_superuser=Count('id', filter=Q(is_superuser=True)),total_staff=Count('id', filter=Q(is_staff=True)),total_active=Count('id', filter=Q(is_active=True)))
        return render(request, 'Admin/Admin_user.html', {'users': users, 'total_users':total_users , 'total_staff':totals['total_staff'], 'total_superuser':totals['total_superuser'], 'total_active':totals['total_active']})

@login_required
def user_update(request, user_update_id):
    user = get_object_or_404(User, id=user_update_id)
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_update_id)
        form = UserUpdationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/admin_user/")
        else:
            print("--------Error in form-----------")
    else:
        form = UserUpdationForm(instance=user)
    return render(request, 'Admin/user_update.html', {'form': form, 'user':user})

@login_required
def make_superuser(request, user_update_id):
    user = get_object_or_404(User, id=user_update_id)
    if not user.is_superuser:
        user.is_superuser = True
        user.save()
        messages.success(request, f'{user.username} is now a superuser.')
    else:
        messages.info(request, f'{user.username} is already a superuser.')
    return redirect('/admin_user/')

@login_required
def remove_superuser(request, user_update_id):
    user = get_object_or_404(User, id=user_update_id)
    if user.is_superuser:
        user.is_superuser = False
        user.save()
        messages.success(request, f'{user.username} is no longer a superuser.')
    else:
        messages.info(request, f'{user.username} is not a superuser.')
    return redirect('/admin_user/') 

@login_required
def make_staff(request, user_update_id):
    user = get_object_or_404(User, id=user_update_id)
    if not user.is_staff:
        user.is_staff = True
        user.save()
        messages.success(request, f'{user.username} is now a staff member.')
    else:
        messages.info(request, f'{user.username} is already a staff member.')
    return redirect('/admin_user/')

@login_required
def remove_staff(request, user_update_id):
    user = get_object_or_404(User, id=user_update_id)
    if user.is_staff:
        user.is_staff = False
        user.save()
        messages.success(request, f'{user.username} is no longer a staff member.')
    else:
        messages.info(request, f'{user.username} is not a staff member.')
    return redirect('/admin_user/') 

@login_required
def user_delete(request, user_del_id):
    user = get_object_or_404(User, id=user_del_id)
    user.delete()
    return redirect("/admin_user/")

@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request) 
    return redirect('/login/')

@login_required
def buy(request, item_total):
    try:
        total_price = float(item_total)
        upi_id = "ravikasabe1010-2@oksbi"
        qr_code = None
        upi_url = (
            f'upi://pay?pa={upi_id}&am={total_price:.2f}&cu=INR')
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return render(request, 'buy.html', {'total_price':total_price, 'qr_code': qr_code})
    except ValueError:
        return render(request, 'error.html', {'message': 'Invalid total value.'})
    

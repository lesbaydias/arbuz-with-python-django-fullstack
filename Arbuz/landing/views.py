from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, Edit,ItemForm,Payment, EditPayment,EditProfileForm,EditPasswordForm
from .models import ItemTable, BasketItem, Payment_Card, PurchaseItem, Purchase
from .decorators import is_admin, apply_to_all_methods

import requests
import json


api_key = '63a0a36d21ac437bb8b173d5e44bfc53'
api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key

def get_ip_geolocation_data(ip_address):
    # not using the incoming IP address for testing
    print(ip_address)
    response = requests.get(api_url)
    return response.content


def user_city(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    geolocation_json = get_ip_geolocation_data(ip)
    geolocation_data = json.loads(geolocation_json)
    country = geolocation_data['country']
    region = geolocation_data['region']
    request.session['country'] = country
    request.session['region'] = region


@csrf_exempt
def home(request):
    user_city(request)
    context = {
        "Fruits": ItemTable.objects.all().filter(category__contains='Fruits'),
        "Drinks": ItemTable.objects.all().filter(category__contains='Drinks'),
        "Vegetables": ItemTable.objects.all().filter(category__contains='Vegetables')
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.save()
            return redirect('log_in')
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'sign_in.html', {'form': form})

def edit(request, pk):
    context = {}
    obj = get_object_or_404(User, pk=pk)
    form = Edit(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'index.html')
    context["form"] = form

    return render(request, "edit.html", context)


def delete(request):
    del request.session['viewed_items']
    return HttpResponseRedirect('home')


def detail(request, id):
    context = {}
    data = ItemTable.objects.get(id=id)
    context["data"] = data
    first = True
    if request.user.is_authenticated:
        basket = BasketItem.objects.filter(user=request.user, item=data)
        if basket:
            first = False
            basket = basket[0]
            context['num'] = basket.quantity
        context['first'] = first
        max_viewed_item_length = 10
        viewed_items = request.session.get('viewed_items', [])
        viewed_item = data.id, data.name
        b = False
        if len(viewed_items) > 0:
            for d in viewed_items:
                if d[0] == viewed_item[0]:
                    b = True

        if not b:
            viewed_items.insert(0, viewed_item)
            viewed_items = viewed_items[:max_viewed_item_length]
            request.session['viewed_items'] = viewed_items

    return render(request, "detail.html", context)


def search_books(request):
    name = request.GET.get('name', "")
    data = ItemTable.objects.filter(name__icontains=name)
    context = {
        'data': data,
        'name': name,
    }
    return render(request, "search.html", context)


def item_list(request):
    sort_option = request.GET.get('sort', 'asc')
    query = request.GET.get('q')

    if query and sort_option == 'asc':
        items = ItemTable.objects.filter(name__icontains=query)
        items = items.order_by('price')

    elif query and sort_option == 'desc':
        items = ItemTable.objects.filter(name__icontains=query)
        items = items.order_by('-price')
    else:
        items = ItemTable.objects.all()

    if sort_option == 'asc':
        items = items.order_by('price')
    elif sort_option == 'desc':
        items = items.order_by('-price')

    return render(request, 'allForClients.html', {'items': items, 'sort_option': sort_option, 'query': query})


def catalog(request, category):
    context = {
        "items": ItemTable.objects.all().filter(category__contains=category),
        'name': category
    }
    return render(request, 'catalog.html', context)

@apply_to_all_methods(login_required(login_url='home'))
@apply_to_all_methods(is_admin(login_url='home'))
class Admin:
    def UU(request):
        context = {
            "allForUsers": User.objects.all()
        }
        return render(request, 'UU.html', context)

    def allEdit(request):
        context = {
            "allForClientsItems": ItemTable.objects.all()
        }
        return render(request, 'allEdit.html', context)

    def allUsers(request):
        context = {
            "allForUsers": User.objects.all()
        }
        return render(request, 'allUsers.html', context)


    def AdminUser(request):
        return render(request, 'AdminUser.html')

    def all(request):
        context = {
            "allForClientsItems": ItemTable.objects.all()
        }
        return render(request, 'all.html', context)

    def insert(request):
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/all")
        else:
            form = ItemForm()
        return render(request, 'media.html', {'form': form})

    def insertUsers(request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/allUsers")
        else:
            form = RegistrationForm()
        return render(request, 'insertUserMedia.html', {'form': form})

    def updateItems(request, pk):
        if pk is not None:
            items = get_object_or_404(ItemTable, pk=pk)
        else:
            items = None

        if request.method == "POST":
            form = ItemForm(request.POST, instance=items)
            if form.is_valid():
                return render(request, "AdminUser.html")
        else:
            form = ItemForm(instance=items)

        return render(request, "Update.html",
                      {"form": form, "instance": items, "model_type": "Item"})

    def deleteItems(request, pk=None):
        context = {}
        if pk is not None:
            items = get_object_or_404(ItemTable, pk=pk)
        else:
            items = None

        if request.method == "POST":
            items.delete()
            return HttpResponseRedirect('/allForClients')

        return render(request, 'delete.html', context)

    def updateOnlyUser(request, pk=None):
        context = {}
        if pk is not None:
            user = get_object_or_404(User, pk=pk)
        else:
            user = None

        if request.method == "POST":
            user.delete()
            return HttpResponseRedirect('/allUsers')

        return render(request, 'delete.html', context)

class All:
    def signout(request):
        logout(request)
        return redirect('home')

    def profile(request):
        data = request.user
        card = Payment_Card.objects.filter(user=data).values()
        items = Purchase.objects.filter(user=request.user)
        if card:
            card = card[0]
        context = {
            "datas": card,
            "items": items,
        }

        return render(request, 'profile.html', context)

    def allForClients(request):
        context = {
            "allForClientsItems": ItemTable.objects.all()
        }
        return render(request, 'allForClients.html', context)




def creditcard(request):
    if request.method == 'POST':
        form = Payment(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('profile')
    else:
        form = Payment()
    return render(request, 'createCreditCard.html', {'form': form})



def update_basket(request):
    print(request.GET)
    id = request.GET['id']
    action = request.GET['action']
    page = request.GET['page']
    item = ItemTable.objects.get(pk=id)
    context = {}
    basket = BasketItem.objects.filter(item=item, user=request.user)
    if basket:
        basket = basket[0]
    if action == 'add':
        if not basket:
            basket = BasketItem(user=request.user, item=item, quantity=0)
        basket.quantity += 1
        context['quantity'] = basket.quantity
        basket.save()
    elif action == 'remove':
        basket.quantity -= 1
        context['quantity'] = basket.quantity
        basket.save()
        if basket.quantity == 0:
            basket.delete()
    elif action == 'delete':
        context['quantity'] = 0
        basket.delete()
    if page=='basket':
        html = updated_basket(request.user)
        context['html']=html
    total = BasketItem.objects.filter(user=request.user)
    sum = 0
    for i in total:
        sum += i.subtotal()
    context['sum']=sum
    return JsonResponse(context)


def updated_basket(user):
    html =''
    items = BasketItem.objects.filter(user=user)
    for i in items:
        html+='<div class="row">\
              <div class="col-lg-3 col-md-12 mb-4 mb-lg-0">\
                <!-- Image -->\
                <div class="bg-image hover-overlay hover-zoom ripple rounded" data-mdb-ripple-color="light">\
                  <img src="'+ i.item.image_field.url +'"\
                    class="w-100" alt="Product" />\
                  <a href="#!">\
                    <div class="mask" style="background-color: rgba(251, 251, 251, 0.2)"></div>\
                  </a>\
                </div>\
                <!-- Image -->\
              </div>\
              <div class="col-lg-5 col-md-6 mb-4 mb-lg-0">\
                <!-- Data -->\
                <p><strong>'+ i.item.name +'</strong></p>\
                <button type="button" class="btn btn-primary btn-sm me-1 mb-2" data-mdb-toggle="tooltip"\
                  title="Remove item" onclick="update_basket('+ str(i.item.id) +', \'delete\', \'basket\')">\
                  <i class="fas fa-trash"></i>\
                </button>\
                <button type="button" class="btn btn-danger btn-sm mb-2" data-mdb-toggle="tooltip"\
                  title="Move to the wish list">\
                  <i class="fas fa-heart"></i>\
                </button>\
                <!-- Data -->\
              </div>\
              <div class="col-lg-4 col-md-6 mb-4 mb-lg-0">\
                <!-- Quantity -->\
                <div class="d-flex mb-4" style="max-width: 300px">\
                  <button class="btn btn-primary px-3 me-2"\
                    onclick="update_basket('+ str(i.item.id) +', \'remove\', \'basket\')">\
                    <i class="fas fa-minus"></i>\
                  </button>\
                  <div class="form-outline">\
                    <input id="form1" min="0" name="quantity" value="'+str(i.quantity)+'" type="number" class="form-control" readonly >\
                  </div>\
                  <button class="btn btn-primary px-3 ms-2"\
                    onclick="update_basket('+ str(i.item.id) +', \'add\', \'basket\')">\
                    <i class="fas fa-plus"></i>\
                  </button>\
                </div>\
                <!-- Price -->\
                <p class="text-start text-md-center">\
                  <strong>'+ str(i.subtotal()) +'</strong>\
                </p>\
                <!-- Price -->\
              </div>\
            </div>\
            <hr class="my-4" />'
    return html


def basket(request):
    user = request.user
    items = BasketItem.objects.filter(user=user)
    sum = 0
    for i in items:
        sum += i.subtotal()
    print(items)
    return render(request, 'basket.html',{
        'items': items,
        'sum': sum,
    })


def basket_submit(request):
    items = BasketItem.objects.filter(user=request.user)
    sum = 0
    if not items:
        return render(request, 'failure.html', {
            'text': 'User does not have items in card'
        })
    for i in items:
        sum += i.subtotal()

    obj = Payment_Card.objects.filter(user=request.user)
    if obj:
        obj = obj[0]
        balance = obj.balance
    else:
        return render(request, 'failure.html',{
            'text': 'User does not have card'
        })

    if balance < sum:
        return render(request, 'failure.html', {
            'text': 'User does not have enough money'
        })
    balance -= sum
    obj.balance = balance
    obj.save()
    purchase = Purchase(user=request.user, total_sum=sum)
    purchase.save()
    for i in items:
        p_item = PurchaseItem(item=i.item, quantity=i.quantity, purchase=purchase)
        p_item.save()
        i.delete()
    return redirect('home')


def editProfile(request, pk):
    context = {}
    obj = get_object_or_404(User, pk=pk)
    form = EditProfileForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('profile')
    context["form"] = form

    return render(request, "edit.html", context)


def editPassword(request, pk):
    context = {}
    obj = get_object_or_404(User, pk=pk)
    form = EditPasswordForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('profile')
    context["form"] = form

    return render(request, "edit.html", context)


def editPayment(request):
    if request.method == 'POST':
        obj = get_object_or_404(Payment_Card, user=request.user)
        form = EditPayment(request.POST, request.FILES)

        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            balance = form.cleaned_data['balance']
            if card_number == obj.card_number:
                obj.balance += balance
                obj.save()
                return redirect('profile')
            else:
                form.add_error("card_number", "Wrong card number")
    else:
        form = EditPayment()
    return render(request, 'creditcard.html', {'form': form})


def show_purchase(request):
    purchase = Purchase.objects.filter(user=request.user)
    list = []
    for i in purchase:
        list.append(PurchaseItem.objects.filter(purchase=i))
    return render(request, 'purchase.html', {
        'list': list
    })

def map(request):
    response = requests.get('https://api.ipdata.co?api-key=abe293b41e6b06708553d5e08b1341f84acee4b5d2cf2d8e95bec043')
    data = response.json()
    print(data)
    list = []
    list.append({
        'lat': 43.36712223952115,
        'lon': 76.94921186908212
    })
    list.append({
        'lat': 43.20771260922432,
        'lon': 76.66911749104598
    })
    list.append({
        'lat': 42.455928125183796,
        'lon': 69.52673523929923
    })
    list.append({
        'lat': 47.05251554474009,
        'lon': 51.870877519045486
    })
    list.append({
        'lat': 40.68936728875058,
        'lon': -74.0444964719105
    })
    list = json.dumps(list)
    context = {'list': list}
    return render(request, 'map.html', context)
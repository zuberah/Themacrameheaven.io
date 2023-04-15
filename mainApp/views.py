from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(Request):
    product = Product.objects.all()
    product = product[::-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(Request, "index.html", {"product": product,"maincategory": maincategory, "subcategory": subcategory})

def servicepage(Request):
    return render(Request, "service.html")


def aboutpage(Request):
    product = Product.objects.all()
    product = product[::-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(Request, "about.html",{"product": product, "maincategory": maincategory, "subcategory": subcategory})

def shoppage(Request, mc, sc):
    if (mc == 'All' and sc == 'All'):
        product = Product.objects.all()
    elif (mc != 'All' and sc == 'All'):
        product = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc))
    elif (mc == 'All' and sc != 'All'):
        product = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc))
    else:
        product = Product.objects.filter(subcategory=Subcategory.objects.get(
            name=sc), maincategory=Maincategory.objects.get(name=mc))
    count = len(product)
    product = product[::-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()

    return render(Request, "shop.html", {"product": product, "maincategory": maincategory, "subcategory": subcategory, 'mc': mc, 'sc': sc, 'count': count})


def pricefilter(Request, mc, sc):
    if (Request.method == 'POST'):
        min = Request.POST.get('min')
        max = Request.POST.get('max')
        if (mc == 'All' and sc == 'All'):
            product = Product.objects.all()
        elif (mc != 'All' and sc == 'All'):
            product = Product.objects.filter(finalprice__gte=min, finalprice__lte=max,
                                             maincategory=Maincategory.objects.get(name=mc))
        elif (mc == 'All' and sc != 'All'):
            product = Product.objects.filter(finalprice__gte=min, finalprice__lte=max,
                                             subcategory=Subcategory.objects.get(name=sc))
        else:
            product = Product.objects.filter(finalprice__gte=min, finalprice__lte=max, subcategory=Subcategory.objects.get(
                name=sc), maincategory=Maincategory.objects.get(name=mc))
        # product = Product.objects.filter(finalprice__gte=min, finalprice__lte=max)
        # finaldata = []
        # for item in product:
        #     if (item.finalprice >= int(min) and item.finalprice <= int(max)):
        #         finaldata.append(item)
        # product = finaldata
        count = len(product)
        product = product[::-1]
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {"product": product, "maincategory": maincategory, "subcategory":   subcategory, 'count': count, 'mc': mc, 'sc': sc})
    else:
        return HttpResponseRedirect('/shop/All/All')


def sortfilter(Request, mc, sc):
    if (Request.method == 'POST'):
        sort = Request.POST.get('sort')
        if (sort == 'newest'):
            sort = 'id'
        elif (sort == 'HTOL'):
            sort = 'finalprice'
        elif (sort == 'LTOH'):
            sort = '-finalprice'
        if (mc == 'All' and sc == 'All'):
            product = Product.objects.all().order_by(sort)
        elif (mc != 'All' and sc == 'All'):
            product = Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc)).order_by(sort)
        elif (mc == 'All' and sc != 'All'):
            product = Product.objects.filter(
                subcategory=Subcategory.objects.get(name=sc)).order_by(sort)
        else:
            product = Product.objects.filter(subcategory=Subcategory.objects.get(
                name=sc), maincategory=Maincategory.objects.get(name=mc)).order_by(sort)
        # product = Product.objects.filter(finalprice__gte=min, finalprice__lte=max)
        # finaldata = []
        # for item in product:
        #     if (item.finalprice >= int(min) and item.finalprice <= int(max)):
        #         finaldata.append(item)
        # product = finaldata
        count = len(product)
        product = product[::-1]
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {"product": product, "maincategory": maincategory, "subcategory":   subcategory, 'count': count, 'mc': mc, 'sc': sc})
    else:
        return HttpResponseRedirect('/shop/All/All')


def searchpage(Request):
    if (Request.method == 'POST'):
        search = Request.POST.get('search')
        product = Product.objects.filter(
            Q(name__icontains=search) | Q(color__icontains=search))
        count = len(product)
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        return render(Request, "shop.html", {"product": product, "maincategory": maincategory, "subcategory":   subcategory, 'count': count, 'mc': 'All', 'sc': 'All'})
    else:
        return HttpResponseRedirect('shop/All/All/')


def singleproduct(Request, num):
    product = Product.objects.get(id=num)
    return render(Request, "single-product.html", {"product": product})


def loginpage(Request):
    if (Request.method == 'POST'):
        username = Request.POST.get('username')
        password = Request.POST.get('password')
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(Request, user)
            if (user.is_superuser):
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponseRedirect('/profile')
        else:
            messages.error(Request, 'Invalid username or password')
    return render(Request, 'login.html')


def signuppage(Request):
    if (Request.method == 'POST'):
        name = Request.POST.get('name')
        username = Request.POST.get('username')
        email = Request.POST.get('email')
        phone = Request.POST.get('phone')
        password = Request.POST.get('password')
        cpassword = Request.POST.get('cpassword')
        if (password == cpassword):
            try:
                user = User(username=username)
                user.set_password(password)
                user.save()
                buyer = Buyer()
                buyer.name = name
                buyer.username = username
                buyer.email = email
                buyer.phone = phone
                buyer.password = password
                buyer.save()
                return HttpResponseRedirect('/login')
            except:
                messages.error(Request, "user already exist !!!")
        else:
            messages.error(Request, "password doesn't matched !!!")
    return render(Request, 'signup.html')


def logoutpage(Request):
    logout(Request)
    return HttpResponseRedirect('/login')


def contactpage(Request):
    return render(Request, 'contact.html')

def confirmationpage(Request):
    return render(Request,"confirmation.html")


# decorators means to enhance it's functionality without changing the code
@login_required(login_url='/login/')
def profilepage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        wishlist = Wishlist.objects.filter(user=buyer  )
        return render(Request, "profile.html", {"data": buyer})


# decorators means to enhance it's functionality without changing the code
@login_required(login_url='/login/')
def updateprofilepage(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        if (Request.method == "POST"):
            buyer.name = Request.POST.get('name')
            buyer.email = Request.POST.get('email')
            buyer.phone = Request.POST.get('phone')
            buyer.addressline1 = Request.POST.get('addressline1')
            buyer.addressline2 = Request.POST.get('addressline2')
            buyer.addressline3 = Request.POST.get('addressline3')
            buyer.pin = Request.POST.get('pin')
            buyer.city = Request.POST.get('city')
            buyer.state = Request.POST.get('state')
            if (Request.FILES.get('pic')):
                buyer.pic = Request.FILES.get('pic')
            buyer.save()
            return HttpResponseRedirect('/profile/')
    return render(Request, "update-profile.html", {"data": buyer})


def AddToCart(Request, num):
    p = Product.objects.get(id=num)
    cart = Request.session.get('cart', None)
    if (cart):
        if (str(p.id) in cart):
            item = cart[str(p.id)]
            item['qty'] = item['qty']+1
            item['total'] = item['total']+p.finalprice
            cart[str(p.id)] = item

        else:
            cart.setdefault(str(p.id), {'name': p.name, 'color': p.color, 'size': p.size,
                            'price': p.finalprice, 'qty': 1, 'total': p.finalprice, 'pic': p.pic1.url})
    else:
        cart = {str(p.id): {'name': p.name, 'color': p.color, 'size': p.size,
                            'price': p.finalprice, 'qty': 1, 'total': p.finalprice, 'pic': p.pic1.url}}
    Request.session['cart'] = cart
    total = 0
    for value in cart.values():
        total = total + value['total']
    if (total < 1000 and total > 0):
        shipping = 150
    else:
        shipping = 0
    Request.session['total'] = total
    Request.session['shipping'] = shipping
    Request.session['final'] = total + shipping
    return HttpResponseRedirect('/cart/')


def cartPage(Request):
    cart = Request.session.get('cart', None)
    items = []
    for key, value in cart.items():
        value.setdefault('id', key)
        items.append(value)
    total = Request.session.get('total', 0)
    shipping = Request.session.get('shipping', 0)
    final = Request.session.get('final', 0)

    return render(Request, 'cart.html', {'cart': items, 'total': total, 'shipping': shipping, 'final': final})


def deletepage(Request, id):
    cart = Request.session.get('cart', None)
    if (cart and id in cart):
        del cart[id]
        Request.session['cart'] = cart
        total = 0
        for value in cart.values():
            total = total + value['total']
        if (total < 1000 and total > 0):
            shipping = 150
        else:
            shipping = 0
        Request.session['total'] = total
        Request.session['shipping'] = shipping
        Request.session['final'] = total + shipping
    return HttpResponseRedirect('/cart/')


def UpdateCartPage(Request, id, op):
    cart = Request.session.get('cart', None)
    if (cart and id in cart):
        item = cart[id]
        if (op == "dec" and item['qty'] == 1):
            pass
        elif (op == "dec"):
            item['qty'] = item['qty']-1
            item['total'] = item['total']-item['price']
        else:
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
        cart[id] = item
        Request.session['cart'] = cart
        total = 0
        for value in cart.values():
            total = total + value['total']
        if (total < 1000 and total > 0):
            shipping = 150
        else:
            shipping = 0
        Request.session['total'] = total
        Request.session['shipping'] = shipping
        Request.session['final'] = total + shipping
        return HttpResponseRedirect('/cart/')


@login_required(login_url='/login/')
def checkoutpage(Request):
    user = User.objects.get(username=Request.user.username)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username = Request.user.username)
    total = Request.session.get('total', 0)
    if(total==0):
        return HttpResponseRedirect('/cart/')
    return render(Request,"checkout.html",{"data":buyer})


@login_required(login_url='/login/')
def placeOrder(Request):
    user = User.objects.get(username=Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        total = Request.session.get('total',0)
        if(total):
            shipping = Request.session.get('shipping',0)
            final = Request.session.get('final',0)
            buyer = Buyer.objects.get(username=Request.user.username)
            checkout = Checkout()
            checkout.user = buyer
            checkout.totalAmount = total
            checkout.shippingAmount = shipping
            checkout.finalAmount = final
            checkout.save()
            cart = Request.session.get('cart')
            for key,value in cart.items():
                checkoutproduct = CheckoutProducts()
                checkoutproduct.checkout = checkout
                checkoutproduct.pid = int(key)
                checkoutproduct.name = value['name']
                checkoutproduct.color = value['color']
                checkoutproduct.size = value['size']
                checkoutproduct.price = value['price']
                checkoutproduct.qty = value['qty']
                checkoutproduct.total = value['total']
                checkoutproduct.pic = value['pic']
                checkoutproduct.save()
            Request.session['cart']={}
            Request.session['total']=0
            Request.session['shipping']=0
            Request.session['final']=0
            Request.session['cartcount']=0
            return HttpResponseRedirect('/confirmation/')
            
        else:
            return HttpResponseRedirect("/cart/")
        
@login_required(login_url='/login/')      
def addToWishlist(Request,num):
    user = User.objects.get(username = Request.user.username)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        buyer = Buyer.objects.get(username = Request.user.username)
        product = Product.objects.get(id = num)
        try:
            wishlist = Wishlist.objects.get(user=buyer, product = product)
        except:
            wish = Wishlist()
            wish.user = buyer
            wish.product = product
            wish.save()
        return HttpResponseRedirect('/profile/')




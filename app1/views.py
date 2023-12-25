from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.contrib import messages

def form(request):
    return render(request,"form.html")

def register(request):
    errors = user.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        passwd = request.POST['pass']
        hashed_pwd= bcrypt.hashpw(passwd.encode(), bcrypt.gensalt()).decode()
        X =user.create(
            first=request.POST['fname'],
            last=request.POST['lname'],
            email=request.POST['email'],
            birth=request.POST['bdate'],
            pwd=hashed_pwd
        )
        request.session['id'] = X.id
        request.session['username'] = X.first_name
    return redirect("/main")

def login(request):
    check_user = user.objects.filter(email=request.POST['e-mail'])
    if check_user:
        logged_user = check_user[0]
        if bcrypt.checkpw(request.POST['passwd'].encode(),logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['username'] = logged_user.first_name
            return redirect("/main")
        else:
            messages.error(request,"Invalid password")
            return redirect("/")
    else:
        messages.error(request,"Invalid email")
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def main(request):
    if not 'id' in request.session:
        messages.error(request,"No user logged in")
        return redirect("/")
    else:
        context={
            "oneuser":user.show(request.session['id']),
            "allres":restaurant.showall(),
            "favres": restaurant.show_fav(request.session['id']),
            "toprated":restaurant.rate()
        }
        return render(request,"index.html",context)

def addres(request):
    if not 'id' in request.session:
        messages.error(request,"No user logged in")
        return redirect("/")
    return render(request,"addres.html")

def create_res(request):
    errors2 = restaurant.objects.validator2(request.POST)
    if len(errors2) > 0:
        for key,value in errors2.items():
            messages.error(request, value)
        return redirect("/addres")
    else:
        X = restaurant.create(
            request.POST['res_name'],
            request.POST['res_location'],
            request.POST['foodtype'],
            request.session['id']
        )
        return redirect("/oneres/"+str(X.id))
    
def del_res(request,id):
    restaurant.delete(id)
    return redirect("/main#all-res")

def edit_res(request,id):
    context={
        "oneres":restaurant.showone(id)
    }
    return render(request,"edit.html",context)

def update_res(request,id):
    errors2 = restaurant.objects.validator2(request.POST)
    if len(errors2) > 0:
        for key,value in errors2.items():
            messages.error(request, value)
        return redirect("/edit_res/"+str(id))
    else:
        X=restaurant.update(
            request.POST['res_name'],
            request.POST['res_location'],
            request.POST['foodtype'],
            id
        )
        return redirect("/oneres/"+str(X.id))

def fav_res(request,id):
    restaurant.fav(
        request.session['id'],
        id
        )
    return redirect("/main#fav_ones")

def unfav_res(request,id):
    restaurant.unfav(request.session['id'], id)
    return redirect("/main#fav_ones")

def show_res(request,id):
    context={
        "oneres":restaurant.showone(id),
        "allrate":rate.showall(id),
        "rate":rate.rating(id),
        "allrev":review.showall(id),
        "oneuser":user.show(request.session['id']),
    }
    return render(request,"res.html",context)

def rate_res(request,id):
    rate.create(
        request.POST['rating1'],
        request.session['id'],
        id
    )

    review.create(
        request.POST['review1'],
        request.session['id'],
        id
    )

    return redirect("/oneres/"+str(id))

def del_rev(request,id1,id2):
    review.delete(id1)
    return redirect("/oneres/"+str(id2))

def edit_rev(request,id1,id2):
    context={
        "oneres":restaurant.showone(id2),
        "onerev":review.showone(id1)
    }
    return render(request,"rev_update.html",context)

def update_rev(request,id1,id2):
        review.update(
            request.POST['rev1'],
            id1,
        )
        return redirect("/oneres/"+str(id2))

def find(request):
    request.session['loc'] = request.POST['res_location']
    return redirect("/find2")

def find2(request):
    context={
        "allres":restaurant.find(request.session['loc']),
        "loc":request.session['loc']
    }
    return render(request,"find.html", context)
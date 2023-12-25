
# ********************************************************************************************
# imports
# ********************************************************************************************

from django.db import models
import datetime
from datetime import datetime
import re
from django.db.models import Avg,Count

# ********************************************************************************************
# class user
# ********************************************************************************************

class userManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['fname']) < 2:
            errors["fname"] = "first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email Address"
        if len(user.objects.filter(email = postData['email'])) > 0:
            errors["email"] = "Email address must be unique"

        if postData['bdate'] == "":
            errors["bdate"] = "Birth date is mandatory"
        else:
            bdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            date_num1 = datetime.today().year
            date_num2 = bdate.year
            if datetime.today() < bdate:
                errors["bdate"] = "Birth date should be in the past"
            elif (date_num1 - date_num2) < 13:
                errors["bdate"] = "Age should be 13 years old at least"

        if len(postData['pass']) < 8:
            errors["password"] = "password should be at least 8 charcters"
        if postData["con-pass"] != postData['pass']:
            errors["password"] = "Password should be the same"
        return errors

class user(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=70)
    birth_date=models.DateField()
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=userManager()

    def create(first,last,email,birth,pwd):
        return user.objects.create(
        first_name=first,
        last_name=last,
        email=email,
        birth_date=birth,
        password=pwd
        )
    
    def show(id):
        return user.objects.get(id=id)

# ********************************************************************************************
# class restaurant
# ********************************************************************************************

class restaurantManager(models.Manager):
    def validator2(self,postData):
        errors2={}
        if postData['res_name'] == "":
            errors2["res_name"] = "Restaurant name is required"
        if len(restaurant.objects.filter(name= postData['res_name'])):
            errors2["res_name"] = "This Restaurant is already added"
        if postData['res_location'] == "":
            errors2["res_location"] = "Restaurant location is required"
        if postData['foodtype'] == "":
            errors2["foodtype"] = "Restaurant Cuisine type is required"
        return errors2

class restaurant(models.Model):
    name=models.CharField(max_length=45)
    location=models.CharField(max_length=45)
    foodtype=models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(user, related_name= "uploaded_ones", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(user,related_name="liked_ones")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=restaurantManager()

    def create(name,location,foodtype,uploaded_by):
        return restaurant.objects.create(
        name = name,
        location = location,
        foodtype = foodtype,
        uploaded_by = user.objects.get(id=uploaded_by)
        )

    def showone(id):
        return restaurant.objects.get(id=id)

    def showall():
        return restaurant.objects.all()

    def show_fav(usr_id):
        logged_user = user.objects.get(id=usr_id)
        return logged_user.liked_ones.all()

    def delete(id):
        X =restaurant.objects.filter(id=id)
        X.delete()

    def update(name,location,foodtype,id):
        res = restaurant.objects.get(id=id)
        res.name = name
        res.location = location
        res.foodtype = foodtype
        res.save()
        return res

    def fav(usr_id,res_id):
        res = restaurant.objects.get(id=int(res_id))
        usr = user.objects.get(id=int(usr_id))
        res.users_who_like.add(usr)

    def unfav(usr_id,res_id):
        res = restaurant.objects.get(id=int(res_id))
        usr = user.objects.get(id=int(usr_id))
        res.users_who_like.remove(usr)

    def rate():
        return restaurant.objects.all().annotate(num_rates=Count('res_rated')).order_by('-num_rates')[:5]

    def find(location):
        return restaurant.objects.filter(location = location)

# ********************************************************************************************
# class rate
# ********************************************************************************************

class rate(models.Model):
    rate = models.IntegerField()
    rated_by = models.ForeignKey(user, related_name= "rated_ones", on_delete = models.CASCADE)
    rated_res = models.ForeignKey(restaurant, related_name= "res_rated", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create(rate1,usr_id,res_id):
        return rate.objects.create(
            rate=rate1,
            rated_by = user.objects.get(id=int(usr_id)),
            rated_res = restaurant.objects.get(id=int(res_id))
        )

    def rating(res_id):
        num= rate.objects.filter(rated_res=int(res_id)).aggregate(Avg('rate'))
        num1= num['rate__avg']
        if num1:
            return round(num1,1)
        else:
            return num1
        
    def showall(res_id):
        num= rate.objects.filter(rated_res=int(res_id)).aggregate(Count('rate'))
        num1= num['rate__count']
        if num1:
            return round(num1,1)
        else:
            return num1

# ********************************************************************************************
# class review
# ********************************************************************************************

class review(models.Model):
    review = models.TextField()
    reviewed_by = models.ForeignKey(user, related_name= "reviewed_ones", on_delete = models.CASCADE)
    reviewed_res = models.ForeignKey(restaurant, related_name= "review", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create(review1,usr_id,res_id):
        return review.objects.create(
            review=review1,
            reviewed_by = user.objects.get(id=int(usr_id)),
            reviewed_res = restaurant.objects.get(id=int(res_id))
        )
    
    def showall(res_id):
        return review.objects.filter(reviewed_res=int(res_id))
    
    def showone(rev_id):
        return review.objects.get(id=int(rev_id))
    
    def delete(id):
        X =review.objects.filter(id=id)
        X.delete()

    def update(rev1,rev_id):
        rev = review.objects.get(id=rev_id)
        rev.review = rev1
        rev.save()
        return rev

# ********************************************************************************************
# ********************************************************************************************

from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('register', views.register),
    path('login', views.login),
    path('main', views.main),
    path('logout', views.logout),
    path('addres', views.addres),
    path('create_res', views.create_res),
    path('del_res/<int:id>', views.del_res),
    path('edit_res/<int:id>', views.edit_res),
    path('update_res/<int:id>', views.update_res),
    path('fav_res/<int:id>', views.fav_res),
    path('unfav_res/<int:id>', views.unfav_res),
    path('oneres/<int:id>', views.show_res),
    path('rate/<int:id>', views.rate_res),
    path('del_rev/<int:id1>/<int:id2>', views.del_rev),
    path('edit_rev/<int:id1>/<int:id2>', views.edit_rev),
    path('update_rev/<int:id1>/<int:id2>', views.update_rev),
    path('find', views.find),
    path('find2', views.find2),
]
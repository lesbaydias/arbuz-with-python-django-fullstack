from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from landing import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),

    path('AdminUser', views.Admin.AdminUser, name='AdminUser'),
    path('all/', views.Admin.all, name='all'),
    path('allUsers/', views.Admin.allUsers, name='all'),
    path('insert/', views.Admin.insert, name='insert'),
    path('insertUsers/', views.Admin.insertUsers, name='insert'),
    path('UU', views.Admin.UU, name='UU'),
    path('allEdit', views.Admin.allEdit, name='allEdit'),
    path('<int:pk>/updateItems', views.Admin.updateItems, name='updateItems'),
    path('<int:pk>/deleteItems', views.Admin.deleteItems, name='deleteItems'),
    path('AdminUser/<int:pk>/delete', views.Admin.updateOnlyUser, name='updateOnlyUser'),

    path('<int:id>/detail', views.detail, name='detail'),

    path('allForClients', views.All.allForClients, name='allForClients'),
    path('sign-up', views.signup, name='signup'),
    path('log_in', views.log_in, name='log_in'),
    path('signout', views.All.signout, name='signout'),
    path('profile', views.All.profile, name='profile'),
    path('delete', views.delete, name='delete'),

    path('<int:pk>/editProfile', views.editProfile, name='editProfile'),
    path('<int:pk>/editPassword', views.editPassword, name='editPassword'),
    path('<int:pk>/edit', views.edit, name='edit'),

    path('search_books', views.search_books, name='search_books'),
    path('catalog/<str:category>', views.catalog, name='catalog'),
    path('item_list', views.item_list, name='item_list'),

    path('update_basket', views.update_basket, name='update-basket'),
    path('basket', views.basket, name='basket'),
    path('submit', views.basket_submit, name='submit'),

    path('creditcard', views.creditcard, name='creditcard'),
    path('editPayment', views.editPayment, name='editPayment'),

    path('purchase', views.show_purchase, name='purchase'),

    path('user_city/', views.user_city, name='user_city'),
    path('map/', views.map, name='map'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

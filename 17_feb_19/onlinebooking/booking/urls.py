from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^home/', views.allview, name='homedetail'),
    url(r'^ticket/', views.ticket_view, name='ticket'),    
    url(r'^traveller_info/', views.traveller_info, name='traveller'),
    url(r'^checkinfo/',views.checkout_new,name='checkout_new'), 
    url(r'^summary/',views.summary_new,name='summary_new'),
    url(r'^payment/',views.summary1_new,name='summary1_new'),  

    
 ] 
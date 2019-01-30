from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^home/', views.allview, name='homedetail'),
    url(r'^ticket/', views.ticket_view, name='ticket'),    
    url(r'^traveller_info/', views.traveller_info, name='traveller'),
    url(r'^api_call/', views.api_call, name='api_call'),  
    url(r'^checkinfo/',views.checkinfodeatil,name='check'),
    url(r'^summarydet/',views.summarydetail,name='sumaryinfo'),
    url(r'^summary1deta/',views.summary1deta,name='summary1info'),     
    url(r'^child_ages/',views.childAges,name='childs'),     


    
 ] 
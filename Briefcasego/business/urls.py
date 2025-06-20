from django.urls import path
from . import views,login,logout,send_contract,respond_contract,notification,announce,download_contract_pdf

urlpatterns = [
    path('', views.index, name='home'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('logout/',logout.logout_view, name='logout'),
    path('login/',login.login_view, name='login'),
    path('send_contract/',send_contract.send_contract_request, name='send_contract'),
    path('announce/',announce.announce, name='announce'),
    path('about/',views.about, name='about'),
    path('contracts/notifications/',notification.contract_notifications, name='contract_notifications'),
    path('contract/respond/<int:contract_id>/',respond_contract.respond_contract, name='respond_contract'),
    path('download_contract/<int:contract_id>/', download_contract_pdf.download_contract_pdf, name='download_contract')

]

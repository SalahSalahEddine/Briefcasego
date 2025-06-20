from django.shortcuts import render,redirect
from .models import Business,ContractRequest,Posts
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import ecdsa
from django.db.models import Q
import os
from django.conf import settings
'''
function to save keys into the path
'''
def save_keys(company_name):
    key_dir = os.path.join(settings.BASE_DIR, 'keys',company_name)
    os.makedirs(key_dir, exist_ok=True)
    public_key_path = os.path.join(key_dir, 'public_key.pem')
    private_key_path = os.path.join(key_dir, 'private_key.pem')
    return public_key_path,private_key_path
def index(request):
    contract = None 
    notification_count = 0
    if 'business_name' in request.session:
        user = Business.objects.filter(company_name=request.session['business_name']).first()
        notification_count = ContractRequest.objects.filter(receiver=user, status='pending').count()
        contract = ContractRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            counterparty_is_paid=True
        ).last()
        #contract = ContractRequest.objects.filter(receiver=user, counterparty_is_paid=True).last()
    if request.method == "POST":
        global company
        company = request.POST['company_name']
        Business.objects.create(
            		company_name=company,
            		email=request.POST['email'],
            		zip_code=request.POST['zip_code'],
            		address=request.POST['address'],
            		number_of_employees=request.POST['number_of_employees'],
            		country=request.POST['country'],
            		city=request.POST['city'],
			password = make_password(request.POST['password']),)
        sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        vk = sk.verifying_key
        public_key_path, private_key_path = save_keys(company)
        with open(public_key_path, 'wb') as pub_file:
            pub_file.write(vk.to_pem())
        with open(private_key_path, 'wb') as priv_file:
            priv_file.write(sk.to_pem())
        request.session['business_name'] = request.POST['company_name']
        return redirect('/')
    return render(request, 'index.html',{'notification_count': notification_count,'contract': contract,'myEmail':user.email})
def newsfeed(request):
    posts = Posts.objects.all()
    return render(request, 'newsfeed.html', {'posts': posts})
def about(request):
    return render(request, 'about.html')


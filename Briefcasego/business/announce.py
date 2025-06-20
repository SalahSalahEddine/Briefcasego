from django.shortcuts import redirect
from django.contrib import messages
from .models import Business,Posts
def announce(request):
    try:
        if request.method == "POST" and 'business_name' in request.session:
            sender = Business.objects.get(company_name=request.session['business_name'])
            memail = sender.email
            Posts.objects.create(
                company_name = sender,
                email = memail,
                contract_type = request.POST['contract_type'],
                conditions = request.POST['conditions']
            )
            messages.success(request, "Contract request sent.")
            return redirect('newsfeed')
    except Business.DoesNotExist:
        sender_email = None
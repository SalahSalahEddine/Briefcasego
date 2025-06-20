from django.shortcuts import render,redirect
from .models import Business,ContractRequest
def contract_notifications(request):
    if 'business_name' in request.session:
        user = Business.objects.get(company_name=request.session['business_name'])
        contracts = ContractRequest.objects.filter(receiver=user, status='pending')

        return render(request, 'notifications.html', {'contracts': contracts})
    return redirect('/')
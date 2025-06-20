from django.contrib.auth.hashers import check_password
from .models import Business
from django.shortcuts import redirect,render
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Business.objects.get(email=email)
            if check_password(password, user.password):
                request.session['business_name'] = user.company_name
                return redirect('/')
            else:
                return render(request, 'index.html', {'login_error': 'Invalid password'})
        except Business.DoesNotExist:
            return render(request, 'index.html', {'login_error': 'User not found'})

    return redirect('/')
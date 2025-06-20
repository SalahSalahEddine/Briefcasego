from django.shortcuts import redirect
# Create your views here.
def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('/')
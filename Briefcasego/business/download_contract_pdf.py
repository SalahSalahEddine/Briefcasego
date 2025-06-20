import os
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden, Http404
from .models import ContractRequest

def download_contract_pdf(request, contract_id):
    try:
        contract = ContractRequest.objects.get(id=contract_id)
    except ContractRequest.DoesNotExist:
        raise Http404("Contract not found.")

    if not contract.counterparty_is_paid:
        return HttpResponseForbidden("Payment required.")

    user_company = request.session.get('business_name')

    if contract.sender.company_name != user_company and contract.receiver.company_name != user_company:
        return HttpResponseForbidden("Unauthorized access.")

    # Track download
    if contract.sender.company_name == user_company:
        contract.sender_downloaded = True
    elif contract.receiver.company_name == user_company:
        contract.receiver_downloaded = True

    delete_after = False
    if contract.sender_downloaded and contract.receiver_downloaded:
        delete_after = True
        contract.counterparty_is_paid = False

    contract.save()

    filename = f"{contract.sender.company_name}_{contract.receiver.company_name}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, 'contracts', filename)

    if not os.path.exists(filepath):
        raise Http404("Contract PDF not found.")

    # Open file before deletion
    response = FileResponse(open(filepath, 'rb'), content_type='application/pdf', as_attachment=True, filename=filename)

    if delete_after:
        try:
            os.remove(filepath)
        except OSError:
            pass 

    return response


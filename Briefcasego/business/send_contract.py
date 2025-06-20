from django.contrib import messages
from .models import Business,ContractRequest
from dateutil.relativedelta import relativedelta
import base64
from datetime import date
import json
import os
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
from ecdsa import SigningKey

#private key
def private_key(company_name):
    key_dir = os.path.join(settings.BASE_DIR, 'keys',company_name)
    os.makedirs(key_dir, exist_ok=True)
    private_key_path = os.path.join(key_dir, 'private_key.pem')
    with open(private_key_path, "rb") as f:
        sk = SigningKey.from_pem(f.read())
    return sk

#interest rate swaps payment_frequency
def calculate_payment_frequency_IRS(duration_key):
    payment_frequency_IRS = {
        "3months": relativedelta(months=3),
        "6months": relativedelta(months=6),
        "1year": relativedelta(years=1),
        "3year": relativedelta(years=3),
        "5year": relativedelta(years=5)
    }
    return date.today() + payment_frequency_IRS.get(duration_key, relativedelta())
def send_contract_request(request):
     if request.method == "POST" and 'business_name' in request.session:
        sender = Business.objects.get(company_name=request.session['business_name'])
        try:
             receiver = Business.objects.filter(email=request.POST['email']).first()
             cds_file = request.FILES.get('cds_bonds')
             if cds_file:
                  if not cds_file.name.endswith('.pdf'):
                       return HttpResponse("Only PDF files are allowed.")
        except Business.DoesNotExist:
              messages.error(request, "Receiver not found")
              return redirect('/')
        email = request.POST['email']
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        contract_type = request.POST['contract_type']
        sofr = request.POST.get('sofr_input')
        spread = request.POST.get('spread_input')
        interest_rate_type = request.POST.get('rate_type')
        treasury_bond_yield_or_coast_of_funds = request.POST.get('Treasury_bond_yield_Coast_of_Fund')
        payment_frequency = calculate_payment_frequency_IRS(request.POST.get('payment_frequency'))
        Reference_Entity = request.POST.get('reference_entity')
        credit_event = request.POST.get('credit_event')
        bond_or_proof = request.FILES.get('cds_bonds')
        underlying_asset = request.POST.get('underlying_asset')
        strike_price = request.POST.get('strike_price')
        expiration_date = request.POST.get('expiration_date')
        option_type = request.POST.get('option_type')
        third_part = request.POST.get('third_part')
        settelment_type = request.POST.get('settelment_type')
        quantity = request.POST.get('quantity')
        forward_price = request.POST.get('forward_price')
        national_amount = request.POST.get('national_amount')
        #to_json
        data = {
            "sender": str(sender),
            "receiver": str(receiver),
            "email": str(email),
            "price": price,
            "duration": str(duration),
            "contract_type": contract_type,
            "sofr": sofr,
            "spread": spread,
            "interest_rate_type": interest_rate_type,
            "treasury_bond_yield_or_coast_of_funds": treasury_bond_yield_or_coast_of_funds,
            "payment_frequency": str(payment_frequency),
            "Reference_Entity": Reference_Entity,
            "credit_event": credit_event,
            "underlying_asset": underlying_asset,
            "strike_price": strike_price,
            "expiration_date": str(expiration_date),
            "option_type": option_type,
            "third_part": third_part,
            "settelment_type": settelment_type,
            "quantity": quantity,
            "forward_price": forward_price,
            "national_amount": national_amount,
        }
        prv = private_key(sender.company_name)
        message = json.dumps(data, sort_keys=True).encode()
        signature = prv.sign(message)
        signature_b64 = base64.b64encode(signature).decode()
        ContractRequest.objects.create(
            sender=sender,
            receiver=receiver,
            email=email,
            price=price,
            duration=duration,
            contract_type=contract_type,
            sofr = sofr,
            spread = spread,
            interest_rate_type = interest_rate_type,
            treasury_bond_yield_or_coast_of_funds = treasury_bond_yield_or_coast_of_funds,
            payment_frequency = payment_frequency,
            Reference_Entity = Reference_Entity,
            credit_event = credit_event,
            bond_or_proof = bond_or_proof,
            underlying_asset = underlying_asset,
            strike_price = strike_price,
            expiration_date = expiration_date,
            option_type = option_type,
            third_part =third_part,
            settelment_type = settelment_type,
            quantity = quantity,
            forward_price = forward_price,
            national_amount = national_amount,
            sender_signature = signature_b64
            ),
        messages.success(request, "Contract request sent.")
        return redirect('/')
from django.shortcuts import redirect
from .models import ContractRequest
from django.conf import settings
from .upload import upload_to_lighthouse
from dotenv import load_dotenv
from ecdsa import SigningKey
import os
from .generate_pdf import generate_isda_confirmation
import json
import base64


load_dotenv()
ipfs_api_key = os.getenv("ipfs_api_key")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
#private key
def private_key(company_name):
    key_dir = os.path.join(settings.BASE_DIR, 'keys',company_name)
    os.makedirs(key_dir, exist_ok=True)
    private_key_path = os.path.join(key_dir, 'private_key.pem')
    with open(private_key_path, "rb") as f:
        sk = SigningKey.from_pem(f.read())
    return sk
#Function to make counterparty pay
def is_pay(contract):
    contract.counterparty_is_paid = True
    contract.save()
    return contract.counterparty_is_paid
def respond_contract(request, contract_id):
    if request.method == "POST" and 'business_name' in request.session:
        try:
            contract = ContractRequest.objects.get(id=contract_id)
            if contract.receiver.company_name != request.session['business_name']:
                return redirect('contract_notifications')

            action = request.POST.get('action')

            if action == 'reject':
                if contract.bond_or_proof and contract.bond_or_proof.storage.exists(contract.bond_or_proof.name):
                    contract.bond_or_proof.delete(save=False)
                contract.delete()

            elif action == 'accept':
                contract.status = 'accepted'
                recepient = {
                     "sender": str(contract.sender.company_name),
                     "receiver": str(contract.receiver.company_name),
                     "email": str(contract.email),
                     "price": float(contract.price) if contract.price else 0,
                     "duration": str(contract.duration),
                     "contract_type": contract.contract_type,
                     "sofr": float(contract.sofr) if contract.sofr else 0,
                     "spread": float(contract.spread) if contract.spread else 0,
                     "interest_rate_type": contract.interest_rate_type,
                     "treasury_bond_yield_or_coast_of_funds": float(contract.treasury_bond_yield_or_coast_of_funds)if contract.treasury_bond_yield_or_coast_of_funds else 0 ,
                     "payment_frequency": str(contract.payment_frequency),
                     "Reference_Entity": contract.Reference_Entity,
                     "credit_event": contract.credit_event,
                     "underlying_asset": contract.underlying_asset,
                     "strike_price": float(contract.strike_price) if contract.strike_price else 0,
                     "expiration_date": str(contract.expiration_date),
                     "option_type": contract.option_type,
                     "third_part": contract.third_part,
                     "settelment_type": contract.settelment_type,
                     "quantity": float(contract.quantity) if contract.quantity else 0,
                     "forward_price": float(contract.forward_price) if contract.forward_price else 0,
                     "national_amount": float(contract.national_amount) if contract.national_amount else 0,
                }
                try:
                    pdf_path = os.path.join(MEDIA_DIR,'contracts',f"{contract.sender.company_name}_{contract.receiver.company_name}.pdf")
                    prv = private_key(contract.receiver.company_name)
                    message = json.dumps(recepient, sort_keys=True).encode()
                    signature = prv.sign(message)
                    signature_b64 = base64.b64encode(signature).decode()
                    if signature_b64:
                        contract.receiver_signature = signature_b64
                        #generate pdf contract
                        generate_isda_confirmation(contract, contract.sender.company_name, contract.receiver.company_name)
                        if is_pay(contract):
                            #upload contract pdf file to ipfs
                            cid = upload_to_lighthouse(pdf_path, ipfs_api_key)
                            if cid:
                                contract.ipfs_cid = cid

                except Exception as e:
                    print("PDF Generation Failed:", e)
                contract.save()

        except ContractRequest.DoesNotExist:
            pass

    return redirect('contract_notifications')

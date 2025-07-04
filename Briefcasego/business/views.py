def index(request):
    contract = None 
    notification_count = 0
    user = None  # ← تجنب خطأ UnboundLocalError

    if 'business_name' in request.session:
        user = Business.objects.filter(company_name=request.session['business_name']).first()
        if user:
            notification_count = ContractRequest.objects.filter(receiver=user, status='pending').count()
            contract = ContractRequest.objects.filter(
                Q(sender=user) | Q(receiver=user),
                counterparty_is_paid=True
            ).last()

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
            password=make_password(request.POST['password']),
        )
        sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        vk = sk.verifying_key
        public_key_path, private_key_path = save_keys(company)
        with open(public_key_path, 'wb') as pub_file:
            pub_file.write(vk.to_pem())
        with open(private_key_path, 'wb') as priv_file:
            priv_file.write(sk.to_pem())
        request.session['business_name'] = company
        return redirect('/')

    return render(request, 'index.html', {
        'notification_count': notification_count,
        'contract': contract,
        'myEmail': user.email if user else None  # ← تأكد أن user ليس None
    })

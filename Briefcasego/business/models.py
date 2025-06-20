from django.db import models
import datetime

today = datetime.datetime.now()
# Create your models here.
class Business(models.Model):
    company_name = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=10)
    address = models.TextField()
    number_of_employees = models.IntegerField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.company_name
class ContractRequest(models.Model):
    CONTRACT_TYPES = [
        ('forward', 'Forward'),
        ('future', 'Future'),
        ('interest rate swaps', 'Interest Rate Swaps'),
        ('credit default swaps', 'Credit Default Swaps'),
        ('naked cds', 'Naked CDS'),
        ('option_call','Option_Call')
    ]
    DURATION_CHOICES = [
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('1_5_years', '1.5 Years'),
        ('2_years', '2 Years'),
        ('5_years', '5 Years'),
    ]
    INTEREST_RATE_TYPE = [
         ('fixed', 'Fixed'),
          ('float', 'Float')
    ]
    CREDIT_EVENT = [
        ('failure to pay','Failure to Pay'),
        ('restructuring','Restructuring'),
        ('bankruptcy','Bankruptcy')
    ]
    OPTION_TYPE = [
        ('american','American'),
        ('european','European'),
        ('asian','Asian'),
    ]
    THIRD_PART = [
        ('yes','YES'),
         ('no','NO')
    ]
    SETELMENT_TYPE = [
        ('physical','Physical'),
        ('cash','Cash')
    ]
    sender = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='sent_contracts')
    sender_signature = models.CharField(max_length=20,null=True)
    receiver = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='received_contracts')
    receiver_signature = models.CharField(max_length=20,null=True)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=20,null=True)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES,default='3_months')
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPES)
    interest_rate_type = models.CharField(max_length=30, choices=INTEREST_RATE_TYPE,null=True)
    payment_frequency = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    Reference_Entity = models.CharField(max_length=20,null=True)
    margin = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    sofr = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    spread = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    treasury_bond_yield_or_coast_of_funds = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    credit_event = models.CharField(max_length=20,choices=CREDIT_EVENT,null=True)
    bond_or_proof = models.FileField(upload_to='uploads/',default='file')
    underlying_asset = models.CharField(max_length=20,null=True)
    strike_price = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    expiration_date =  models.DateField(null=True, blank=True)
    option_type = models.CharField(max_length=30, choices=OPTION_TYPE,null=True)
    third_part = models.CharField(max_length=30, choices=THIRD_PART,null=True)
    settelment_type = models.CharField(max_length=30, choices=SETELMENT_TYPE,null=True)
    quantity =  models.DecimalField(max_digits=10,decimal_places=2,null=True)
    forward_price = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    national_amount = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    counterparty_is_paid = models.BooleanField(default=False)
    ipfs_cid = models.CharField(max_length=100, blank=True, null=True)
    sender_downloaded = models.BooleanField(default=False)
    receiver_downloaded = models.BooleanField(default=False)
    



    def __str__(self):
        return f"{self.sender} → {self.receiver} [{self.contract_type}]"
    
class Posts(models.Model):
    CONTRACT_TYPES = [
        ('forward', 'Forward'),
        ('future', 'Future'),
        ('interest rate swaps', 'Interest Rate Swaps'),
        ('credit default swaps', 'Credit Default Swaps'),
        ('naked cds', 'Naked CDS')
    ]
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPES)
    email = models.EmailField()
    company_name = models.CharField(max_length=100,default='company')
    conditions = models.TextField(max_length=800,default='no_conditions')

    def __str__(self):
        return f"{self.company_name} → {self.email} [{self.conditions}]"

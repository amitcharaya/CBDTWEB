from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django import forms
from django.forms import ModelForm
from .models import Header,Records
from django.forms import BaseFormSet

class UploadFileForm(forms.Form):

    file = forms.FileField()

class ResponseFileForm(forms.Form):
    filename=forms.CharField(widget=forms.HiddenInput())
    headerIdentifier = forms.CharField(widget=forms.HiddenInput(),max_length=2,label='Header Identifier')
    orignatorCode = forms.CharField(widget=forms.HiddenInput(),max_length=11,label="Orignator Code")
    responderCode = forms.CharField(widget=forms.HiddenInput(),max_length=11,label="Responder Code")
    fileRefernceNo = forms.CharField(widget=forms.HiddenInput(),max_length=10,label="File Ref. No.")
    totalNoOfRecords = forms.CharField(widget=forms.HiddenInput(),max_length=6,label="Total Records")

AccountActiveFlags =(
    ("00", "Active"),
    ("01", "Account Closed"),
    ("02", "No Such Account"),
    ("51", "KYC Documents Pending"),
    ("52", "Documents Pending for Account Holder turning Major"),
    ("53", "Account inoperative"),
    ("54", "Dormant A/c"),
    ("55", "A/c in Zero Balance/No Transactions have Happened, First Transaction in Cash or Self Cheque"),
    ("60", "Account Holder Expired"),
    ("62", "Account Under Litigation"),
    ("65", "Account Holder Name Invalid"),
    ("68", "A/c Blocked or Frozen"),
    ("69", "Customer Insolvent / Insane"),

)
JointAccountFlags=(
    ("00","Joint Account"),
    ("01","Individual Account"),
)

AccountTypes=(
    ("SB","Saving Bank Accounts"),
    ("CA","Current Accounts"),
    ("CC","Cash Credit Accounts"),
    ("OD","Over Draft Accounts"),
    ("TD","Term Deposit Accounts"),
    ("LN","Loan Accounts"),
    ("SG","State Government Account"),
    ("CG","Central Government Account"),
    ("OT","Others"),
    ("NR","Non- Resident Account"),
    ("PP","Public Provident Fund Account"),
    ("NO","NRO account"),
)


class ResponseFileRecordsForm(forms.Form):
    recordIdentifer = forms.CharField(widget=forms.HiddenInput(),max_length=2,label="Record Identifier",required=False)
    recordIdentifer.widget.attrs.update(size='2')
    recordRefernceNo = forms.CharField(widget=forms.HiddenInput(),max_length=15,label="Refernce No",required=False)
    recordRefernceNo.widget.attrs.update(size='15')
    ifscCode = forms.CharField(max_length=11,label="IFSC Code",required=False)
    ifscCode.widget.attrs.update(size='11')
    destinationBankAccountNo = forms.CharField(max_length=35,label="Destination Bank Account No",required=False)
    accountValidFlag = forms.ChoiceField(choices=AccountActiveFlags, label="Active Validation Flag")

    jointAccountFlag = forms.ChoiceField(choices=JointAccountFlags, label="Joint Account Flag")
    primaryPan = forms.CharField(max_length=10,label="Primary Person PAN",required=False)
    primaryPan.widget.attrs.update(size='10')
    secondaryPan = forms.CharField(max_length=10,label="Secondary Person PAN",required=False)
    primaryAccountHolderName = forms.CharField(max_length=50,label="Primary Account Holder Name",required=False)
    secondaryAccountHolderName = forms.CharField(max_length=50,label="Secondary Account Holder Name",required=False)
    accountType = forms.ChoiceField(choices=AccountTypes, label="Account Type",required=False)

    def clean(self):
        jointAccountFlag = self.cleaned_data.get('jointAccountFlag')

        secondaryAccountHolderName = self.cleaned_data.get('secondaryAccountHolderName')
        print("in validations")
        print(jointAccountFlag)
        if jointAccountFlag == "00" and not secondaryAccountHolderName :
            raise ValidationError({'secondaryAccountHolderName': ["This Filed is required",]})








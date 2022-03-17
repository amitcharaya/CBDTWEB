from django.db import models
from django_cryptography.fields import encrypt
# Create your models here.
class Header(models.Model):
    filename=encrypt(models.CharField(max_length=100))
    headerIdentifier=encrypt(models.CharField(max_length=2))
    orignatorCode=encrypt(models.CharField(max_length=11))
    responderCode=encrypt(models.CharField(max_length=11))
    fileRefernceNo=encrypt(models.CharField(max_length=10))
    totalNoOfRecords=encrypt(models.CharField(max_length=6))
    def __str__(self):
        return self.filename

class Records(models.Model):
    header=models.ForeignKey(Header,on_delete=models.CASCADE)
    recordIdentifer=encrypt(models.CharField(max_length=2))
    recordRefernceNo=encrypt(models.CharField(max_length=15))
    ifscCode=encrypt(models.CharField(max_length=11))
    destinationBankAccountNo=encrypt(models.CharField(max_length=35))
    accountValidFlag=encrypt(models.CharField(max_length=2))
    jointAccountFlag=encrypt(models.CharField(max_length=2))
    primaryPan=encrypt(models.CharField(max_length=10))
    secondaryPan=encrypt(models.CharField(max_length=10))
    primaryAccountHolderName=encrypt(models.CharField(max_length=50))
    secondaryAccountHolderName=encrypt(models.CharField(max_length=50))
    accountType=encrypt(models.CharField(max_length=2))

    def __str__(self):
        return self.header.filename + " " +self.recordRefernceNo

from django.db import models

# Create your models here.
class Header(models.Model):
    filename=models.CharField(max_length=100)
    headerIdentifier=models.CharField(max_length=2)
    orignatorCode=models.CharField(max_length=11)
    responderCode=models.CharField(max_length=11)
    fileRefernceNo=models.CharField(max_length=10)
    totalNoOfRecords=models.CharField(max_length=6)
    def __str__(self):
        return self.filename

class Records(models.Model):
    header=models.ForeignKey(Header,on_delete=models.CASCADE)
    recordIdentifer=models.CharField(max_length=2)
    recordRefernceNo=models.CharField(max_length=15)
    ifscCode=models.CharField(max_length=11)
    destinationBankAccountNo=models.CharField(max_length=35)
    accountValidFlag=models.CharField(max_length=2)
    jointAccountFlag=models.CharField(max_length=2)
    primaryPan=models.CharField(max_length=10)
    secondaryPan=models.CharField(max_length=10)
    primaryAccountHolderName=models.CharField(max_length=50)
    secondaryAccountHolderName=models.CharField(max_length=50)
    accountType=models.CharField(max_length=2)

    def __str__(self):
        return self.header.filename + " " +self.recordRefernceNo

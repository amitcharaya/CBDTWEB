
from django.shortcuts import redirect
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from pathlib import Path
# Create your views here.
from cbdtapp.forms import UploadFileForm,ResponseFileForm,ResponseFileRecordsForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django import  forms as fo
from .models import Header,Records
@login_required
def home(request):
    return render(request, 'home.html')


def generateResponse(request):
    # cretae response file when user hits submit in respnose form
    ResponseFileRecordsFormFormset=formset_factory(ResponseFileRecordsForm)

    if request.method == 'POST':
        formset = ResponseFileRecordsFormFormset(request.POST)
        form=ResponseFileForm(request.POST)
        if formset.is_valid() and form.is_valid():

            # do something with the formset.cleaned_data
            filename=form.cleaned_data.get('filename')
            f = open('static/outward/'+filename, 'wb+')

            headerIdentifier=form.cleaned_data.get('headerIdentifier')
            if len(headerIdentifier)==2:
                f.write(bytes(headerIdentifier,'utf-8'))
            orignatorCode=form.cleaned_data.get('orignatorCode')
            if len(orignatorCode)==11:
                f.write(bytes(orignatorCode,'utf-8'))
            else:
                noOfSpaceToAppend=11-len(orignatorCode)
                spaces=" "*noOfSpaceToAppend
                orignatorCode=orignatorCode+spaces
                f.write(bytes(orignatorCode, 'utf-8'))


            responderCode=form.cleaned_data.get('responderCode')
            if len(responderCode)==11:
                f.write(bytes(responderCode,'utf-8'))
            else:
                noOfSpaceToAppend=11-len(responderCode)
                spaces=" "*noOfSpaceToAppend
                responderCode=responderCode+spaces
                f.write(bytes(responderCode, 'utf-8'))

            fileRefernceNo=form.cleaned_data.get('fileRefernceNo')
            if len(fileRefernceNo)==10:
                f.write(bytes(fileRefernceNo,'utf-8'))

            totalNoOfRecords = form.cleaned_data.get('totalNoOfRecords')
            if len(totalNoOfRecords) == 6:
                f.write(bytes(totalNoOfRecords,'utf-8'))
            header=Header(filename=filename,headerIdentifier=headerIdentifier,orignatorCode=orignatorCode,responderCode=responderCode,fileRefernceNo=fileRefernceNo,totalNoOfRecords=totalNoOfRecords)
            header.save()
            filler=" "*460
            f.write(bytes(filler,'utf-8'))
            f.write(bytes('\n','utf-8'))
            # header completed

            for form in formset:
                recordIdentifer=form.cleaned_data.get('recordIdentifer')
                if len(recordIdentifer)==2:
                    f.write(bytes(recordIdentifer, 'utf-8'))

                recordRefernceNo = form.cleaned_data.get('recordRefernceNo')
                if len(recordRefernceNo) == 15:
                    f.write(bytes(recordRefernceNo, 'utf-8'))
                else:
                    noOfSpaceToAppend = 15 - len(recordRefernceNo)
                    spaces = " " * noOfSpaceToAppend
                    recordRefernceNo = recordRefernceNo + spaces
                    f.write(bytes(recordRefernceNo, 'utf-8'))

                ifscCode = form.cleaned_data.get('ifscCode')
                if len(ifscCode) == 11:
                    f.write(bytes(ifscCode, 'utf-8'))

                destinationBankAccountNo = form.cleaned_data.get('destinationBankAccountNo')
                if len(destinationBankAccountNo) == 35:
                    f.write(bytes(destinationBankAccountNo, 'utf-8'))
                else:
                    noOfSpaceToAppend = 35 - len(destinationBankAccountNo)
                    spaces = " " * noOfSpaceToAppend
                    destinationBankAccountNo = destinationBankAccountNo + spaces
                    f.write(bytes(destinationBankAccountNo, 'utf-8'))

                accountValidFlag = form.cleaned_data.get('accountValidFlag')
                if len(accountValidFlag) == 2:
                    f.write(bytes(accountValidFlag, 'utf-8'))
                    # if account is closed skip remaining fileds
                if accountValidFlag=="02":
                    filler = " " * 435
                    f.write(bytes(filler, 'utf-8'))
                    f.write(bytes('\n', 'utf-8'))
                    record = Records(header=header, recordIdentifer=recordIdentifer, recordRefernceNo=recordRefernceNo,
                                     ifscCode=ifscCode, destinationBankAccountNo=destinationBankAccountNo,
                                     accountValidFlag=accountValidFlag, jointAccountFlag="  ",
                                     primaryPan="          ", secondaryPan="          ",
                                     primaryAccountHolderName="                                                  ",
                                     secondaryAccountHolderName="                                                  ", accountType="  ")
                    record.save()
                else:
                    jointAccountFlag = form.cleaned_data.get('jointAccountFlag')
                    primaryAccountHolderName = form.cleaned_data.get('primaryAccountHolderName')
                    secondaryAccountHolderName = form.cleaned_data.get('secondaryAccountHolderName')

                    if len(jointAccountFlag) == 2:
                        f.write(bytes(jointAccountFlag, 'utf-8'))
                    primaryPan = form.cleaned_data.get('primaryPan')
                    if len(primaryPan) == 10:
                        f.write(bytes(primaryPan, 'utf-8'))
                    else:
                        filler = " " * 10
                        f.write(bytes(filler, 'utf-8'))


                    secondaryPan = form.cleaned_data.get('secondaryPan')
                    if len(secondaryPan) == 10:
                        f.write(bytes(secondaryPan, 'utf-8'))
                    else:
                        filler = " " * 10
                        f.write(bytes(filler, 'utf-8'))


                    if len(primaryAccountHolderName) == 50:
                        f.write(bytes(primaryAccountHolderName, 'utf-8'))
                    else:
                        noOfSpaceToAppend = 50 - len(primaryAccountHolderName)
                        spaces = " " * noOfSpaceToAppend
                        primaryAccountHolderName = primaryAccountHolderName + spaces
                        f.write(bytes(primaryAccountHolderName, 'utf-8'))


                    if len(secondaryAccountHolderName) == 50:
                        f.write(bytes(secondaryAccountHolderName, 'utf-8'))
                    else:
                        noOfSpaceToAppend = 50 - len(secondaryAccountHolderName)
                        spaces = " " * noOfSpaceToAppend
                        secondaryAccountHolderName = secondaryAccountHolderName + spaces
                        f.write(bytes(secondaryAccountHolderName, 'utf-8'))
                    accountType = form.cleaned_data.get('accountType')
                    if len(accountType) == 2:
                        f.write(bytes(accountType, 'utf-8'))
                    else:
                        filler = " " * 2
                        f.write(bytes(filler, 'utf-8'))
                    filler=" "*311
                    f.write(bytes(filler, 'utf-8'))
                    f.write(bytes('\n', 'utf-8'))
                    record=Records(header=header,recordIdentifer=recordIdentifer,recordRefernceNo=recordRefernceNo,ifscCode=ifscCode,destinationBankAccountNo=destinationBankAccountNo,accountValidFlag=accountValidFlag,jointAccountFlag=jointAccountFlag,primaryPan=primaryPan,secondaryPan=secondaryPan,primaryAccountHolderName=primaryAccountHolderName,secondaryAccountHolderName=secondaryAccountHolderName,accountType=accountType)
                    record.save()

            f.close()
            print(formset.cleaned_data)
            print(form.cleaned_data)
            redirect('home')
        else:
            print(formset.errors)
            formset = ResponseFileRecordsFormFormset(request.POST)
            form = ResponseFileForm(request.POST)
            return render(request, 'cbdtapp/Response.html', {'form': form, 'formset': formset})

    return render(request, 'cbdtapp/uploadfile.html')
@login_required
def upload_file(request):
    # take text file and load it intp forms using form ResponseFileForm and ResponseFileRecordsForm Form set
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            context=handle_uploaded_file(request.FILES['file'],request)
            header=context.get('header')
            print(header)
            records=context.get('records')
            fo=ResponseFileForm(
                initial={'headerIdentifier': header.get('identifier'), 'orignatorCode': header.get('orignatorCode'), 'responderCode': header.get('responderCode'),
                         'fileRefernceNo': header.get('fileRefernceNo'), 'totalNoOfRecords': header.get('totalNoOfRecords'),'filename':header.get('filename').replace('CBDTUser',str(request.user))})

            ResponseFileRecordsFormFormset=formset_factory(ResponseFileRecordsForm,extra=int(header.get('totalNoOfRecords')))
            formset=ResponseFileRecordsFormFormset()

            count=0
            for form in formset:
                record=records[count]
                form.initial['recordIdentifer']=record.get('identifier')
                form.initial['recordRefernceNo'] = record.get('recordRefrenceNo')
                form.initial['ifscCode'] = record.get('ifscCode')
                form.initial['destinationBankAccountNo'] = record.get('bankAccountNo')
                count=count+1
            return render(request, 'cbdtapp/Response.html', {'form': fo,'formset':formset})
        else:
            return HttpResponse("error")
    else:

        form = UploadFileForm()
        return render(request, 'cbdtapp/uploadfile.html', {'form': form})

def handle_uploaded_file(f,request):
    with open('static/inward/'+f.name, 'wb+') as destination:

        for chunk in f.chunks():
            destination.write(chunk)

    #take file and return context
    context={}
    records = []
    header={}
    # read input file
    f = open('static/inward/'+f.name, 'r')
    if f.mode == 'r':
        Lines = f.readlines()
        count = 0


        for line in Lines:
            # read lines from file

            identifier=line[:2]

            if identifier=="30":
                # if header record
                orignatorCode = line[2:13]
                responderCode = line[13:24]
                fileRefernceNo = line[24:34]
                totalNoOfRecords = line[34:40]
                FILENAME=Path(f.name).stem
                FILENAME=FILENAME[:-3]+"RES.txt"
                header={'identifier':identifier,'orignatorCode':orignatorCode,'responderCode':responderCode,'fileRefernceNo':fileRefernceNo,'totalNoOfRecords':totalNoOfRecords,'filename':FILENAME}
            if identifier=="70":
                # if it is a record
                recordRefrenceNo=line[2:17]
                ifscCode=line[17:28]
                bankAccountNo=line[28:63]
                records.append({'identifier':identifier,'recordRefrenceNo':recordRefrenceNo,'ifscCode':ifscCode,'bankAccountNo':bankAccountNo})
        # set the context
        context={'header':header,'records':records}
    return context




@login_required
def logoutuser(request):
    logout(request)
    return redirect('login')


def loginpage(request):


    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            messages.error(request, 'Username or password incorrect')

    context = {}
    return render(request, 'cbdtapp/login.html', context)

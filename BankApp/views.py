from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,RequesterForm,DonnerForm
from django.contrib.auth import login
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
from .models import Banks, Blood, RequesterModel , DonnerModel ,RequestedBlood
import string
import random

#name@#0123

def index(request):
    return HttpResponse("Hello, world. Site is under Cunstruction")
    
def home(request):
    return render(request,'home.html')
    
def GetSecret():
	return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 7))

def register(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = UserRegistrationForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})    

def Donner(request):
	if request.method == "POST":
		form = DonnerForm(request.POST)			
		if form.is_valid():
			form.save()
			messages.success(request, "Registration successful." )
			B=Blood(BloodGrp=request.POST['BloodGrp'],
					Bid_id=request.POST['Bid'],
					Did=request.user,
					Secret=GetSecret(),
					is_available=True)
			B.save()	
			return render(request,'home.html',context={"text":"Thank You for Donation"})
		messages.error(request, "Unsuccessful registration. Invalid information.")
	donner1 = DonnerModel.objects.filter(Did_id=request.user.id)
	if len(donner1) == 1:
		if donner1[0].Did_id==request.user.id:	
			print("\n\n",donner1[0].BloodGrp,"  ",)
			B=Blood(BloodGrp=donner1[0].BloodGrp,
					Bid=donner1[0].Bid,
					Did=request.user,
					Secret=GetSecret(),
					is_available=True)
			B.save()	
			return render(request,'home.html',context={"text":"Thank You for Donation"})	
		
	form = DonnerForm()
	return render (request=request, template_name="Donner.html", context={"register_form":form,"isShow":False})    


def Requester(request):
	request.session['Bloodgrp'] = ""	
	if request.method == "POST":
		form = RequesterForm(request.POST)			
		if form.is_valid():
			form.save()
			messages.success(request, "Registration successful." )
			request.session['Bloodgrp'] = request.POST['BloodGrp']
			print("dgn done1")
			return redirect("RequesterBloodIsAvailable")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	req1=RequesterModel.objects.filter(Rid=request.user)	
	if len(req1) == 1:	
		return redirect("RequesterBloodIsAvailable")	
	form = RequesterForm()
	return render (request=request, template_name="Requester.html", context={"register_form":form,"isShow":False})    


# make condition if blood is not present

def RequesterBloodIsAvailable(request):
	print("dgn done2")
	if request.method == "POST":
		print("dgn done3")
		DonnerList = Blood.objects.filter(BloodGrp=request.POST['BloodGrp'],is_available=1)
		if len(DonnerList)>0:
			print("dgn done4")
			#now just give the first blood but after add date and give oldest blood
			print(DonnerList[0].Bid.id,"  ",type(DonnerList[0].Bid),"  ",str(DonnerList[0].Bid))
			BankDetails = Banks.objects.get(id=DonnerList[0].Bid.id) 
			
			DonnerData = [DonnerList[0].BloodGrp,BankDetails.Bcity,BankDetails.BState]
			#add here a data on which date blood will given.
			ReqObj = RequestedBlood(Dnid=DonnerList[0].Did.id,
									Bid=BankDetails,
									Rqid=request.user,
									Secret=GetSecret(),
									Bloodid=DonnerList[0])
			ReqObj.save()
			print("\n\n",DonnerList[0].BloodGrp,"   ",BankDetails.Bcity,"   ",BankDetails.BState,"\n\n")
			BloodD = Blood.objects.get(id=DonnerList[0].id)
			BloodD.is_available = False
			BloodD.save()
			return render (request=request, template_name="RequesterForBlood.html", context={"DonnerData":DonnerData,"is_data":True})			
	return render (request=request, template_name="RequesterForBlood.html", context={"BloodGrp":request.session['Bloodgrp'],"is_show":True})

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from services.models import Service
from nodes.models import LoRaNode
from gateways.models import Gateway

# Create your views here.
@login_required
def index(request):
	template = "index.html"
	user = request.user.username
	service_num = len(Service.objects.all())
	gateway_num = len(Gateway.objects.all())
	node_num = len(LoRaNode.objects.all())

	print(service_num, gateway_num, node_num)
	context = {
			"user": user,
			"service_num": service_num,
			"gateway_num": gateway_num,
			"node_num": node_num

	}
	return render(request, template, context)

def signup(request):
	if request.method == "POST":
		# username = request.POST["username"]
		# password1 = request.POST["password1"]
		# password2 = request.POST["password2"]
		email = request.POST["email"]

		form = UserCreationForm(request.POST)

		if form.is_valid():
			print(form.cleaned_data)
			user = User.objects.create_user(form.cleaned_data['username'], email, form.cleaned_data['password1'])
			user.save()
			login(request, user)

			return HttpResponseRedirect("/")

		else:
			print("bad form")
			template = "registration/signup.html"
			return render(request, template, {"form":form})	
	
	else:
		template = "registration/signup.html"
		return render(request, template, {})	


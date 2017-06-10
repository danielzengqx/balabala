from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
	template = "gateway_index.html"
	context = {


	}
	return render(request, template, context)
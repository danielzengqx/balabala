from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
	template = "index.html"
	context = {


	}
	return render(request, template, context)
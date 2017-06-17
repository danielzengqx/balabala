from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
	template = "service_index.html"
	context = {

	}
	return render(request, template, context)

def add_service(request):
    template = "service_add.html"
    context = {

    }
    return render(request, template, context)
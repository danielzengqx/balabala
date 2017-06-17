from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
	template = "service_index.html"
	context = {

	}
	return render(request, template, context)

def service_add(request):
    template = "service_add.html"
    context = {

    }
    return render(request, template, context)

def service_detail(request):
    template = "service_detail.html"
    context = {

    }
    return render(request, template, context)
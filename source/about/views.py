from django.shortcuts import render

# Create your views here.
def about_us(request):
    return render(request, "about.html")

def about_gavin(request):
    return render(request, "gavin.html")

def about_jocelyn(request):
    return render(request, "jocelyn.html")

def about_swapnil(request):
    return render(request, "swapnil.html")

def about_thomas(request):
    return render(request, "thomas.html")

def about_paloma(request):
    return render(request, "paloma.html")

def about_template(request):
    return render(request, "bio-template.html")

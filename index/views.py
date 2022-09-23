from django.shortcuts import render

# Create your views here.
from blueapps.account.decorators import login_exempt


@login_exempt
def vue(request):
    return render(request, 'index.html')
    # SITE_URL = "http://127.0.0.1:8000"
    # return render(request, 'index.html', {"SITE_URL": SITE_URL})

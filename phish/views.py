import requests
from .models import Tested_URLs
from django.template import loader
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .classifier.vectorizer import vectorize
from .classifier.classifier_vector import classify



def index(request):
    template = loader.get_template('phish/index.html')
    return HttpResponse(template.render(request=request))

def verify(request):
    if request.method == "POST":
        ip =request.META.get('HTTP_X_FORWARDED_FOR')or request.META.get('REMOTE_ADDR')
        print(ip)
        print(request.META.get('HTTP_X_FORWARDED_FOR'))
        print(request.META.get('REMOTE_ADDR'))
        url = request.POST['url']
        print(url)
        url = url.strip(' \t\n\r')
        try:
            requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}, timeout=60, verify=False)
        except:
            context = {
                'inaccessible_url': "Inaccessible url nigga"
            }
            return render(request, 'phish/index.html', context)
        list = vectorize(url)
        print(list)
        result = classify(list)
        print(result)
        obj = Tested_URLs(url=url, phishing=result)
        obj.save()
        if result:
            context = {
                 'phish_pos': "its a phish nigga, back the fuck off"
            }
        else :
            context = {
                'phish_neg': "its not a phish nigga, go a head"
            }
        return render(request, 'phish/index.html', context)
    else :
        redirect('phish/index.html')

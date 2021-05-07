import requests
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader

from .classifier.classifier_vector import classify
from .classifier.vectorizer import vectorize
from .fusioncharts import FusionCharts
from .models import REVIEWS
from .models import URL


def form(request):
    template = loader.get_template('phish/form.html')
    return HttpResponse(template.render(request=request))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    if request.method == "POST":
        list_rate = request.POST.getlist('rate')
        # print("this is the rate")
        # print(list_rate[0])
        ipo = get_client_ip(request)
        message = request.POST['review']
        # print(message)
        obj = REVIEWS(ip=ipo, msg=message, rate=list_rate[0])
        obj.save()
        return redirect('/')
    urlf = listurl()
    occf = listoccf()
    ph = phish()
    nph = notphish()

    print(len(urlf))
    print(len(occf))
    lab0 = urlf[0]
    lab1 = urlf[1]
    lab2 = urlf[2]
    lab3 = urlf[3]
    lab4 = urlf[4]
    lab5 = urlf[5]
    lab6 = urlf[6]

    occ0 = occf[0]
    occ1 = occf[1]
    occ2 = occf[2]
    occ3 = occf[3]
    occ4 = occf[4]
    occ5 = occf[5]
    occ6 = occf[6]

    column2d = FusionCharts("column2d", "ex1", "684", "476", "chart-1", "json",
                            {
                                "chart": {
                                    "caption": "Most Submitted URLs",
                                    "baseFont": "Lato",
                                    "captionfontsize": "18",
                                    "subcaption": "2018",
                                    "yaxisname": "Number of Submissions",
                                    "captionpadding": "20",
                                    "showvalues": "0",
                                    "showborder": "0",
                                    "showalternatehgridcolor": "0",
                                    "plotgradientcolor": "2",
                                    "showplotborder": "0",
                                    "adjustDiv": "0",
                                    "yaxisnamefontsize": "14",
                                    "yAxisNameFontBold": "0",
                                    "yAxisValuesPadding": "18",
                                    "divlinealpha": "10",
                                    "xaxislinealpha": "20",
                                    "LabelPadding": "50",
                                    "showlabels": "0",
                                    "numdivlines": "4",
                                    "showxaxisline": "1",
                                    "plotspacepercent": "40",
                                    "yAxisValueDecimals": "0",
                                    "formatnumberscale": "1",
                                    # "numberscalevalue": "24,31,12",
                                    # "numberscaleunit": " day, months, years",
                                    "palettecolors": "#50e85a",
                                    "plotToolText": "<div>URL : <b>$label</b><br/>Submissions' Number : <b>$value</b></div>",
                                    "defaultnumberscale": " ",
                                    "plotFillAlpha": "90"
                                },

                                "data": [{
                                    "label": lab0,
                                    "value": occ0
                                }, {
                                    "label": lab1,
                                    "value": occ1
                                }, {
                                    "label": lab2,
                                    "value": occ2
                                }, {
                                    "label": lab3,
                                    "value": occ3
                                }, {
                                    "label": lab4,
                                    "value": occ4
                                }, {
                                    "label": lab5,
                                    "value": occ5
                                }, {
                                    "label": lab6,
                                    "value": occ6
                                }, {

                                }]
                            })
    pie2d = FusionCharts("pie2d", "ex2", "684", "476", "chart-2", "json",
                         {
                             "chart": {
                                 "caption": "Total Phish",

                                 "startingangle": "120",
                                 "showlabels": "0",
                                 "showlegend": "1",
                                 "enablemultislicing": "0",
                                 "slicingdistance": "15",
                                 "showpercentvalues": "1",
                                 "showpercentintooltip": "0",
                                 "plottooltext": "$label $datavalue",
                                 "theme": "ocean"
                             },

                             "data": [{
                                 "label": "phish",
                                 "value": ph
                             }, {
                                 "label": "notphish",
                                 "value": nph
                             }, {

                             }]
                         })
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    context = {'output1': column2d.render(), 'output2': pie2d.render()}
    return render(request, 'phish/index.html', context)


def verify(request):
    if request.method == "POST":
        urlf = listurl()
        occf = listoccf()
        ph = phish()
        nph = notphish()

        print(len(urlf))
        print(len(occf))
        lab0 = urlf[0]
        lab1 = urlf[1]
        lab2 = urlf[2]
        lab3 = urlf[3]
        lab4 = urlf[4]
        lab5 = urlf[5]
        lab6 = urlf[6]

        occ0 = occf[0]
        occ1 = occf[1]
        occ2 = occf[2]
        occ3 = occf[3]
        occ4 = occf[4]
        occ5 = occf[5]
        occ6 = occf[6]
        column2d = FusionCharts("column2d", "ex1", "684", "476", "chart-1", "json",
                                {
                                    "chart": {
                                        "caption": "Most Submitted URLs",
                                        "baseFont": "Lato",
                                        "captionfontsize": "18",
                                        "subcaption": "2018",
                                        "yaxisname": "Number of Submissions",
                                        "captionpadding": "20",
                                        "showvalues": "0",
                                        "showborder": "0",
                                        "showalternatehgridcolor": "0",
                                        "plotgradientcolor": "2",
                                        "showplotborder": "0",
                                        "adjustDiv": "0",
                                        "yaxisnamefontsize": "14",
                                        "yAxisNameFontBold": "0",
                                        "yAxisValuesPadding": "18",
                                        "divlinealpha": "10",
                                        "xaxislinealpha": "20",
                                        "LabelPadding": "50",
                                        "showlabels": "0",
                                        "numdivlines": "4",
                                        "showxaxisline": "1",
                                        "plotspacepercent": "40",
                                        "yAxisValueDecimals": "0",
                                        "formatnumberscale": "1",
                                        # "numberscalevalue": "24,31,12",
                                        # "numberscaleunit": " day, months, years",
                                        "palettecolors": "#50e85a",
                                        "plotToolText": "<div>URL : <b>$label</b><br/>Submissions' Number : <b>$value</b></div>",
                                        "defaultnumberscale": " ",
                                        "plotFillAlpha": "90"
                                    },

                                    "data": [{
                                        "label": lab0,
                                        "value": occ0
                                    }, {
                                        "label": lab1,
                                        "value": occ1
                                    }, {
                                        "label": lab2,
                                        "value": occ2
                                    }, {
                                        "label": lab3,
                                        "value": occ3
                                    }, {
                                        "label": lab4,
                                        "value": occ4
                                    }, {
                                        "label": lab5,
                                        "value": occ5
                                    }, {
                                        "label": lab6,
                                        "value": occ6
                                    }, {

                                    }]
                                })
        pie2d = FusionCharts("pie2d", "ex2", "684", "476", "chart-2", "json",
                             {
                                 "chart": {
                                     "caption": "Total Phish",

                                     "startingangle": "120",
                                     "showlabels": "0",
                                     "showlegend": "1",
                                     "enablemultislicing": "0",
                                     "slicingdistance": "15",
                                     "showpercentvalues": "1",
                                     "showpercentintooltip": "0",
                                     "plottooltext": "$label $datavalue",
                                     "theme": "ocean"
                                 },

                                 "data": [{
                                     "label": "phish",
                                     "value": ph
                                 }, {
                                     "label": "notphish",
                                     "value": nph
                                 }, {

                                 }]
                             })
        # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.

        url = request.POST['url']

        url = url.strip(' \t\n\r')
        try:
            requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}, timeout=60,
                         verify=False).raise_for_status()
        except:
            context = {'output1': column2d.render(), 'output2': pie2d.render(),
                       'inaccessible_url': "Inaccessible url"
                       }
            return render(request, 'phish/index.html', context)
        list = vectorize(url)
        print(list)
        result = classify(list)
        if (URL.objects.filter(name=url).count() == 0):
            obj = URL(name=url, phish=result, occ=0)
            obj.save()
        else:
            URL.objects.filter(name=url).update(occ=F('occ') + 1)

        # ip = get_client_ip(request)
        # test = int(IP.objects.filter(ip=ip).count())
        # if (test == 0):
        # 	Ip = IP(ip.get_client_ip(request),occ= 0)
        # 	Ip.save()
        # else:
        # 	IP.objects.filter(ip=ip).update(occ=F('occ') + 1)

        if result:
            context = {'output1': column2d.render(), 'output2': pie2d.render(),
                       'phish_pos': "Beware ! It's a phish !"
                       }

        else:
            context = {'output1': column2d.render(), 'output2': pie2d.render(),
                       'phish_neg': "Go ahead , It's not a phish !"
                       }
        return render(request, 'phish/index.html', context)
    else:
        return redirect('/')


def listocc():
    urls = URL.objects.all()
    occur = []
    for url in urls:
        occur = occur + [int(format(url.occ))]
    occur.sort()
    occur.reverse()
    return (occur)


def listurl():
    urls = URL.objects.all()
    phishing_urls = []
    occur = sorted(list(set(listocc())))
    occur.reverse()
    # print(occur)
    for c in occur:
        for url in urls:
            if url.occ == int(c):
                phishing_urls = phishing_urls + [format(url.name)]
    return (phishing_urls)


def listoccf():
    urls = URL.objects.all()
    urlf = listurl()
    occf = []
    for u in urlf:
        # print(u)
        for url in urls:
            if url.name == u:
                occf = occf + [int(format(url.occ))]
    return (occf)


def phish():
    ph = URL.objects.filter(phish=True).count()
    return (ph)


def notphish():
    nph = URL.objects.filter(phish=False).count()
    return (nph)


def chart(request):
    urlf = listurl()
    occf = listoccf()
    ph = phish()
    nph = notphish()

    print(len(urlf))
    print(len(occf))
    lab0 = urlf[0]
    lab1 = urlf[1]
    lab2 = urlf[2]
    lab3 = urlf[3]
    lab4 = urlf[4]
    lab5 = urlf[5]
    lab6 = urlf[6]

    occ0 = occf[0]
    occ1 = occf[1]
    occ2 = occf[2]
    occ3 = occf[3]
    occ4 = occf[4]
    occ5 = occf[5]
    occ6 = occf[6]

    column2d = FusionCharts("column2d", "ex1", "684", "476", "chart-1", "json",
                            {
                                "chart": {
                                    "caption": "Most Submitted URLs",
                                    "baseFont": "Lato",
                                    "captionfontsize": "18",
                                    "subcaption": "2018",
                                    "yaxisname": "Number of Submissions",
                                    "captionpadding": "20",
                                    "showvalues": "0",
                                    "showborder": "0",
                                    "showalternatehgridcolor": "0",
                                    "plotgradientcolor": "2",
                                    "showplotborder": "0",
                                    "adjustDiv": "0",
                                    "yaxisnamefontsize": "14",
                                    "yAxisNameFontBold": "0",
                                    "yAxisValuesPadding": "18",
                                    "divlinealpha": "10",
                                    "xaxislinealpha": "20",
                                    "LabelPadding": "50",
                                    "showlabels": "0",
                                    "numdivlines": "4",
                                    "showxaxisline": "1",
                                    "plotspacepercent": "40",
                                    "yAxisValueDecimals": "0",
                                    "formatnumberscale": "1",
                                    # "numberscalevalue": "24,31,12",
                                    # "numberscaleunit": " day, months, years",
                                    "palettecolors": "#50e85a",
                                    "plotToolText": "<div>URL : <b>$label</b><br/>Submissions' Number : <b>$value</b></div>",
                                    "defaultnumberscale": " ",
                                    "plotFillAlpha": "90"
                                },

                                "data": [{
                                    "label": lab0,
                                    "value": occ0
                                }, {
                                    "label": lab1,
                                    "value": occ1
                                }, {
                                    "label": lab2,
                                    "value": occ2
                                }, {
                                    "label": lab3,
                                    "value": occ3
                                }, {
                                    "label": lab4,
                                    "value": occ4
                                }, {
                                    "label": lab5,
                                    "value": occ5
                                }, {
                                    "label": lab6,
                                    "value": occ6
                                }, {

                                }]
                            })
    pie2d = FusionCharts("pie2d", "ex2", "684", "476", "chart-2", "json",
                         {
                             "chart": {
                                 "caption": "Total Phish",

                                 "startingangle": "120",
                                 "showlabels": "0",
                                 "showlegend": "1",
                                 "enablemultislicing": "0",
                                 "slicingdistance": "15",
                                 "showpercentvalues": "1",
                                 "showpercentintooltip": "0",
                                 "plottooltext": "$label $datavalue",
                                 "theme": "ocean"
                             },

                             "data": [{
                                 "label": "phish",
                                 "value": ph
                             }, {
                                 "label": "notphish",
                                 "value": nph
                             }, {

                             }]
                         })
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    context = {'output1': column2d.render(), 'output2': pie2d.render()}
    return render(request, 'phish/stat.html', context)

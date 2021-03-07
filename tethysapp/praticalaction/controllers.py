from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from tethys_sdk.gizmos import Button
import decimal, csv, json
from .chartUtils import getForecastData, get_forecastpercent
import requests, psycopg2
from datetime import timedelta
import datetime as dt
from .utils import get_thredds_info

# @login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'praticalaction/home.html', context)

def check_for_decimals(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def getRecentDate(comid, cty):
    conn = psycopg2.connect(host="192.168.10.6", database="servirFloodHiwat", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = 'select distinct(rundate) from forecast' + cty + ' where comid = ' + comid + ' order by rundate desc'

    try:
        cur.execute(query)
        a = cur.fetchall()
        bb = (str(a[0])[19:-3]).split(",")
        b = bb[0].strip() + "-" + "{:02d}".format(int(bb[1])) + "-" + "{:02d}".format(int(bb[2]))
    except:
        runDate = dt.datetime.now().date() - timedelta(1)
        b = runDate.strftime('%Y-%m-%d')

    conn.close()
    return b

def getGeoJson(loc):
    request_params = dict(cty=loc)
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/hiwatAPI/getFeaturesHIWATPA', params=request_params,headers=request_headers)
    # print (res.text)
    return(res.text)

def getGeoJson1(request):
    loc = request.GET.get('stID').strip()
    request_params = dict(cty=loc)
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/hiwatAPI/getFeaturesHIWATPA', params=request_params,headers=request_headers)
    # print (res.text)
    # return(res.text)
    return HttpResponse(res.text, content_type='application/json')


def chartHiwat(request):
    return_obj = {}
    try:
        comid =int(request.GET.get('stID'))
    except:
        comid = 57465
    return_obj = getForecastData(comid)
    # print (return_obj)
    return HttpResponse(return_obj, content_type= 'application/json')

def forecastpercent(request):
    if request.is_ajax() and request.method == 'GET':
        comid = request.GET.get('comid')
        return JsonResponse(get_forecastpercent(comid))

def index(request):
    getjson = getGeoJson('Babai')
    thredds_wms_obj = get_thredds_info()
#    print(getjson)
    context = {
        'myJson': getjson,
        'thredds_urls': json.dumps(thredds_wms_obj),
    }
    return render(request, 'praticalaction/main.html', context)

def getForecastCSV(request):
    comid = request.GET.get('comid')
    cty = request.GET.get('cty')
    recentDate = request.GET.get('forecastDate')
    if recentDate is None:
        recentDate = getRecentDate(comid, cty)
    conn = psycopg2.connect(host="192.168.10.6", database="servirFloodHiwat", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "SELECT forecastdate, forecastvalue FROM public.forecast" + cty + " where comid =" \
            + str(comid) + " and runDate = '" + str(recentDate) + "' order by forecastdate"

    cur.execute(query)
    rows = cur.fetchall()
    # // CSV starts herer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forecastData_' + str(comid) + '.csv"'
    header = ['Dates', 'Values']
    writer = csv.writer(response)
    writer.writerow(header)

    for row in rows:
        dates = (str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S')))
        values = (float(row[1]))

        writer.writerow([dates, values])
    conn.close()
    return response

def getHistoricCSV(request):
    comid = request.GET.get('comid')
    cty = request.GET.get('cty')

    conn = psycopg2.connect(host="192.168.10.6", database="servirFloodHiwat", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "select historydate, historyvalue from history" + cty + " where comid = " + str(
        comid) + " order by historydate"
    cur.execute(query)
    rows = cur.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historicData_' + str(comid) + '.csv"'
    header = ['Dates', 'Values']
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        mydate = str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S'))
        writer.writerow([mydate, row[1]])
    conn.close()
    return response






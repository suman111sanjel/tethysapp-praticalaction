import requests, ast, json #, decimal
import datetime as dt
from datetime import timedelta
runDate = dt.datetime.now().date() - timedelta(days=0)
from django.http import JsonResponse


def get_returnPeriod_data(comid):
    request_params = dict(comid=comid, cty='nepal')
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/hiwatAPI/getreturnPeriodHIWAT', params=request_params, headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'return_max':
            return_max = value
        if key == 'return_20':
            return_20 = value
        if key == 'return_10':
            return_10 = value
        if key == 'return_2':
            return_2 = value
    return return_max, return_2, return_10, return_20

def get_historic_data(comid):
    hdates = []
    hvalues= []
    request_params = dict(comid=comid, cty='nepal')
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/hiwatAPI/getHistoricHIWAT', params=request_params,headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'hdates':
            hdates = value
        if key == 'hvalues':
            hvalues = value
    return hdates, hvalues, hdates[0], hdates[-1]
def get_flow_duration_curve(comid):
    request_params = dict(comid=comid, cty='bhutan')
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/api/getFlowDurationCurve', params=request_params,headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'prob':
            prob = value
        if key == 'sorted_daily_avg1':
            sorted_daily_avg1 = value
    return prob, sorted_daily_avg1
def getForecastData(comid):
    request_params = dict(comid=comid, cty='nepal')
    request_headers = dict(Authorization='Token 93eae5155d3c551cd5d449e896cf707869b63eb2')
    res = requests.get('http://tethys.icimod.org/apps/apicenter/hiwatAPI/getForecastHIWAT', params=request_params, headers=request_headers)
    data = json.loads(res.text)
    for key, value in data.items():
        if key == 'dates':
            dates = value
        if key == 'values':
            values = value
        if key == 'rundate':
            rundate = value

    return_obj = {}

    # Get Historic data
    hdate, hval,datetime_start,datetime_end = get_historic_data(comid)
    #
    # #Get Return Period
    return_max, return_2, return_10, return_20 = get_returnPeriod_data(comid)

    # # Get flow duration
    # prob, sorted_daily_avg = get_flow_duration_curve(comid)

    return_obj["dates"] = (dates)
    return_obj["values"] = (values)
    return_obj["rundate"] = (rundate)
    return_obj["riverID"] = (comid)

    return_obj["success"] = "success"
    # return_obj["range"] =  max(max_values) + max(max_values) / 5

    # # #Historic data
    return_obj["hdate"] = (hdate)
    return_obj["hval"] = (hval)

    # # #Return Period
    return_obj["return_max"] = return_max
    return_obj["return_2"] = return_2
    return_obj["return_10"] = return_10
    return_obj["return_20"] = return_20
    return_obj["datetime_start"] = (datetime_start)
    return_obj["datetime_end"] = (datetime_end)
    #
    # #Flow-Duration
    # return_obj["prob"] = (prob)
    # return_obj["sorted_daily_avg"] = (sorted_daily_avg)

    #Download data
    return JsonResponse(return_obj)

def get_forecastpercent(comid):
    ens = ''

    request_params = dict(watershed_name='south_asia', subbasin_name='mainland', reach_id=comid,
                          return_format='csv')
    request_headers = dict(Authorization='Token f8c44a2529aa779332944206a5e23885a682cc96')  # SERVIR
    rpall = requests.get('http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetReturnPeriods/',
                         params=request_params,
                         headers=request_headers)

    request_params = dict(watershed_name='south_asia', subbasin_name='mainland', reach_id=comid,
                          forecast_folder='most_recent', ensemble=ens)
    request_headers = dict(Authorization='Token f8c44a2529aa779332944206a5e23885a682cc96')
    ens = requests.get('https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetEnsemble/',
                       params=request_params, headers=request_headers)

    dicts = ens.content.splitlines()
    dictstr = []
    # a = str(rpall.content, "utf-8")
    rpdict = ast.literal_eval(rpall.content)
    rpdict.pop('max', None)

    rivperc = {}
    riverpercent = {}
    rivpercorder = {}

    for q in rpdict:
        rivperc[q] = {}
        riverpercent[q] = {}

    dictlen = len(dicts)
    for i in range(1, dictlen):
        # b = str(dicts[i], "utf-8")
        dictstr.append(dicts[i].split(","))

    for rps in rivperc:
        rp = float(rpdict[rps])
        for b in dictstr:
            date = b[0][:10]
            if date not in rivperc[rps]:
                rivperc[rps][date] = []
            length = len(b)
            for x in range(1, length):
                flow = float(b[x])
                if x not in rivperc[rps][date] and flow > rp:
                    rivperc[rps][date].append(x)
        for e in rivperc[rps]:
            riverpercent[rps][e] = float(len(rivperc[rps][e])) / 51.0 * 100

    for keyss in rivperc:
        data = riverpercent[keyss]
        ordered_data = sorted(
            data.items(), key=lambda x: dt.datetime.strptime(x[0], '%Y-%m-%d'))
        rivpercorder[keyss] = ordered_data

    rivdates = []
    rivperctwo = []
    rivpercten = []
    rivperctwenty = []

    for a in rivpercorder['two']:
        rivdates.append(a[0])
        rivperctwo.append(a[1])

    for s in rivpercorder['ten']:
        rivpercten.append(s[1])

    for d in rivpercorder['twenty']:
        rivperctwenty.append(d[1])

    formatteddates = [str(elem)[-4:] for elem in rivdates]
    formattedtwo = ["%.0f" % elem for elem in rivperctwo]
    formattedten = ["%.0f" % elem for elem in rivpercten]
    formattedtwenty = ["%.0f" % elem for elem in rivperctwenty]

    formatteddates = formatteddates[:len(formatteddates) - 5]
    formattedtwo = formattedtwo[:len(formattedtwo) - 5]
    formattedten = formattedten[:len(formattedten) - 5]
    formattedtwenty = formattedtwenty[:len(formattedtwenty) - 5]

    dataformatted = {'percdates': formatteddates, 'two': formattedtwo, 'ten': formattedten,
                     'twenty': formattedtwenty}

    return dataformatted



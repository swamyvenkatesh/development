# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse, HttpResponseRedirect
import xmltodict
import json
import ast
from datetime import datetime
from xlrd import open_workbook
import os, sys
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
def allview(request):
    """ 
    This view to collect all details from Home Page
    """
    if request.method == "POST":
        originStattion = request.POST.get('txtfromstation')
        destStattion = request.POST.get('txttostation')
        departureDate = request.POST.get('txtfromdate')
        departureTime = request.POST.get('Ddldeptime')
        returnDate = request.POST.get('txttodate')
        returnTime = request.POST.get('DdlReturntime')
        numAdults = request.POST.get('DdlAdults')
        numChilds = request.POST.get('DdlNonAdults')      

        date_string = str(departureDate)
        format1 = "%d-%b-%Y"
        format2 = "%Y-%m-%d"
        actual_date = datetime.strptime(date_string, format1).strftime(format2)
        
        request.session['origin'] = str(originStattion)
        request.session['destination'] = str(destStattion)
        request.session['deptDate'] = str(actual_date)
        request.session['deptTime'] = str(departureTime)
        request.session['adults'] = int(numAdults)
        request.session['children'] = int(numChilds)
        return HttpResponseRedirect('/alltest/ticket/')        
    else:
        return render(request,"booking/index.html",{})

def ticket_view(request):
    """ 
    Point To Point Tickets generating view 
    """
    originLoc = request.session['origin']
    destinationLoc = request.session['destination']
    date_string = request.session['deptDate']+"T"+request.session['deptTime']
    date_time_obj = datetime.strptime(request.session['deptDate'], '%Y-%m-%d')     
    display_date = date_time_obj.date()
    no_of_adults = request.session['adults'] 
    no_of_childs = request.session['children']  
    
    wb=open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
    worksheet = wb.sheet_by_index(0)
    nc = worksheet.ncols
    nr = worksheet.nrows
    ortakes=[]
    desttakes=[]
    fr=[]    
    orgLocCode = 0
    countryCode = 0
    destLocCode = 0
    for cr in range(1, nr):
        firstcol=worksheet.cell_value(cr, 1).encode('utf-8')
        if firstcol == originLoc :
            orgLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))            
        if firstcol == destinationLoc :
            destLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))    

    xml = """
        <?xml version="1.0" encoding="UTF-8"?>
            <ACP_RailAvailRQ xmlns="http://www.acprailinternational.com/API/R2" ResponseType="Native-Availability">
                <POS>
                    <RequestorID>RTG-XML</RequestorID>
                </POS>
                <RailAvailInfo>
                    <OriginDestinationSpecifications>
                        <OriginLocation LocationCode="%d"/>
                        <DestinationLocation LocationCode="%d"/>
                        <Departure DepartureDate="%s:00.0Z"/>
                    </OriginDestinationSpecifications>
                    <PassengerSpecifications>
                        <PassengerType Age="-1" Quantity="3"/>
                    </PassengerSpecifications>
                    <FareQualifier RateCategory="Regular"/>
                        <ResponsePtPTypes>
                            <ResponsePtPType>TW</ResponsePtPType>
                        </ResponsePtPTypes>
                </RailAvailInfo>
            </ACP_RailAvailRQ>
        """%(orgLocCode, destLocCode, date_string)

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text             
        result = xmltodict.parse(response)  

        try:            
            result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))            
            result = result.encode('utf-8') 
        except:
            pass       
        
        if result['ACP_RailAvailRS'].get('OriginDestinationOptions') is not None:

            originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
            destinationLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['DestinationLocation']['@Name']                                 
            journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']

            result_list = []
            fareRPHS_List = []

            for index,i in enumerate(journey):
                result_dict = {}            
                changes = i['JourneySegments']['JourneySegment']
                if i.get('FareRPHs'):
                    fareRPHS_List.append(i['FareRPHs']['FareRPH'])
                    result_dict['fareRPHS_List'] = i['FareRPHs']['FareRPH']
                result_dict['changes'] = len(changes) - 1       

                deptTimeList = []
                arrivalTimeList = [] 
                journeyDetailsList = []
                if len(changes) == 1:                    
                    segment = changes['TrainSegment']                
                    trainNum = segment['@TrainNumber']
                    departDateTime = segment['@DepartureDateTime']
                    arrivalDateTime = segment['@ArrivalDateTime']
                    departStation = segment['DepartureStation']
                    departStationName = departStation['@Name']
                    arrivaltStation = segment['ArrivalStation']
                    arrivaltStationName = arrivaltStation['@Name']

                    depttime = departDateTime.split("T")[-1]
                    deptTimeList.append(depttime)
                    arrtime = arrivalDateTime.split("T")[-1]
                    arrivalTimeList.append(arrtime)

                    journeyDetails = {}
                    journeyDetails['train'] = str(trainNum)
                    journeyDetails['dept_station'] = str(departStationName)
                    journeyDetails['dept_time'] = str(depttime)
                    journeyDetails['arr_station'] = str(arrivaltStationName)
                    journeyDetails['arr_time'] = str(arrtime)
                    journeyDetailsList.append(journeyDetails)
                else:
                    for change in changes:
                        segment = change['TrainSegment']                
                        trainNum = segment['@TrainNumber']
                        departDateTime = segment['@DepartureDateTime']
                        arrivalDateTime = segment['@ArrivalDateTime']
                        departStation = segment['DepartureStation']
                        departStationName = departStation['@Name']
                        arrivaltStation = segment['ArrivalStation']
                        arrivaltStationName = arrivaltStation['@Name']

                        depttime = departDateTime.split("T")[-1]
                        deptTimeList.append(depttime)
                        arrtime = arrivalDateTime.split("T")[-1]
                        arrivalTimeList.append(arrtime)

                        journeyDetails = {}
                        journeyDetails['train'] = str(trainNum)
                        journeyDetails['dept_station'] = str(departStationName)
                        journeyDetails['dept_time'] = str(depttime)
                        journeyDetails['arr_station'] = str(arrivaltStationName)
                        journeyDetails['arr_time'] = str(arrtime)                
                        journeyDetailsList.append(journeyDetails)
                   
                result_dict['departure'] = deptTimeList[0]
                result_dict['arrival'] = arrivalTimeList[-1]
                datetimeFormat = '%H:%M:%S'
                timeDuration = datetime.strptime(result_dict['arrival'], datetimeFormat)\
                    - datetime.strptime(result_dict['departure'], datetimeFormat)

                result_dict['duration'] = timeDuration
                result_dict['journey_details'] = journeyDetailsList
                result_dict['index'] = index                
                result_list.append(result_dict)
                
            fares = result['ACP_RailAvailRS']['Fares']['Fare']            
            sample = []        
            fare_classes_list = []

            for ff in fareRPHS_List:
                li = []
                for j in fares:
                    fare_classes_list.append(str(j['@Class']))                    
                    if len(ff) != 0:
                        for k in ff:                            
                            if k == j['@FareReference']:
                                dic1 = {}
                                dic1['total_price'] = j['TotalPrice']['@Amount']
                                
                                dic1['fareRefer'] = j['@FareReference']
                                dic1['class'] = j['@Class']
                                dic1[j['@Class']] = j['TotalPrice']['@Amount']
                                dic1['product_name'] = str(j['ProdMarketingName']).split(">")[1].replace("</div","")                                
                                dic1['sales_condition'] = j['SalesConditions']['@RefundPolicy']


                                dic1['ticket_option'] = j['@TicketOption']
                                dic1['is_passport'] = j['@PassportRequired']
                                dic1['is_dob'] = j['@DateOfBirthRequired']
                                dic1['is_paxname'] = j['@PaxNameRequested']
                                dic1['is_cntryres'] = j['@CntryResidenceRequired']
                                dic1['is_nationality'] = j['@NationalityRequired']
                                dic1['is_birthplace'] = j['@PlaceOfBirthRequired']
                                dic1['is_email'] = j['@EmailRequired']


                                li.append(dic1)
                    else:
                        li = []
                        ff == j['@FareReference']
                        dic1 = {}
                        dic1['total_price'] = j['TotalPrice']['@Amount']                       
                        dic1['fareRefer'] = j['@FareReference']
                        dic1['class'] = j['@Class']
                        dic1['product_name'] = str(j['ProdMarketingName']).split(">")[1].replace("</div","")
                        dic1['sales_condition'] = j['SalesConditions']['@RefundPolicy']
                        dic1['ticket_option'] = j['@TicketOption']
                        dic1['is_passport'] = j['@PassportRequired']
                        dic1['is_dob'] = j['@DateOfBirthRequired']
                        dic1['is_paxname'] = j['@PaxNameRequested']
                        dic1['is_cntryres'] = j['@CntryResidenceRequired']
                        dic1['is_nationality'] = j['@NationalityRequired']
                        dic1['is_birthplace'] = j['@PlaceOfBirthRequired']
                        dic1['is_email'] = j['@EmailRequired']
                        li.append(dic1)
                        sample.append(li)
                sample.append(li)
            fare_classes_list = list(set(fare_classes_list))           
            
            final_list = []
            dd = {}
            ddd = {}
            for main_index,i in enumerate(sample):                
                min_value = 0
                for kk in i:        
                    if kk['product_name'] not in dd:                        
                        for index, class1 in enumerate(fare_classes_list):
                            if kk.get(class1) is not None:
                                list1 = {}                    
                                list1[class1] = kk[class1]
                                dd[kk['product_name']] = list1
                                if min_value == 0:
                                    min_value = kk[class1]
                                elif min_value > kk[class1]:
                                    min_value = kk[class1]
                    else:                        

                        for index, class1 in enumerate(fare_classes_list):
                            if kk.get(class1) is not None: 
                                name = dd.get(kk['product_name'])                  
                                name[class1] = kk[class1]
                                dd[kk['product_name']] = name
                                if min_value == 0:
                                    min_value = kk[class1]
                                elif min_value > kk[class1]:
                                    min_value = kk[class1]

                dd['min'] = min_value
                ddd[main_index] = dd
                
                if result_list[main_index]['index'] == main_index:
                    result_list[main_index]['lowest_price'] = min_value                    

                final_list.append(ddd)
                dd = {}
                ddd = {}   
 
            return render(request,"booking/tickets.html",
                {"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, 
                "final_result":result_list, "prices_data":sample, 'classes':fare_classes_list, 
                'result_output':final_list, 'adults':no_of_adults, 'childs':no_of_childs} )        
        else:
            return HttpResponse("Getting Web Service Error")
    else:
        print "Status code error", Result.status_code
        return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":display_date})  



def traveller_ajax_info(request):
    if request.method == "GET":
        adults = request.GET.get('adults_num')
        childs = request.GET.get('child_num')
        date_text = request.GET.get('date_text')



        return render(request,"booking/traveller-information.html",
            {'adults_count':adults,'child_count':childs, 'date_text':date_text})
        # return HttpResponse("test")
    else:
        pass

def traveller_info(request):
    # no_of_adults = request.session['adults'] 
    # no_of_childs = request.session['children']
    no_of_adults = 3
    no_of_childs = 2
    date_text = "Madrid - Barcelona - Jan. 30, 2019"
    # if request.method == "GET":
    #     adults = request.GET.get('adults_num')
    #     childs = request.GET.get('child_num')
    #     date_text = request.GET.get('date_text')



    #     return render(request,"booking/traveller-information.html",
    #         {'adults_count':adults,'child_count':childs, 'date_text':date_text})
    #     return HttpResponse("test")
    # else:
    #     return render(request,"booking/traveller-information.html",
    #         {'adults_count':no_of_adults,'child_count':no_of_childs,'date_text':date_text})

    
    return render(request,"booking/traveller-information.html",
            {'adults_count':no_of_adults,'child_count':no_of_childs,'date_text':date_text})




def checkinfodeatil(request):

    return render(request,'booking/checkout.html',{})



def checkinfodeatil1(request):
    if request.method=="GET":

        print request.GET,"((("
        # data1=json.dumps(request.GET)
        # try:
        #     data1=ast.literal_eval(data1)
        #     lastname = data1.get('varsec1')
        #     print lastname
        # except:
        #     pass
        # print data1
        # print data1.get("varsec1")
        newdat=request.GET.get("varfrst")
        newdat1=request.GET.get("varsec1")
        print newdat,newdat1,"{{{{{{{{{"
        return HttpResponse("hi")


        # return render(request,'booking/checkout.html',{})
    else:
        return render(request,'booking/checkout.html',{})
def summarydetail(request):
    return render(request,'booking/summary.html',{})
def summary1deta(request):
    return render(request,'booking/summary1.html',{})
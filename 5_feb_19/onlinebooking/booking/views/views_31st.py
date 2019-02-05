# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

def childAges(request):
    if request.session.get('child_ages'):
        del request.session['child_ages']
    if request.method == "GET":
        # print request.GET
        child_ages = request.GET.getlist('child_passenger_ages[]')
        # print child_ages 
        request.session['child_ages'] = [str(i) for i in child_ages]
        return JsonResponse({'message':"success"})
    else:
        pass

def ticket_view(request):
    """ 
    Point To Point Tickets generating view 
    """
    ErroMessage = ""
    originLoc = request.session['origin']
    destinationLoc = request.session['destination']
    date_string = request.session['deptDate']+"T"+request.session['deptTime']
    date_time_obj = datetime.strptime(request.session['deptDate'], '%Y-%m-%d')     
    display_date = date_time_obj.date()
    no_of_adults = request.session['adults'] 
    no_of_childs = request.session['children']   
    child_ages = request.session['child_ages']
    # print child_ages

    ReturnReturnDate="" 
    
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

    xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
    root = ET.Element("ACP_RailAvailRQ",xmlns="http://www.acprailinternational.com/API/R2", ResponseType="Native-Availability")
    pos = ET.SubElement(root, "POS")
    requestor = ET.SubElement(pos, "RequestorID").text="RTG-XML"
    rail_avail_info = ET.SubElement(root, "RailAvailInfo")
    origins = ET.SubElement(rail_avail_info , 'OriginDestinationSpecifications')
    origin1=ET.SubElement(origins,'OriginLocation', LocationCode="{0}".format(orgLocCode))
    origin2=ET.SubElement(origins,'DestinationLocation', LocationCode="{0}".format(destLocCode))
    origin3=ET.SubElement(origins,'Departure', DepartureDate="{0}".format(date_string))
    if ReturnReturnDate:
        origin4=ET.SubElement(origins,'Return', ReturnDate="{0}".format(""))

    passengers = ET.SubElement(rail_avail_info , 'PassengerSpecifications')
    # for adults 
    passtype=ET.SubElement(passengers,'PassengerType',Age="-1", Quantity="{0}".format(no_of_adults))
    # for childs
    if child_ages:
        for i in child_ages:
            passtype=ET.SubElement(passengers,'PassengerType',Age=str(i), Quantity="1")
    fare_qual=ET.SubElement(rail_avail_info,'FareQualifier RateCategory="Regular"')
    responsePt=ET.SubElement(rail_avail_info,'ResponsePtPTypes')
    responsePt1=ET.SubElement(responsePt,'ResponsePtPType').text="TW" 
    mydata = ET.tostring(root) 

    xml_data += mydata  
    print xml_data 

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml_data, headers=headers)
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
                
            if result['ACP_RailAvailRS'].get('Fares') is not None:
                fares = result['ACP_RailAvailRS']['Fares']['Fare']            
                sample = []        
                fare_classes_list = []

                for ff in fareRPHS_List:
                    li = []
                    for j in fares:
                        clas = str(j['@Class'])
                        if clas.__contains__('-'):
                            clas = clas.split("-")[-1]
                        fare_classes_list.append(clas)                    
                        if len(ff) != 0:
                            for k in ff:                            
                                if k == j['@FareReference']:
                                    dic1 = {}
                                    dic1['total_price'] = j['TotalPrice']['@Amount']                                
                                    dic1['fareRefer'] = j['@FareReference']                                
                                    dic1['class'] = clas
                                    dic1[clas] = j['TotalPrice']['@Amount']
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
                            dic1['class'] = clas
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
                # print fare_classes_list        
                print "$$$###"*40
                print sample
                final_list = []
                dd = {}
                ddd = {}
                for main_index,i in enumerate(sample):                
                    min_value = 0
                    min_value_list = []
                    for kk in i:        
                        if kk['product_name'] not in dd:                        
                            for index, class1 in enumerate(fare_classes_list):
                                if kk.get(class1) is not None:
                                    list1 = {}                    
                                    list1[class1] = kk[class1]
                                    dd[kk['product_name']] = list1
                                    
                                    if min_value == 0:
                                        min_value = kk[class1]
                                        min_value_list.append(min_value)

                                    elif min_value > kk[class1]:
                                        min_value = kk[class1]
                                        min_value_list.append(min_value)

                        else:                        

                            for index, class1 in enumerate(fare_classes_list):
                                if kk.get(class1) is not None: 
                                    name = dd.get(kk['product_name'])                  
                                    name[class1] = kk[class1]
                                    dd[kk['product_name']] = name

                                    if min_value == 0:
                                        min_value = kk[class1]
                                        min_value_list.append(min_value)

                                    elif min_value > kk[class1]:
                                        min_value = kk[class1]
                                        min_value_list.append(min_value)
                    
                    
                    min_value_list = sorted([float(i) for i in min_value_list])
                    min_value = min(min_value_list)          

                    dd['min'] = min_value
                    ddd[main_index] = dd
                    
                    if result_list[main_index]['index'] == main_index:
                        result_list[main_index]['lowest_price'] = min_value                    

                    final_list.append(ddd)


                    dd = {}
                    ddd = {} 
                print "=================================="
                print final_list
                print "After successfull response"                
                return render(request,"booking/tickets.html",
                    {"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, 
                    "final_result":result_list, "prices_data":sample, 'classes':fare_classes_list, 
                    'result_output':final_list, 'adults':no_of_adults, 'childs':no_of_childs,"Error":ErroMessage} )        
        

            else:
                return render(request,"booking/tickets.html",
                    {"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, 
                    "final_result":result_list, "prices_data":[], 'classes':[], 
                    'result_output':[], 'adults':no_of_adults, 'childs':no_of_childs,"Error":ErroMessage} )
        else:
            ErroMessage = "Getting Web Service Error"
            return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, "Error":ErroMessage})  
            # return HttpResponse("Getting Web Service Error")
    else:
        # print "Status code error", Result.status_code
        return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, "Error":ErroMessage})  



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




def passenger_page_info1(request):
    if request.method == "GET":
        fare = request.GET.get('fare')
        fare_class = request.GET.get('fareClass')
        heading = request.GET.get('heading')
        request.session['fare'] = fare
        request.session['fare_class'] = fare_class        
        request.session['heading_date'] = heading  
        print "from ajax request function"      

        return HttpResponseRedirect('/alltest/traveller_info/')  

def traveller_info1(request):
    no_of_adults = range(request.session['adults'])
    no_of_childs = range(request.session['children'])
    date_text = request.session['heading_date']
    fare = request.session['fare']
    fare_class = request.session['fare_class']
    print no_of_adults,"--", no_of_childs, "--", date_text, "==",fare, "--", fare_class
    # no_of_adults = 3
    # no_of_childs = 2
    # date_text = "Madrid - Barcelona - Jan. 30, 2019"

    return render(request,"booking/traveller-information.html",
            {'adults_count':no_of_adults,'child_count':no_of_childs,'date_text':date_text})
   


def api_call(request):  

    # xml = """<?xml version='1.0' encoding='utf-8'?>
    # <a>б</a>"""

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
                    <Departure DepartureDate="2019-01-30T08:00:00.0Z"/>
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
    """%(7000372, 7023060)


    # headers = {'Content-Type': 'application/xml'} # set what your server accepts
    # print requests.post('http://httpbin.org/post', data=xml, headers=headers).text




    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text
       
        result = xmltodict.parse(response)        
        # result = json.dumps(result, ensure_ascii=False)
        # print type(result)
        # result = ast.literal_eval(result).encode('utf8')
        try:
            # result = ast.literal_eval(result).encode('utf8')
            result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))
            
        except:
            pass
        # print "^^^"*40
        # print type(result)
        # print result
        originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
        destinationLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['DestinationLocation']['@Name']
        
        # print "$$"*30
        # print "From Dictionary"
        # print "source --",originLocation
        # print "destination --- >", destinationLocation

        journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']

        result_list = []

        for i in journey:
            result_dict = {}

            # print "&&&"*40
            # print i['JourneySegments']['JourneySegment']
            changes = i['JourneySegments']['JourneySegment']
            # print "length of segments", len(changes)
            result_dict['changes'] = len(changes) - 1           

            deptTimeList = []
            arrivalTimeList = []            
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
                print trainNum, departDateTime, arrivalDateTime,departStationName,arrivaltStationName

                journeyDetails = " Train " + trainNum + " Depart "+departStationName+" at "+depttime+" - Arrive "+arrivaltStationName+" at "+ arrtime
                print "^^^^^^^^^^^^^^^^^^^^^^^^^"
                print journeyDetails

                # print arrtime
                # for key, value in ArrivalStation.items():
                #     print key,value
                # break
                # for key, value in segment.items():
                #     print key,value
                #     trainNum = key['@TrainNumber']
                #     Depart = key['@DepartureDateTime']
                #     Arrival = key['@ArrivalDateTime']
                #     key['DepartureStation']
                #     journeyDetails = "Train" + trainNum + "Depart Chichester at 08:09 - Arrive London Victoria at 09:40" 

            result_dict['departure'] = deptTimeList[0]
            result_dict['arrival'] = arrivalTimeList[-1]
            result_list.append(result_dict)
            break
        # print "=============================="
        # print result_list

        fares = result['ACP_RailAvailRS']['Fares']['Fare']
        print "$$"*50
        fares_data = []
        for i in fares:
            fares_dict = {}
            # print i['@FareReference']  
            # print i['TotalPrice']['@Fare']

            fares_dict['class'] = i['@Class']
            fares_dict['total_price'] = i['TotalPrice']['@Fare']
            fares_data.append(fares_dict)
        print fares_data


        # print journey
    else:
        print "Status code error", Result.status_code
    print "After request"
    print "Response is ---->",Result
    return HttpResponse("Hi")


      


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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse
import xmltodict
import json
import ast
import datetime
from xlrd import open_workbook
import os
from django.conf import settings

# Create your views here.
def allview(request):
    if request.method == "POST":
        date = request.POST.get('txtfromdate')
        print date,"$$$$$"
        # 30-Jan-2019
        dd = datetime.datetime.strptime(str(date), "%d-%m-%Y").strftime('%Y-%m-%d')
        print dd
        return HttpResponse(date)
    else:
        return render(request,"booking/index.html",{})



def ticket_view(request):
    originLoc = "Madrid"
    destinationLoc = "Barcelona"
    # originLoc = "London"
    # destinationLoc = "Paris"
    # originLoc = "Chichester"
    # destinationLoc = "Delamere"
    date = "2019-01-30"
    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    # presentdate=datetime.datetime.today()    
    # print presentdate
    print date_time_obj.date()

    date = date_time_obj.date()    
    
    wb=open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
    worksheet = wb.sheet_by_index(0)
    nc = worksheet.ncols
    nr = worksheet.nrows
    ortakes=[]
    desttakes=[]
    fr=[]
    # dict1={}
    orgLocCode = 0
    countryCode = 0
    for cr in range(1, nr):
        firstcol=worksheet.cell_value(cr, 1).encode('utf-8')
        if firstcol == originLoc :
            orgLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))            
        if firstcol == destinationLoc :
            destLocCode = int(worksheet.cell_value(cr, 0))
            countryCode = int(worksheet.cell_value(cr, 2))
    # print orgLocCode, destLocCode, "^^^^"

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
        """%(orgLocCode, destLocCode)

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Before request"
    Result = requests.post(serURL, data=xml, headers=headers)
    if Result.status_code == 200:
        response = Result.text             
        result = xmltodict.parse(response)        
        try:            
            result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))            
        except:
            pass        
        # print "***"*30
        if result['ACP_RailAvailRS'].get('OriginDestinationOptions') is not None:

            originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
            destinationLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['DestinationLocation']['@Name']                                   

            journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys']['Journey']

            result_list = []
            fareRPHS_List = []

            for index,i in enumerate(journey, start=1):
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
                    journeyDetails['train'] = trainNum
                    journeyDetails['dept_station'] = departStationName
                    journeyDetails['dept_time'] = depttime
                    journeyDetails['arr_station'] = arrivaltStationName                
                    journeyDetails['arr_time'] = arrtime                
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
                        journeyDetails['train'] = trainNum
                        journeyDetails['dept_station'] = departStationName
                        journeyDetails['dept_time'] = depttime
                        journeyDetails['arr_station'] = arrivaltStationName                
                        journeyDetails['arr_time'] = arrtime                
                        journeyDetailsList.append(journeyDetails)
                   
                result_dict['departure'] = deptTimeList[0]
                result_dict['arrival'] = arrivalTimeList[-1]
                datetimeFormat = '%H:%M:%S'
                timeDuration = datetime.datetime.strptime(result_dict['arrival'], datetimeFormat)\
                    - datetime.datetime.strptime(result_dict['departure'], datetimeFormat)

                result_dict['duration'] = timeDuration
                result_dict['journey_details'] = journeyDetailsList
                result_dict['index'] = index
                result_list.append(result_dict)      

            print "========== fare rph",fareRPHS_List
            fares = result['ACP_RailAvailRS']['Fares']['Fare']


            sample = []
            #####################################################3

            # fares list, farerphs list
            fare_classes_list = []

            for ff in fareRPHS_List:
                li = []
                for j in fares:
                    fare_classes_list.append(str(j['@Class']))  
                    # li = []
                    if len(ff) != 0:
                        for k in ff:
                            
                            if k == j['@FareReference']:
                                dic1 = {}
                                dic1['total_price'] = j['TotalPrice']['@Amount']
                                dic1['fareRefer'] = j['@FareReference']
                                dic1['class'] = j['@Class']
                                dic1[j['@Class']] = j['TotalPrice']['@Amount']
                                dic1['product_name'] = j['@ProductName']

                                # print dic1
                                # pass
                                li.append(dic1)
                    else:
                        li = []
                        ff == j['@FareReference']
                        dic1 = {}
                        dic1['total_price'] = j['TotalPrice']['@Amount']
                        dic1['fareRefer'] = j['@FareReference']
                        dic1['class'] = j['@Class']
                        dic1['product_name'] = j['@ProductName']


                        # print dic1
                        # pass
                        li.append(dic1)
                        sample.append(li)
                sample.append(li)
                # break
            # print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"*20            
            # print sample
            fare_classes_list = list(set(fare_classes_list))
            # print fare_classes_list
            # print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"*20

            ##############################################################

            final_list = []
            dd = {}
            ddd = {}
            for main_index,i in enumerate(sample,start=1):
                print "$$$"
                print index
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
                # ddd[index] = dd
                dd['min'] = min_value
                ddd[main_index] = dd
                # ddd['min'] = min_value



                # else:
                #     ddd{}


                final_list.append(ddd)
                dd = {}
                ddd = {}
                # ddd = {}
            print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"*20   
            print final_list
            # print ddd



            print "lenth of results " , len(result_list)
            print "lenth of final " , len(final_list)
            print "lenth of sample " , len(sample)




            ###################################################33

            # fares_data = []
            # fares_data1 = []            

            # fare_classes_list = []   

                  

            # for fare in fares:                
            #     fare_classes_list.append(str(fare['@Class']))               
                
            #     for fareRPH in fareRPHS_List:
                    
            #         # print "===="*20
            #         # print fareRPH
            #         lll = []
            #         for ff in fareRPH:
            #             fares_dict = {}
            #             if ff == fare['@FareReference']:
            #                 fares_dict['fareRefer'] = fare['@FareReference']
            #                 fares_dict['class'] = fare['@Class']
            #                 fares_dict['total_price'] = fare['TotalPrice']['@Amount']
            #                 fares_dict[fare['@Class']] = fare['TotalPrice']['@Amount']
            #                 fares_dict['product_name'] = fare['@ProductName']
            #             # fares_dict['sale_condition'] = fare['SalesConditions']
            #                 fares_data.append(fares_dict)
            #                 lll.append(fares_dict)
            #         fares_data1.append(lll)
                
            #         # break
            #         # fares_data.append(fares_data1)

            #     # 
                
            #     #         if fares_dict:
            #     #             li.append(fares_dict)
            #     # if len(li) != 0:
            #     #     fares_data.append(li)
            #     # break
            # fare_classes_list = sorted(list(set(fare_classes_list)))

            # print "***"*30
            

            

            # # print "========= calsses ",fare_classes_list
            # # print fares_data1
             
            # n=len(fare_classes_list)

            # final = [fares_data[i * n:(i + 1) * n] for i in range((len(fares_data) + n - 1) // n )] 
            # print "&&"*50

            # print final
            print "After Successfull request"               




            return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":date, "final_result":result_list, "prices_data":sample, 'classes':fare_classes_list, 'result_output':final_list} )        
        else:
            return HttpResponse("Getting Web Service Error")
    else:
        print "Status code error", Result.status_code
        return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":date})  




    
    # return render(request,"booking/tickets.html",{"loc":originLoc,"point":destinationLoc,"dateinfo":date})

def traveller_info(request):
    return render(request,"booking/traveller-information.html",{})


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




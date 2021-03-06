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
from models import Cart, CartProducts, CartProductPassengers, CartProductDetails
from djmoney.money import Money
import pickle, uuid

# Create your views here.
def allview(request):
    """ 
    This view to collect all details from Home Page
    """
    
    if request.method == "POST":
        print request.POST
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

        request.session.modified = True
        # return HttpResponse("hello")
        return HttpResponseRedirect('/alltest/ticket/')        
    else:
        return render(request,"booking/index.html",{})

def childAges(request):
    ''' 
    Non-Adults data storing into session 
    '''
    request.session.modified = True

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

    if request.method == "POST":
        print "hi"
        print request.POST

        request.session.modified = True
        ''' fare '''
        fare = request.POST.get('fare', False)
        if fare:
            request.session['fare'] = fare

        ''' fare class'''

        fare_class = request.POST.get('fareclass', False)
        if fare_class:
            request.session['fare_class'] = fare_class

        ''' fare reference '''
        fare_ref = request.POST.get('farereference', False)
        if fare_ref:
            request.session['fare_ref'] = fare_ref
        
        ''' heading '''
        heading = request.POST.get('header', False)
        if heading:
            request.session['heading'] = heading

        ''' adults '''
        no_of_adults = request.POST.get('adults_count', False)
        if no_of_adults:
            request.session['adult_count'] = no_of_adults
        
        ''' childs'''
        no_of_childs = request.POST.get('child_count', False)
        if no_of_childs:
            request.session['child_count'] = no_of_childs

        # print "====================$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"    
        # print no_of_adults,"--", no_of_childs, "--", heading, "==",fare, "--", fare_class
        # print "====================$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

        

        passport = ""
        nationality = ""
        dob = ""
        countryResidence = ""
        birthPlace = ""

        checkingData = request.session.get('resultData')
        if checkingData:   
            passport = str( checkingData[0][0]['is_passport'])
            nationality = str(checkingData[0][0]['is_nationality'])
            dob = str(checkingData[0][0]['is_dob'])
            countryResidence = str(checkingData[0][0]['is_cntryres'])
            birthPlace = str(checkingData[0][0]['is_birthplace'])

        # passport = "true"
        # no_of_adults = range(int(no_of_adults))
        # no_of_childs = range(int(no_of_childs))
            request.session['passport'] = passport
            request.session['nationality'] = nationality
            request.session['dob'] = dob
            request.session['countryResidence'] = countryResidence
            request.session['birthPlace'] = birthPlace

        request.session.modified = True


        # print passport,nationality, dob, type(passport), type(nationality), type(dob)

        return HttpResponseRedirect('/alltest/traveller_info')


        # return render(request,"booking/traveller-information.html",
        #         {'adults_count':no_of_adults,'child_count':no_of_childs,
        #         'date_text':heading, 'passport':passport, 'dob':dob, 'nationality':nationality,
        #         'country_residence':countryResidence,'birth_place':birthPlace})
        
    else:


        ErroMessage = ""
        originLoc = request.session['origin']
        destinationLoc = request.session['destination']
        date_string = request.session['deptDate']+"T"+request.session['deptTime']
        date_time_obj = datetime.strptime(request.session['deptDate'], '%Y-%m-%d')     
        display_date = date_time_obj.date()
        no_of_adults = request.session['adults'] 
        no_of_childs = request.session['children']   
        child_ages = request.session.get('child_ages')
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
        # print xml_data 

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

                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get('OriginLocation') is not None:
                    originLocation = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation']['@Name']
                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get('DestinationLocation') is not None:
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
                        departStationCode = departStation['@LocationCode']
                        arrivaltStation = segment['ArrivalStation']
                        arrivaltStationName = arrivaltStation['@Name']
                        arrivaltStationCode = arrivaltStation['@LocationCode']


                        depttime = departDateTime.split("T")[-1]
                        deptTimeList.append(depttime)
                        arrtime = arrivalDateTime.split("T")[-1]
                        arrivalTimeList.append(arrtime)

                        journeyDetails = {}
                        journeyDetails['train'] = str(trainNum)
                        journeyDetails['dept_station'] = str(departStationName)
                        journeyDetails['dept_station_code'] = str(departStationCode)                                            
                        journeyDetails['dept_time'] = str(depttime)
                        journeyDetails['arr_station'] = str(arrivaltStationName)
                        journeyDetails['arr_station_code'] = str(arrivaltStationCode)
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
                            departStationCode = departStation['@LocationCode']
                            arrivaltStation = segment['ArrivalStation']
                            arrivaltStationName = arrivaltStation['@Name']
                            arrivaltStationCode = arrivaltStation['@LocationCode']


                            depttime = departDateTime.split("T")[-1]
                            deptTimeList.append(depttime)
                            arrtime = arrivalDateTime.split("T")[-1]
                            arrivalTimeList.append(arrtime)

                            journeyDetails = {}
                            journeyDetails['train'] = str(trainNum)
                            journeyDetails['dept_station'] = str(departStationName)
                            journeyDetails['dept_station_code'] = str(departStationCode)                        
                            journeyDetails['dept_time'] = str(depttime)
                            journeyDetails['arr_station'] = str(arrivaltStationName)
                            journeyDetails['arr_station_code'] = str(arrivaltStationCode)                        
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

                print "============================"
                print result_list
                print "$$$$$$$$$$$$$$$$$$$$$$"
                with open(os.path.join(settings.MEDIA_ROOT, "result_list.txt"), 'w' ) as file1:
                    # file1.write(result_list)
                    pickle.dump(result_list, file1)
                    
                if result['ACP_RailAvailRS'].get('Fares') is not None:
                    fares = result['ACP_RailAvailRS']['Fares']['Fare']            
                    sample = []        
                    fare_classes_list = []

                    for ff in fareRPHS_List:
                        li = []
                        for j in fares:
                            clas = j['@Class']
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
                    # print "$$$###"*40
                    # print sample
                    # print "$$$###"*40
                    final_list = []
                    dd = {}
                    ddd = {}
                    fare_ref_list = []
                    f_d = {}
                    f_dd = {}
                    for main_index,i in enumerate(sample):                
                        min_value = 0
                        min_value_list = []
                        for kk in i:        
                            if kk['product_name'] not in dd:                        
                                for index, class1 in enumerate(fare_classes_list):
                                    if kk.get(class1) is not None:
                                        list1 = {}   
                                        list1[class1] = kk[class1]
                                        list1[kk[class1]] = kk['fareRefer']                                   
                                        dd[kk['product_name']] = list1 

                                        list2 = {}
                                        list2[class1] = kk['fareRefer']
                                        f_d[kk['product_name']] = list2                                
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
                                        name[kk[class1]] = kk['fareRefer']                              
                                        dd[kk['product_name']] = name

                                        name1 = f_d.get(kk['product_name'])
                                        name1[class1] = kk['fareRefer']
                                        f_d[kk['product_name']] = name1

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

                        f_dd[main_index] = f_d


                        
                        if result_list[main_index]['index'] == main_index:
                            result_list[main_index]['lowest_price'] = min_value                    

                        final_list.append(ddd)
                        fare_ref_list.append(f_dd)


                        dd = {}
                        ddd = {} 
                        f_d = {}
                        f_dd = {}
                    print "=================================="
                    print final_list
                    # print "**********************"
                    # print fare_ref_list
                    print "After successfull response" 
                    request.session['resultData'] = sample
                    request.session.modified = True
                    return render(request,"booking/tickets.html",
                        {"loc":originLoc,"point":destinationLoc,"dateinfo":display_date, 
                        "final_result":result_list, "prices_data":sample, 'classes':fare_classes_list, 
                        'result_output':final_list, 'fare_refs':fare_ref_list ,'adults':no_of_adults, 'childs':no_of_childs,"Error":ErroMessage} )        
            

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



def traveller_info(request):
    ''' 
    Passengers Page view 
    '''
    if request.method == "POST":
        print "hi"
        print request.POST
        print "################"
        adult_count  = child_count = fare = fare_class = fare_ref = ''
        if request.session:
            # print request.session.get('fare')
            # print request.session.get('fare_ref')
            # # print request.session.get('fare_class')
            # print request.session.get('heading')
            fare_class = request.session.get('fare_class')
            if fare_class:
                request.session['fare_class'] = fare_class
            fare_ref = request.session.get('fare_ref')
            if fare_ref:
                request.session['fare_ref'] = fare_ref
            fare = request.session.get('fare')
            if fare:
                request.session['fare'] = fare
            adult_count = request.session.get('adult_count')
            if adult_count:
                request.session['adult_count'] = adult_count
            child_count =  request.session.get('child_count')
            if adult_count:
                request.session['child_count'] = child_count

        passengers_info = json.loads(request.POST.get('passengersData'))

        n = passengers_num = int(adult_count)+int(child_count)

        
        my_list=passengers_info[2:]
        my_list = my_list[:len(my_list)-4]
        n = len(my_list)/passengers_num

        print fare, fare_class, passengers_num, my_list, n
        final_passengers_list = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]     

        print final_passengers_list
        passengers_data = []
        for i in final_passengers_list:
            del i[0]
            passengers_data.append(i)

        print "=================="
        print passengers_data

        # if len(final_passengers_list) == passengers_num:
        #     print "lengths and count is equal"       

        request.session['passengers_Data'] = passengers_data
        request.session['passengers_num'] = passengers_num

        request.session.modified = True

        # return HttpResponse("post method")
        return HttpResponseRedirect('/alltest/checkinfo')



    else:
        print "else"
        heading = ""
        no_of_adults = ''
        no_of_childs = ''
        passport = ''
        nationality = ''
        dob = ''
        countryResidence = ''
        birthPlace = ''

        if request.session:
            heading = request.session['heading']
            no_of_adults = range(int(request.session['adult_count']))
            no_of_childs = range(int(request.session['child_count']))    
            passport = request.session.get('passport')
            nationality = request.session.get('nationality')
            dob = request.session.get('dob')
            countryResidence = request.session.get('countryResidence')
            birthPlace = request.session.get('birthPlace')
            print "passenger pager else condtion"
            print heading, no_of_adults, no_of_childs, passport, nationality, dob, countryResidence, birthPlace
        
        return render(request,"booking/traveller-information.html",
            {'adults_count':no_of_adults,'child_count':no_of_childs,
            'date_text':heading, 'passport':passport, 'dob':dob, 'nationality':nationality,
            'country_residence':countryResidence,'birth_place':birthPlace})
    

def getCartProductDetails(ref):
    """
        Cart Product Details Data (For displaying purpose only)
    """
    print "GEt Details"

    result_list_data = []
    with open(os.path.join(settings.MEDIA_ROOT, "result_list.txt"), 'r' ) as file1:
        result_list_data = pickle.load(file1)

    dic = {}
    for i in result_list_data:        
        for j1 , j2  in i.items():            
            if j1 == 'fareRPHS_List':                
                j2 = [int(x.encode('utf-8')) for x in j2]                
                if ref in j2:                   
                    dic[ref] = i['journey_details']
                else:
                    pass
    data = {}
    for i in dic[ref]:
        data = i

    return data
        




def checkinfodeatil(request):
    ''' 
    Cart Page view 
    '''
    if request.method == "POST":
        return HttpResponse("Coming Soon")
    else:
        #  session id creation with uuid

        request.session.modified = True
        request.session['id'] = str(uuid.uuid4())

        fare = fare_ref = passengers = passengers_num = fare_class = ''

        if request.session:
            fare = request.session.get('fare')
            fare_ref = request.session.get('fare_ref')
            passengers_data = request.session.get('passengers_Data')
            passengers_num = request.session.get('passengers_num')
            fare_class = request.session.get('fare_class')
        
        print fare_class , fare_ref, fare , passengers , passengers_num       

        # To display Cart Product details function
        cart_prod_details = getCartProductDetails(int(fare_ref))
        print cart_prod_details
        print "@@$%%$#@"*20
        print passengers

        data_from_models = cartModelsDataCreation(request,fare ,fare_class,passengers_num,cart_prod_details , passengers=passengers_data)

        print "from database ---- >",data_from_models
        print type(data_from_models)

        trainNumber = deptStation = deptTime = arrStation = arrTime = ''
        trainCategory = fare_class
        fare = data_from_models[1]
        passengers_num = data_from_models[2]
        for i in data_from_models[0]:
            trainNumber = i['train'] 
            deptStation = i['from_station']
            deptTime = i['departure_date']
            arrStation = i['to_station']
            arrTime = i['arrival_date']
            trainCategory = i['train_category']
        # for i, j in cart_prod_details.items():
        #     if i == 'train':
        #         trainNumber = j            
        #     if i == 'dept_station':
        #         deptStation = j
        #     if i == 'dept_time':
        #         deptTime = j
        #     if i == 'arr_station':
        #         arrStation = j
        #     if i == 'arr_time':
        #         arrTime = j

        print "+++++++++++++++++++++++++++"
        print "-------------", trainNumber, deptStation,deptTime,arrStation,arrTime, trainCategory


        return render(request,'booking/checkout.html',{'cartDetails':'cart_prod_details',
            'Train':trainNumber, 'DeptStation':deptStation, 'DeptTime':deptTime, 
            'ArrStation':arrStation, 'ArrTime':arrTime,"passengercount":passengers_num,
            "faredata":fare, 'fareClass':trainCategory})

def cartModelsDataCreation(request, fare,fare_class,passengers_num, prodDetails, passengers=[]):
    """
        Cart related models data insertion 
    """

    #  Cart Creation
    request.session.modified = True
    session_id = request.session['id']
    # print "before cart model creation"

    cartId = 0
    cart_details = Cart.objects.create(sessionId=session_id,created_date=datetime.now(),booking_ref='',
    user_id=124,agent_ref='second record',notes='updating second cart',status=0,
    currency_id=0,netprice=Money(fare, 'GBP'))

    cart_details = Cart.objects.filter(sessionId=session_id).values()
    print cart_details
    print "$$$$$$$$$"
    price = ""
    for i in cart_details:
        cartId = i['id']
        price = i['netprice']
    # print "after cart model creation"



    #  Cart Products Creation

    cartProductId = 0
    cartProduct = CartProducts.objects.filter(cart_id=cartId)
    print cartProduct
    pass_count = 0
    if cartProduct:
        for i in cartProduct:
            cartProductId = i.cart_id
    else:
        print "cart products else condition"           
        cartProduct = CartProducts.objects.create(cart_id=cartId,product_name=str(fare_class),product_id=1,
        status=0,netprice=Money(fare, 'GBP'),passengers_num=int(passengers_num))
        cartProduct = CartProducts.objects.filter(cart_id=cartId)
        for i in cartProduct:
            cartProductId = i.cart_id
            pass_count = i.passengers_num


    # Cart Product Details Creation

    prodDetailsId = 0
    productDetails = CartProductDetails.objects.filter(cart_product_id=cartProductId)
    if productDetails:
        print "cart product details if condition" 

    else:
        print "cart product details else condition"  

        productDetails = CartProductDetails.objects.create(
            cart_product_id=cartProductId,from_station=str(prodDetails['dept_station']),
        to_station=str(prodDetails['arr_station']),from_code=str(prodDetails['dept_station_code']),to_code=str(prodDetails['arr_station_code']),
        departure_date=str(prodDetails['dept_time']),arrival_date=str(prodDetails['arr_time']),train=str(prodDetails['train']),train_category=str(fare_class))
        print "cart product passsenger  created" 
        productDetails = CartProductDetails.objects.filter(cart_product_id=cartProductId).values()
        print str(prodDetails['dept_time'])
        print productDetails
        # for i in productDetails:
        #     print i.train
        #     print "train no --"*10

    # print productDetails 
    # print "============="
    # print cartProductId
    # print cartProduct 
    # print passengers  


    passengersId = 0
    cartPassengers = CartProductPassengers.objects.filter(cart_product_id=cartProductId)
    if cartPassengers:
        print "cart product passengers if condition" 
        # for i in cartPassengers:
        #     passengersId = i.cart_product_id
    else:
        print "cart product passengers else condition" 
        # cartPassengers = CartProductPassengers.objects.create(cart_product_id=cartProductId,first_name="sunitha",
        # last_name="swain",dob=datetime.now(),nationality="false", passport="false")
        # print "cart product passsenger  created"

        # for passenger in passengers:
        #     pass




    return [productDetails,price, pass_count]





def summarydetail(request):
    return render(request,'booking/summary.html',{})
def summary1deta(request):
    return render(request,'booking/summary1.html',{})
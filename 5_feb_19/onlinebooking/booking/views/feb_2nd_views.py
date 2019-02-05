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
    ''' 
    Non-Adults data storing into session 
    '''
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
                print fare_classes_list        
                print "$$$###"*40
                print sample
                print "$$$###"*40
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
                # print "=================================="
                # print final_list
                print "After successfull response" 
                request.session['resultData'] = sample
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



# def traveller_ajax_info(request):
#     if request.method == "GET":
#         adults = request.GET.get('adults_num')
#         childs = request.GET.get('child_num')
#         date_text = request.GET.get('date_text')

#         return render(request,"booking/traveller-information.html",
#             {'adults_count':adults,'child_count':childs, 'date_text':date_text})
#         # return HttpResponse("test")
#     else:
#         pass




def passenger_page_info1(request):
    ''' 
    passengers page ajax view to store data into session
    '''
    if request.method == "GET":
        print request.GET
        fare = request.GET.get('fare')
        fare_class = request.GET.get('fareClass')
        heading = request.GET.get('heading')
        request.session['fare'] = fare
        request.session['fare_class'] = fare_class        
        request.session['heading_date'] = heading 

        print "from ajax request function"      

        return HttpResponseRedirect('/alltest/traveller_info/')  

def traveller_info(request):
    ''' 
    Passengers Page view 
    '''
    no_of_adults = range(request.session['adults'])
    no_of_childs = range(request.session['children'])
    date_text = request.session['heading_date']
    fare = request.session['fare']
    fare_class = request.session['fare_class']
    checkingData = request.session['resultData']
    # print no_of_adults,"--", no_of_childs, "--", date_text, "==",fare, "--", fare_class
    # print "====================$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

    passport = str( checkingData[0][0]['is_passport'])
    nationality = str(checkingData[0][0]['is_nationality'])
    dob = str(checkingData[0][0]['is_dob'])

    passport = True
    # nationality = True
    # dob = True

    print passport,nationality, dob, type(passport), type(nationality), type(dob)


    return render(request,"booking/traveller-information.html",
            {'adults_count':no_of_adults,'child_count':no_of_childs,
            'date_text':date_text, 'passport':passport, 'dob':dob, 'nationality':nationality})
   



def checkinfodeatil(request):
    ''' 
    Cart Page view 
    '''
    passengers_info = request.session['passengers_Data']
    print "3333333"
    print passengers_info
    print "55555"*20
    print request.session

    fare = str(request.session['fare'])
    # fare = str(fare.split('.')[0])
    fare = float(fare)
    print type(fare)




    all_data = {}
    all_data['passengers'] = passengers_info
    all_data['fare'] = fare
    checkingData = request.session['resultData']
    all_data['passport'] = str( checkingData[0][0]['is_passport'])
    all_data['nationality'] = str(checkingData[0][0]['is_nationality'])
    all_data['dob'] = str(checkingData[0][0]['is_dob'])
    all_data['no_of_adults'] = request.session['adult_count']
    all_data['no_of_childs'] = request.session['child_count']
    passengers_num = request.session['adult_count']+request.session['child_count']

    all_data['passengers_num'] = passengers_num

    print len(passengers_info), "total "

    final = [passengers_info[i * passengers_num:(i + 1) * passengers_num] for i in range((len(passengers_info) + passengers_num - 1) // passengers_num )] 
    print "$$$$$$"*30
    print final




    li = []

    print all_data
    li.append(all_data)


    # return HttpResponse(li)


    # fare1 = int(fare)

    # <django.contrib.sessions.backends.db.SessionStore object at 0x7f7788257790>
    # print request.session.id

    #  Cart Creation

    cart_details = Cart.objects.filter(id=13)
    cartId = 0
    if cart_details:
        print "cart  if condition"          
        for i in cart_details:
            print i.sessionId, i.created_date,i.netprice
            cartId = i.id
            print "success"
    else:
        print "cart else condition"
        cart_details = Cart.objects.create(sessionId=1235,created_date=datetime.now(),booking_ref='',
        user_id=124,agent_ref='second record',notes='updating second cart',status=0,
        currency_id=0,netprice=Money(fare, 'GBP'))
        for i in cart_details:
            print i.sessionId, i.created_date,i.netprice
            cartId = i.id                  
        # pass

    #  Cart Products Creation

    cartProductId = 0
    cartProduct = CartProducts.objects.filter(cart_id=cartId)
    print cartProduct
    
    if cartProduct:
        print "cart products if condition"
        for i in cartProduct:
            print i,"========"
            cartProductId = i.cart_id
    else:
        print "cart products else condition"        
        cartProduct = CartProducts.objects.create(cart_id=cartId,product_name='Standard',product_id=1,
        status=0,netprice=Money(fare, 'GBP'),passengers_num=3)
        print cartProduct
        for i in cartProduct:
            cartProductId = i.cart_id
        print "cartProduct created"


        # pass
    print "==========="
    print cartProductId


    # Cart Product Details Creation

    prodDetailsId = 0
    productDetails = CartProductDetails.objects.filter(cart_product_id=cartProductId)
    if productDetails:
        print "cart product details if condition"  
        # for i in productDetails:
        #     prodDetailsId = i.cart_product_id

    else:
        print "cart product details else condition"  
        productDetails = CartProductDetails.objects.create(

            cart_product_id=cartProductId,from_station="",
        to_station="",from_code="",to_code="",departure_date="",
        arrival_date="",train="",train_category="")
        print "cart product passsenger  created"        


    print productDetails 
    print cartProductId
    print cartProduct    


    passengersId = 0
    cartPassengers = CartProductPassengers.objects.filter(cart_product_id=cartProductId)
    if cartPassengers:
        print "cart product passengers if condition" 
        # for i in cartPassengers:
        #     passengersId = i.cart_product_id
    else:
        print "cart product passengers else condition" 
        cartPassengers = CartProductPassengers.objects.create(cart_product_id=cartProductId,first_name="sunitha",
        last_name="swain",dob=datetime.now(),nationality="false", passport="false")
        print "cart product passsenger  created"



    return render(request,'booking/checkout.html',{})



def checkinfodeatil1(request):
    '''
        Passengers information is storing into session 
    '''
    if request.method=="GET":
        # dictap=request.GET.get("passengers")
        print "from traveller-information ajax request"
        # dictap = request.GET.getlist('passengers')
        # print request.GET

        passengers_info = json.loads(request.GET.get('passengers'))
        adult_count = request.GET.get('adult_num')
        child_count = request.GET.get('child_num')
        print adult_count

      

        print passengers_info
      
        print child_count
        request.session['passengers_Data'] = passengers_info
        request.session['adult_count'] = len(eval(adult_count))
        request.session['child_count'] = len(eval(child_count))

        # print type(products_priorities)
        # print len(products_priorities)


        return HttpResponse(passengers_info)


        # return render(request,'booking/checkout.html',{})
    else:
        return render(request,'booking/checkout.html',{})
def summarydetail(request):
    return render(request,'booking/summary.html',{})
def summary1deta(request):
    return render(request,'booking/summary1.html',{})
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

from onlinebooking import settings

############## logging ###################

# importing module
import logging
from logdna import LogDNAHandler

options = {
    'hostname': 'desktop',
    'ip': '10.0.0.5',
    'mac': 'C0:FF:EE:C0:FF:EE'
}

options['index_meta'] = True

# Creating an object
logger = logging.getLogger('logdna')

logger.setLevel(logging.INFO)

test = LogDNAHandler(settings.LOGDNA_INGEST_KEY, options)
# print settings.LOGDNA_INGEST_KEY
# print test
# log.addHandler(test)

# log.warn("Warning message", {'app': 'bloop'})
# log.info("Info message")

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


##########

# Create your views here.
def allview(request):
    """
    This view to collect all details from Home Page
    """
    # uuid_id = str(uuid.uuid4())
    # request.session['sessionid'] = uuid_id
    if request.method == "POST":
        print "post method"

        if request.session.get('sessionid') is None:
            uuid_id = str(uuid.uuid4())
            request.session['sessionid'] = uuid_id
        else:
            session_id = request.session.get('sessionid')
        # print request.POST

        originStattion = request.POST.get('txtfromstation')
        destStattion = request.POST.get('txttostation')
        departureDate = request.POST.get('txtfromdate')
        departureTime = request.POST.get('Ddldeptime')
        returnDate = request.POST.get('txttodate')
        returnTime = request.POST.get('DdlReturntime')
        numAdults = request.POST.get('DdlAdults')
        numChilds = request.POST.get('DdlNonAdults')
        childAges = json.loads(request.POST.get('childAges'))

        if departureDate:
            date_string = str(departureDate)
            print departureDate, returnDate
            format1 = "%d-%b-%Y"
            format2 = "%Y-%m-%d"
            departureDate = datetime.strptime(date_string, format1).strftime(format2)
        # retn_date = datetime.strptime(str(returnDate), format1).strftime(format2)


        request.session['origin'] = str(originStattion)
        request.session['destination'] = str(destStattion)
        request.session['deptDate'] = str(departureDate)
        request.session['deptTime'] = str(departureTime)
        # request.session['returnDate'] = str(retn_date)
        # request.session['returnTime'] = str(returnTime)        
        request.session['adults'] = int(numAdults)
        request.session['children'] = int(numChilds)
        request.session['child_ages'] = list(childAges)
        request.session.modified = True
        
        # return HttpResponse("coming")
        return HttpResponseRedirect('/alltest/ticket/')
    else:
        print "Else"
        session_id = request.session.get('sessionid')
        request.session['sessionid'] = session_id
        print session_id
        request.session.modified = True
        return render(request, "booking/index_new.html", {})


def ticket_view(request):
    """
    Point To Point Tickets generating view
    """

    if request.method == "POST":
        session_id = request.session.get('sessionid')
        request.session.modified = True
        ''' fare '''
        fare = request.POST.get('fare', False)
        if fare:
            request.session['fare_val'] = fare
        ''' fare class'''
        fare_class = request.POST.get('fareclass', False)
        if fare_class:
            request.session['fare_class'] = fare_class
        ''' fare reference '''
        fare_ref = request.POST.get('fareRef', False)
        if fare_ref:
            request.session['fareRef'] = fare_ref
        ''' heading '''
        heading = request.POST.get('header', False)
        if heading:
            request.session['heading'] = heading
        ''' adults '''
        no_of_adults = request.POST.get('adults_count', False)
        if no_of_adults:
            request.session['adults_count'] = no_of_adults
        ''' childs'''
        no_of_childs = request.POST.get('child_count', False)
        if no_of_childs:
            request.session['child_count'] = no_of_childs

        print fare, fare_class, fare_ref, heading, no_of_adults, no_of_childs, "---"

        passport = nationality = dob = countryResidence = birthPlace = age = ""
        checkingData = request.session.get('resultData')
        fares_data = ''

        # print "$$$"*20
        # print checkingData
        # print "$$$"*30
        ''' filter the selected train data and fares '''
        for dd in checkingData:
            # print dd
            # print "==============="
            journeys = dd.get('journey_details')
            # print len(journeys)
            
            fares = dd.get('fares')

            ################## new 
            for ind , i in enumerate(journeys):
                if fares:
                    # print "faresss-------", fares
                    # print "((((((((((("
                    for innerFares in fares:
                        for fare_ind, fares11 in enumerate(innerFares):
                            # print fares11['fareRefer']
                            if float(fares11['fareRefer']) == float(fare_ref):
                                # print "fare refer if condition"
                                # print fares11['fareRefer'] 
                                # print i['train']

                                # print innerFares[fare_ind]
                                # print journeys[ind]
                                fares_data = innerFares[fare_ind]
                                request.session['segments'] = journeys[ind]
                            break

            ############### new end 
            # print len(fares)
            # print fares
            # for ind, i in enumerate(journeys):
            #     print "++++", i 
            #     break
            #     if i['train'] == train_no:
            #         print "after satisfying the condtion"
            #         print journeys[ind]
            #         request.session['segments'] = journeys[ind]
            # break
            # if fares:
            #     print len(fares)
            #     print fares
            #     for fares1 in fares:  
            #         for ind, i in enumerate(fares1):
            #             if ((float(i['fare']) == float(fare)) and (str(i['class']) == str(fare_class))):
            #                 # print "fares data"
            #                 fares_data = fares1[ind]
        print "fares -------------"  
        print fares_data
        if fares_data:
            passport = fares_data.get('is_passport')
            nationality = fares_data.get('is_nationality')
            dob = fares_data.get('is_dob')
            countryResidence = fares_data.get('is_cntryres')
            birthPlace = fares_data.get('is_birthplace')
           

            request.session['passport'] = passport
            request.session['nationality'] = nationality
            request.session['dob'] = dob
            request.session['countryResidence'] = countryResidence
            request.session['birthPlace'] = birthPlace
            # request.session['age'] = age

        request.session['sessionid'] = session_id
        request.session.modified = True
        # return HttpResponse("checking")

        return HttpResponseRedirect('/alltest/traveller_info')
    else:
        session_id = request.session.get('sessionid')
        ErroMessage = ""
        originLoc = request.session['origin']
        destinationLoc = request.session['destination']
        date_string = request.session['deptDate'] + "T" + request.session['deptTime']
        date_time_obj = datetime.strptime(request.session['deptDate'], '%Y-%m-%d')
        display_date = date_time_obj.date()
        no_of_adults = request.session['adults']
        no_of_childs = request.session['children']
        child_ages = request.session.get('child_ages')
        ReturnReturnDate = ""
        wb = open_workbook(os.path.join(settings.MEDIA_ROOT, "FE-locations.xlsx"))
        worksheet = wb.sheet_by_index(0)
        nc = worksheet.ncols
        nr = worksheet.nrows
        ortakes = []
        desttakes = []
        fr = []
        orgLocCode = 0
        countryCode = 0
        destLocCode = 0
        for cr in range(1, nr):
            firstcol = worksheet.cell_value(cr, 1).encode('utf-8')
            if firstcol == originLoc:
                orgLocCode = int(worksheet.cell_value(cr, 0))
                countryCode = int(worksheet.cell_value(cr, 2))
            if firstcol == destinationLoc:
                destLocCode = int(worksheet.cell_value(cr, 0))
                countryCode = int(worksheet.cell_value(cr, 2))

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        root = ET.Element("ACP_RailAvailRQ", xmlns="http://www.acprailinternational.com/API/R2",
                          ResponseType="Native-Availability")
        pos = ET.SubElement(root, "POS")
        requestor = ET.SubElement(pos, "RequestorID").text = "RTG-XML"
        rail_avail_info = ET.SubElement(root, "RailAvailInfo")
        origins = ET.SubElement(rail_avail_info, 'OriginDestinationSpecifications')
        origin1 = ET.SubElement(origins, 'OriginLocation', LocationCode="{0}".format(orgLocCode))
        origin2 = ET.SubElement(origins, 'DestinationLocation', LocationCode="{0}".format(destLocCode))
        origin3 = ET.SubElement(origins, 'Departure', DepartureDate="{0}".format(date_string))
        if ReturnReturnDate:
            origin4 = ET.SubElement(origins, 'Return', ReturnDate="{0}".format(""))

        passengers = ET.SubElement(rail_avail_info, 'PassengerSpecifications')
        # for adults
        passtype = ET.SubElement(passengers, 'PassengerType', Age="-1", Quantity="{0}".format(no_of_adults))
        # for childs
        if child_ages:
            for i in child_ages:
                passtype = ET.SubElement(passengers, 'PassengerType', Age=str(i), Quantity="1")
        fare_qual = ET.SubElement(rail_avail_info, 'FareQualifier RateCategory="Regular"')
        responsePt = ET.SubElement(rail_avail_info, 'ResponsePtPTypes')
        responsePt1 = ET.SubElement(responsePt, 'ResponsePtPType').text = "TW"
        mydata = ET.tostring(root)

        xml_data += mydata

        serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailAvailRQ'
        headers = {'content-type': 'application/xml; charset=utf-8'}
        print "Before request"
        Result = requests.post(serURL, data=xml_data, headers=headers)
        if Result.status_code == 200:
            response = Result.text
            request.session['Avail_Rail_response'] = str(response)            
            result = xmltodict.parse(response)            

            try:
                result = ast.literal_eval(json.dumps(result, ensure_ascii=False).encode('utf8'))
                result = result.encode('utf-8')
            except:
                pass
            # print "^^^^^^^^^^^^^^^^^^^^^^^^"
            # print result

            fares_list = []
            # fare_classes_list = []
            #  journeys - > journey - > fares - > segments

            if result['ACP_RailAvailRS'].get('OriginDestinationOptions') is not None:

                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get(
                        'OriginLocation') is not None:
                    originLocation = \
                    result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['OriginLocation'][
                        '@Name']
                if result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'].get(
                        'DestinationLocation') is not None:
                    destinationLocation = \
                    result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption'][
                        'DestinationLocation']['@Name']
                if result['ACP_RailAvailRS'].get('Fares') is not None:
                    fares_list = result['ACP_RailAvailRS']['Fares']['Fare']
                journey = result['ACP_RailAvailRS']['OriginDestinationOptions']['OriginDestinationOption']['Journeys'][
                    'Journey']

                result_list = []
                fareRPHS_List = []
                fare_class_list = []

                for index, i in enumerate(journey):
                    result_dict = {}
                    changes = i['JourneySegments']['JourneySegment']
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

                        depttime1 = departDateTime.split("T")[-1]
                        depttime = departDateTime
                        deptTimeList.append(depttime)
                        arrtime1 = arrivalDateTime.split("T")[-1]
                        arrtime = arrivalDateTime
                        arrivalTimeList.append(arrtime)

                        journeyDetails = {}
                        journeyDetails['train'] = str(trainNum)
                        journeyDetails['dept_station'] = str(departStationName)
                        journeyDetails['dept_station_code'] = str(departStationCode)
                        journeyDetails['dept_time'] = str(depttime1)
                        journeyDetails['arr_station'] = str(arrivaltStationName)
                        journeyDetails['arr_station_code'] = str(arrivaltStationCode)
                        journeyDetails['arr_time'] = str(arrtime1)
                        journeyDetails['dept_date_time'] = str(departDateTime)
                        journeyDetails['arr_date_time'] = str(arrivalDateTime)

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

                            depttime1 = departDateTime.split("T")[-1]
                            depttime = departDateTime
                            deptTimeList.append(depttime)
                            arrtime1 = arrivalDateTime.split("T")[-1]
                            arrtime = arrivalDateTime
                            arrivalTimeList.append(arrtime)

                            journeyDetails = {}
                            journeyDetails['train'] = str(trainNum)
                            journeyDetails['dept_station'] = str(departStationName)
                            journeyDetails['dept_station_code'] = str(departStationCode)
                            journeyDetails['dept_time'] = str(depttime1)
                            journeyDetails['arr_station'] = str(arrivaltStationName)
                            journeyDetails['arr_station_code'] = str(arrivaltStationCode)
                            journeyDetails['arr_time'] = str(arrtime1)
                            journeyDetails['dept_date_time'] = str(departDateTime)
                            journeyDetails['arr_date_time'] = str(arrivalDateTime)
                            journeyDetailsList.append(journeyDetails)

                    result_dict['departure'] = deptTimeList[0]
                    result_dict['arrival'] = arrivalTimeList[-1]
                    datetimeFormat = "%Y-%m-%dT%H:%M:%S"
                    timeDuration = datetime.strptime(str(result_dict['arrival']), datetimeFormat) \
                                   - datetime.strptime(str(result_dict['departure']), datetimeFormat)
                    # print timeDuration
                    # print "++++++++++++++++++++++++"
                    result_dict['arrival'] = str(result_dict['arrival']).split("T")[-1]
                    result_dict['departure'] = str(result_dict['departure']).split("T")[-1]
                    result_dict['duration'] = str(timeDuration)
                    result_dict['journey_details'] = journeyDetailsList
                    result_dict['index'] = index

                    if i.get('FareRPHs') is not None:
                        if type(i['FareRPHs']['FareRPH']) != list:
                            i['FareRPHs']['FareRPH'] = [i['FareRPHs']['FareRPH']]
                        fareRPHS_List.extend(i['FareRPHs']['FareRPH'])

                        fares = i['FareRPHs']['FareRPH']
                        fare_list = []
                        min_value_list = []
                        

                        for r in range(len(fares)):
                            fares_data = []

                            rph = fares[r]
                            for fare in fares_list:
                                fare_dict = {}
                                if fare['@FareReference'] == rph:

                                    fareDetails = {}

                                    fareDetails['fare'] = float(fare['TotalPrice']['@Amount'])
                                    min_value_list.append(float(fare['TotalPrice']['@Amount']))
                                    clas = fare['@Class']
                                    if clas.__contains__('-'):
                                        clas = clas.split("-")[-1]
                                    fareDetails['class'] = str(clas).strip()
                                    fare_class_list.append(clas)

                                    # prod_name = str(fare['ProdMarketingName']).replace('<div id=\"DisplayName\">', "")
                                    # prod_name = prod_name.replace("</div>", "")
                                    fareDetails['product_name'] = fare['@ProductName']                                        
                                    fareDetails['fareRefer'] = fare['@FareReference']
                                    fareDetails['sales_condition'] = fare['SalesConditions'][
                                        '@RefundPolicy']
                                    fareDetails['ticket_option'] = fare['@TicketOption']
                                    fareDetails['is_passport'] = fare['@PassportRequired']
                                    fareDetails['is_dob'] = fare['@DateOfBirthRequired']
                                    fareDetails['is_paxname'] = fare['@PaxNameRequested']
                                    fareDetails['is_cntryres'] = fare['@CntryResidenceRequired']
                                    fareDetails['is_nationality'] = fare['@NationalityRequired']
                                    fareDetails['is_birthplace'] = fare['@PlaceOfBirthRequired']
                                    fareDetails['is_email'] = fare['@EmailRequired']
                                    if fare['PassengerTypePrices'].get('MixDetails'):
                                        fareDetails['is_age'] = \
                                            fare['PassengerTypePrices']['MixDetails'][
                                                'PassengerPlaceholder'][0]['@Age']
                                    fares_data.append(fareDetails)
                                    

                                    break
                            

                            fare_list.append(fares_data)

                        result_dict['fares'] = fare_list                        
                        min_value_list = [float(x) for x in min_value_list]
                        result_dict['lowest_price'] = min(min_value_list)
                        # print result_dict['lowest_price']

                    result_list.append(result_dict)


                # print result_list
                request.session['response_result'] = result_list               

                if fareRPHS_List:
                    final_list = []
                    dd = {}
                    ddd = {}

                    for main_index, result in enumerate(result_list):                                              
                        if result.get('fares'):
                            for ind1,fare in enumerate(result['fares']):
                                fare = fare[0]
                                # print "____^^^^^^^", fare
                                fare_class_list = list(set([str(x).strip() for x in fare_class_list]))
                                fare_class_list = sorted(fare_class_list)
                                if fare['product_name'] not in dd:                                   
                                    dict1 = {}
                                    li = []
                                    li.append(float(fare['fare']))
                                    li.append(float(fare['fareRefer']))

                                    dict1[fare['class']] = li
                                    # dict1[fare['fare']] = float(fare['fareRefer'])

                                    dd[fare['product_name']] = dict1
                                else:
                                    name = dd.get(fare['product_name'])
                                    li = []
                                    li.append(float(fare['fare']))
                                    li.append(float(fare['fareRefer']))
                                    name[fare['class']] = li
                                    # name[fare['fare']] = float(fare['fareRefer'])
                                # print "inner loop"
                                # print dd                        
                        ddd[main_index] = dd               
                        dd = {}


                    print "After successfull response"
                    # print ddd
                    final_list.append(ddd)
                    fare_class_list = sorted(fare_class_list)

                    # print fare_class_list


                    request.session['resultData'] = result_list
                    request.session['sessionid'] = session_id
                    request.session.modified = True
                    return render(request, "booking/tickets.html",
                                  {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                                   "final_result": result_list, "prices_data": 'sample', 'classes': fare_class_list,
                                   'result_output': final_list, 'adults': no_of_adults,
                                   'childs': no_of_childs, "Error": ErroMessage})


                else:
                    return render(request, "booking/tickets.html",
                                  {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                                   "final_result": result_list, "prices_data": [], 'classes': [],
                                   'result_output': [], 'adults': no_of_adults, 'childs': no_of_childs,
                                   "Error": ErroMessage})
            else:
                ErroMessage = "Getting Web Service Error"
                response = LogDNAHandler(settings.LOGDNA_INGEST_KEY, Result)
                logger.addHandler(response)
                logger.info("Fares are not Available for trains")
                logger.debug("Fares are not Available for trains")

                return render(request, "booking/tickets.html",
                              {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date,
                               "Error": ErroMessage})
        else:
            ErroMessage = "No Response"
            response = LogDNAHandler(settings.LOGDNA_INGEST_KEY, Result)
            logger.addHandler(response)
            logger.info("Fares are not Available for trains")
            logger.debug("Response is not Available from API")
            return render(request, "booking/tickets.html",
                          {"loc": originLoc, "point": destinationLoc, "dateinfo": display_date, "Error": ErroMessage})


def traveller_info(request):
    '''
    Passengers Page view
    '''
    if request.method == "POST":
        session_id = request.session.get('sessionid')
        adult_count = child_count = fare = fare_class = fare_ref = train_no = ''
        if request.session:
            fare_class = request.session.get('fare_class')
            if fare_class:
                request.session['fare_class'] = fare_class
            # fare_ref = request.session.get('fare_ref')
            # if fare_ref:
            #     request.session['fare_ref'] = fare_ref
            train_no = request.POST.get('trainNum', False)
            if train_no:
                request.session['train'] = train_no
            fare = request.session.get('fare_val')
            if fare:
                request.session['fare_val'] = fare
            adult_count = request.session.get('adults_count')
            if adult_count:
                request.session['adults_count'] = adult_count
            child_count = request.session.get('child_count')
            if child_count:
                request.session['child_count'] = child_count
            else:
                child_count =0
        passengers_info = json.loads(request.POST.get('passengersData'))
        passengers_num = int(adult_count) + int(child_count)
        my_list = passengers_info[2:]
        my_list = my_list[:len(my_list) - 4]
        n = len(my_list) / passengers_num
        if n != 0:
            final_passengers_list = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n)]
        else:
            final_passengers_list = my_list
        passengers_data = []
        for i in final_passengers_list:
            del i[0]
            passengers_data.append(i)        

        # To display Cart Product details function
        # cart_prod_data = request.session.get('segments')
        # cart_prod_details = {}
        # cart_prod_details['multiple_segments'] = cart_prod_data
        # cart_prod_details
        cart_prod_details = request.session.get('segments')
        # cart_prod_details = getCartProductDetails(request, int(fare_ref))

        print "*********************"
        print cart_prod_details
        # return HttpResponse("wait")
        
        # Storing data in models
        data_from_models = cartModelsDataCreation(request, fare, fare_class, passengers_num, \
                    adult_count, child_count, cart_prod_details, passengers_data)

        trainNumber = deptStation = deptTime = arrStation = arrTime = ''
        trainCategory = fare_class
        request.session.modified = True
        return HttpResponseRedirect('/alltest/checkinfo')
    else:
        session_id = request.session.get('sessionid')
        heading = no_of_adults = passport = no_of_childs = nationality = dob = countryResidence = birthPlace = age = ""

        if request.session:
            heading = request.session['heading']
            no_of_adults = range(int(request.session['adults_count']))
            no_of_childs = range(int(request.session['child_count']))
            passport = request.session.get('passport')
            nationality = request.session.get('nationality')
            dob = request.session.get('dob')
            countryResidence = request.session.get('countryResidence')
            birthPlace = request.session.get('birthPlace')
            # age = request.session.get('age')
            # age = -1
            child_ages = request.session.get('child_ages')
            child_ages = [str(i) for i in child_ages]
            print child_ages

        request.session['sessionid'] = session_id
        request.session.modified = True

        return render(request, "booking/traveller-information.html",
                      {'adults_count': no_of_adults, 'child_count': no_of_childs,'child_ages':child_ages,
                       'date_text': heading, 'passport': passport, 'dob': dob, 'nationality': nationality,
                       'country_residence': countryResidence, 'birth_place': birthPlace})


def getCartProductDetails(request, ref):
    """
        Cart Product Details Data (For displaying purpose only)
    """

    session_id = request.session.get('sessionid')
    result_list_data = request.session['response_result']    

    dic = {}
    dic1 = {}
    for i in result_list_data:
        for j1, j2 in i.items():
            if j1 == 'fareRPHS_List':
                j2 = [int(x.encode('utf-8')) for x in j2]
                if ref in j2:
                    dic[ref] = i['journey_details']
                else:
                    pass
        dic1['multiple_segments'] = i['journey_details']

    data = {}
    if ref in dic:
        for i in dic[ref]:
            data = i
    return dic1


def cartModelsDataCreation(request, fare, fare_class, passengers_num, adult_count, child_count, prodDetails, passengers):
    """
        Cart related models data insertion
    """

    print "model creation views"
    from_station = to_station = dept_date = ""
    session_id = request.session.get('sessionid')
    if request.session.get('origin'):
        from_station = request.session.get('origin')
    if request.session.get('destination'):
        to_station = request.session.get('destination')
    product_name = str(from_station) + "-" + str(to_station)
    if request.session.get('deptDate'):
        dept_date = request.session.get('deptDate')
    sale_value = ""
    data1  = request.session.get('resultFinalData')
    for i in data1  :
        # print i
        for key, value in i.items():            
            sale_value = value['sales']

    # print session_id
    print sale_value

    # print passengers
    for i, j in enumerate(passengers):
        dict1 = {}
        n = []
        for e in j:
            dict1.update(e)
        n.append(dict1)
        passengers[i] = n

    for index, i in enumerate(passengers):
        ll = []
        dict1 = {}
        for j in i:
            if j.get('first_name'):
                dict1.update(j)
            else:
                dict1.update({'first_name': 'false'})
            if j.get('passport'):
                dict1.update(j)
            else:
                dict1.update({'passport': 'false'})
            if j.get('secondname'):
                dict1.update(j)
            else:
                dict1.update({'secondname': 'false'})
            if j.get('nationality'):
                dict1.update(j)
            else:
                dict1.update({'nationality': 'false'})
            if j.get('dob'):
                dict1.update(j)
            else:
                dict1.update({'dob': 'false'})
            if j.get('age'):
                dict1.update(int(j))
            else:
                dict1.update({'age': -1})
        ll.append(dict1)
        passengers[index] = ll

    print "passengers data checking "
    print passengers
    print "passengers-------------"

    ##################################################################
    # New code for inserting data into db
    ##################################################################

    # Cart model data insertion
    cart_id = 0
    cartData = Cart.objects.filter(orderid=session_id)
    if cartData:
        for i in cartData:
            cart_id = i.id
    else:
        addCart = Cart.objects.create(orderid=session_id, created_date=datetime.now(), booking_ref='',
                                  user_id=124, agent_ref='rail booking', notes='adding  cart', status=0,
                                  currency_id=0)
        cart_id = addCart.id

    # Cart Product model data insertion
    cartProduct = CartProducts.objects.create(
        cart_id=cart_id, service=str(fare_class), product_name=product_name, product_id=1,
        status=0, netprice=float(fare), passengers_num=int(passengers_num),adults_num=int(adult_count),non_adults_num=int(child_count),
        start_date=dept_date, Rule=str(sale_value), fare=float(fare), settlementprice=float(fare))

    # Cart Product Details model data insertion

    prod_detailsList = []
    detail = prodDetails
    # for detail in prodDetails['multiple_segments']:
    depDateTime = str(detail['dept_date_time'])
    depDateTime = depDateTime.split('T')
    depDateTime = " ".join(depDateTime)
    depDateTime = datetime.strptime(depDateTime, '%Y-%m-%d %H:%M:%S')
    arrDateTime = str(detail['arr_date_time'])
    arrDateTime = arrDateTime.split('T')
    arrDateTime = " ".join(arrDateTime)
    arrDateTime = datetime.strptime(arrDateTime, '%Y-%m-%d %H:%M:%S')

    prod_detailsList.append(
        CartProductDetails(cart_product_id=cartProduct.id, from_station=str(detail['dept_station']),
                           to_station=str(detail['arr_station']), from_code=str(detail['dept_station_code']),
                           to_code=str(detail['arr_station_code']),
                           departure_date=depDateTime, arrival_date=arrDateTime, train=str(detail['train']),
                           train_category=str(fare_class),service=str(fare_class)))

    CartProductDetails.objects.bulk_create(prod_detailsList)

    print "cart product details created"

    # cart product passegers creation
    aldetails = []
    for passsenger in passengers:
        for i in passsenger:
            title = str(i['first_name']) + str(i['secondname'])
            aldetails.append(CartProductPassengers(cart_product_id=cartProduct.id, first_name=i['first_name'],
                                                   last_name=i['secondname'], dob=datetime.now(),
                                                   nationality=i['nationality'], passport=i['passport'],
                                                   age=int(str(i['age'])), title=title))

    CartProductPassengers.objects.bulk_create(aldetails)
    print "cart product passsengers  created"

    # carts = Cart.objects.filter(orderid=session_id)

    productAllDetails = CartProductDetails.objects.all()
    products = CartProducts.objects.all()

    return [productAllDetails, products]


def checkout_new(request):
    """ Check out page """

    if request.method == "POST":
        print "POST method"
        session_id = request.session.get('sessionid')

        if request.POST.get('removeCart'):
            """ Remove Product from cart """
            remove_cart_id = request.POST.get('removeCart').encode('utf-8')
            print remove_cart_id
            # cart product  details model data removal
            CartProductDetails.objects.filter(cart_product_id=remove_cart_id).delete()            
            # passengers model data removal
            CartProductPassengers.objects.filter(cart_product_id=remove_cart_id).delete()                        
            # cart products model data removal
            CartProducts.objects.filter(id=remove_cart_id).delete()            
            # return HttpResponse("hello")
            # return HttpResponseRedirect("/alltest/checkinfo_new")
            session_id = request.session.get('sessionid')
            # Retrieving the data based on session id
            cart = Cart.objects.filter(orderid=session_id)
            cart_ids = []
            for i in cart:
                cart_ids.append(i.id)
            # print cart_ids 
            cart_products = CartProducts.objects.filter(cart_id__in=cart_ids)
            # print cart_products
            cart_products_ids = []
            for i in cart_products:
                # print i.id
                cart_products_ids.append(i.id)
            cart_products_details = CartProductDetails.objects.filter(cart_product_id__in=cart_products_ids)           
            prod_data = cartProductsData(request, cart_products_details)
            request.session.modified = True
            return render(request, 'booking/checkout_new.html', \
            {'products':cart_products, 'prod_details':prod_data, })
        else:
            print "33333"
            return HttpResponseRedirect("/alltest/checkinfo")
        return HttpResponseRedirect("/alltest/checkinfo")

    else:     

        session_id = request.session.get('sessionid')
        cart = Cart.objects.filter(orderid=session_id)
        cart_ids = []
        for i in cart:
            cart_ids.append(i.id)
        # print cart_ids 
        cart_products = CartProducts.objects.filter(cart_id__in=cart_ids)
        # print cart_products
        cart_products_ids = []
        for i in cart_products:
            # print i.id
            cart_products_ids.append(i.id)
        cart_products_details = CartProductDetails.objects.filter(cart_product_id__in=cart_products_ids)
        prod_data = cartProductsData(request, cart_products_details)
        request.session.modified = True
        return render(request, 'booking/checkout_new.html', \
        {'products':cart_products, 'prod_details':prod_data})


def cartProductsData(request, prod_details):
    list1 = []            
    for i in prod_details:
        dict1 = {}
        dict1['cart_product_id'] = i.cart_product_id  
        dict1['from'] = i.from_station  
        dict1['to'] = i.to_station
        dict1['departure'] = i.departure_date
        dict1['arrival'] = i.arrival_date
        dict1['duration'] = i.arrival_date - i.departure_date
        dict1['train'] = i.train
        list1.append(dict1)
    return list1


def summary_new(request):

    """ Summary Page View """    

    session_id = request.session.get('sessionid')
    cart = Cart.objects.filter(orderid=session_id)
    cart_ids = []
    for i in cart:
        cart_ids.append(i.id)
    # print cart_ids 
    cart_products = CartProducts.objects.filter(cart_id__in=cart_ids)
    # print cart_products
    cart_products_ids = []
    total = 0
    for i in cart_products:
        # print i.id
        total += float(i.netprice)
        cart_products_ids.append(i.id)
    cart_products_details = CartProductDetails.objects.filter(cart_product_id__in=cart_products_ids)             
    prod_data = cartProductsData(request, cart_products_details)    
    request.session.modified = True



    print "joins data start"

    # Pizza.objects.all().prefetch_related('toppings')
    # data = CartProductDetails.objects.select_related('cart_product__cart').filter()
    # print data

    # for i in data:
    #     print dir(i)

    # dd1 = CartProductDetails.objects.all()
    # for d in dd1:
    #     print dir(d)
    #     print "***"
    #     print d.cart_product.product_name
    #     break

    # dd = CartProductDetails.objects.all().select_related('cart_product').prefetch_related('cart_product__cartproductpassengers_set')
    # print dd, "==================="
    # for d in dd:
    #     print dir(d)
    #     print d.cart_product.product_name
    #     print d.cart_product.first_name

    #     # print d.first_name
    #     break
    # CartProducts.objects.filter()

    # d = CartProductDetails.objects.filter(cart_product_id__in=cart_products_ids).prefetch_related(
    #      'cart_product__cartproductpassengers_set')


    # print "DDDD"
    # print d
    # for i in d:
    #     print dir(i)
    #     break

    # data1 = CartProductDetails.objects.select_related('cart_product').filter()
    # print data1

    print "joins data end "


    return render(request, 'booking/summary_new.html', \
        {'products':cart_products,'prod_details':prod_data,'total_price':total})



def summary1_new(request):

    """ Payment Page view """

    session_id = request.session.get('sessionid')
    cart = Cart.objects.filter(orderid=session_id)
    cart_ids = []
    for i in cart:
        cart_ids.append(i.id)
    # print cart_ids 
    cart_products = CartProducts.objects.filter(cart_id__in=cart_ids)
    # print cart_products
    cart_products_ids = []
    total = 0
    for i in cart_products:
        # print i.id
        total += float(i.netprice)
        cart_products_ids.append(i.id)
    cart_products_details = CartProductDetails.objects.filter(cart_product_id__in=cart_products_ids)             
    prod_data = cartProductsData(request, cart_products_details)
    request.session.modified = True    

    return render(request, 'booking/summary1_new.html', \
        {'products':cart_products,'prod_details':prod_data,'total_price':total})


def checking_api(request):    

    xml ="""

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ACP_RailBookRQ xmlns="http://www.acprailinternational.com/API/R2">
    <POS>
        <RequestorID>RTG-XML</RequestorID>
    </POS>
    <RailBookInfo ContactEmail="" POSReference="">
        <SelectedOptions>
            <SelectedOption TicketOption="Etk" IsCreditSale="true" ID="1">
                <ODFare PlaceOfBirthRequired="false" NationalityRequired="false" CntryResidenceRequired="false" EmailRequired="false" PaxNameRequested="true" DateOfBirthRequired="false" PassportRequired="false" TicketOption="Etk" BookingOnRequest="false" PricingOnRequest="false" PaxUnits="1" TravelDate="2019-03-20" UseByTL="2018-12-19" UseAfterTL="2018-12-20" Magic="59C6C1B9790F61A6F5E651F8CC993F9E789C6D50CB6EC23010BCFB2B523807F949ECDCFC8AD443AB56A12794432056952AC488988A0AF1EF35A1AD00D5DA8335BBB3333BD3A55F7DB87578489660E7B65DEA1BBF0DADEF873C5956A06E9A3BA4DC766D485F76EDDAE5C9F48ABDF0A1EEFEC18B7A171124E80C8245A9F304C68FDCF87D1F7E61ED379B7618A2469E8859069EDDB9C5E98C80D2ED3EE3CAC2B90BB1AAC04B7D302ED46D77AB537671EED14462DCD7C4F189348B09A8DF473FBDEF5D055EF7751FDAF0751E7AEBDBF063F7CEDC78C9B8EED666595C746310C7E911645C6846B8D596165A52490DB60C31CAB99D43A98D565867485B5C60AB10C30412AA88A1845808B1424018AAB8E29268AE0A220C2352232AA8D1C2402C629363AAA08232C304472945A1C0D222A645748400869651A899420A41C8E7994299CC22657CE074024FEDE1CFF332451548D77E381F3417F1A074550F57E9A4CD6AE82E81DCE48ED925F8B1BE0100499C4C31020000" FareType="Regular" RouteDescription="ANY PERMITTED - Travel is allowed via any permitted route." ProductName="TICKET on DEPARTURE &amp; RESERVATION -ANYTIME via:ANY PERMITTED - Travel is allowed via any permitted route." ReservationRequired="true" IncludesProtectionPlan="false" ItineraryType="One-Way-Outbound" CurrencyCode="GBP" TicketCount="1" TicketingTimeLimit="2019-03-19T23:59:59.0Z" IsEstimated="false" Class="Standard" FareReference="2">
                    <PassengerTypePrices>
                        <PassengerMixSlice SFDetails="#{'789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB1523034B3D433E002B19D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C9194120E540C5B1B100867B17A74B000000'}" TotalSliceAmount="194.00" TSC="0.00" UnitPrice="194.00" Quantity="1" Code="ADT" SliceID="1">
                            <MixDetails>
                                <PassengerPlaceholder Age="-1"/>
                            </MixDetails>
                        </PassengerMixSlice>
                    </PassengerTypePrices>
                    <TotalPrice ServiceFee="25.0" Net="184.30" Commission="9.70" Amount="194.00" TSC="0.00" Fare="194.00"/>
                    <OriginLocation Country="GB" Name="London Euston" LocationCode="7000021"/>
                    <DestinationLocation Country="GB" Name="Manchester Piccadilly" LocationCode="7000046"/>
                    <SubComponents/>
                    <IntegratedTotalPrice ServiceFee="25.0" Net="184.30" Commission="9.70" Amount="194.00" TSC="0.00" Fare="194.00"/>
                    <IntegratedPassengerTypePrices>
                        <PassengerMixSlice SFDetails="#{'789C538ECE4FCA4A4D2E515488E60ACDCB2C71CE2F2EB1523034B3D433E002B19D4B8B8A3C8BF39D53AC1494DC9D0294B8824B0B0A7232538B4092AE15C9194120E540C5B1B100867B17A74B000000'}" TotalSliceAmount="194.00" TSC="0.00" UnitPrice="194.00" Quantity="1" Code="ADT" SliceID="1">
                            <MixDetails>
                                <PassengerPlaceholder Age="-1"/>
                            </MixDetails>
                        </PassengerMixSlice>
                    </IntegratedPassengerTypePrices>
                    <PossiblePlacePrefs>
                        <PossibleSpecialRequests>
                            <SpecialRequest>Unspecified</SpecialRequest>
                        </PossibleSpecialRequests>
                        <PossibleCompartmentTypes>
                            <CompartmentType>Unspecified</CompartmentType>
                        </PossibleCompartmentTypes>
                        <PossiblePositions>
                            <Position>Unspecified</Position>
                        </PossiblePositions>
                    </PossiblePlacePrefs>
                    <ProdMarketingName>&lt;div id="DisplayName"&gt;TICKET on DEPARTURE &amp; RESERVATION -ANYTIME&lt;/div&gt;</ProdMarketingName>
                    <SalesConditions RefundPolicy="Non-Refundable">
                        <TermsAndConditions MustAcknowledge="true" URL="http://www.acprail.com/railways-terms-and-conditions/TTL-tod-ow-withres-anytime.html"/>
                        <RefundRules>
                            <RefundRule MinimumPenalty="0.0" PenaltyRate="100.0" WithinDateBasis="P0D" DateBasis="Issue" Sequence="1"/>
                        </RefundRules>
                    </SalesConditions>
                </ODFare>
                <OriginDestinationOption>
                    <Journey IsSubComponent="false" JourneyDuration="PT2H5M">
                        <OriginLocation Country="GB" Name="London Euston" CodeContext="UIC" LocationCode="7000021"/>
                        <DestinationLocation Country="GB" Name="Manchester Piccadilly" CodeContext="UIC" LocationCode="7000046"/>
                        <JourneySegments>
                            <JourneySegment>
                                <TrainSegment OperatorName="ATOC" ReservationMode="Optional" CrossBorder="false" TrainServiceType="Train" JourneyDuration="PT2H5M" TrainNumber="0800" ArrivalDateTime="2019-03-21T10:05:00" DepartureDateTime="2019-03-20T08:00:00">
                                    <DepartureStation Country="GB" Name="London Euston" CodeContext="UIC" LocationCode="7000021"/>
                                    <ArrivalStation Country="GB" Name="Manchester Piccadilly" CodeContext="UIC" LocationCode="7000046"/>
                                    <RailAmenities>
                                        <RailAmenity Name="VT"/>
                                    </RailAmenities>
                                    <ClassCodes/>
                                </TrainSegment>
                            </JourneySegment>
                        </JourneySegments>
                        <FareRPHs>
                            <FareRPH>1</FareRPH>
                            <FareRPH>2</FareRPH>
                        </FareRPHs>
                    </Journey>
                    <PlacePrefs Position="Unspecified" CompartmentType="Unspecified" SpecialRequest="Unspecified"/>
                </OriginDestinationOption>
                <PassengerIndex>
                    <Passenger SliceID="1" PassengerID="1"/>
                </PassengerIndex>
                <PaymentIndex/>
                <CountryLists/>
            </SelectedOption>
        </SelectedOptions>
        <Payments/>
        <Passengers>
            <Passenger IsLeader="false" YearOfBirth="Year" MonthOfBirth="Month" DayOfBirth="Day" PassportNumber="" PlaceOfBirthCountry="CA" PlaceOfBirthCity="" Nationality="CA" CountryResidence="CA" Age="-1" Surname="1qdqwd" GivenName="Passengersadasd" NamePrefix="Mr" ID="1"/>
        </Passengers>
        <Remarks/>
    </RailBookInfo>
</ACP_RailBookRQ>

    """

    serURL = 'URL: https://ws.test.acprailinternational.com/method=ACP_RailBook'

    headers = {'content-type': 'application/xml; charset=utf-8'}
    
    Result = requests.post(serURL, data=xml, headers=headers)
    print Result,"++++++"
    if Result.status_code == 200:
        response = Result.text
        print response
        return HttpResponse(response)
    else:
        print "Status code error", Result.status_code  

        return HttpResponse(Result.status_code )
  

def bookAPI_call(request):
    ''' Booking API Request '''
    journey_data = fare_data = ""
    fare_val = request.session.get('fare_val')
    train_no = request.session.get('train')
    # print train_no
    avail_response = request.session.get('Avail_Rail_response')
    if avail_response:
        data = str(avail_response)
        d1 = data.split('<Journeys>')
        d2 = d1[1].split('</Journeys>')        
        if d2[0].__contains__(str(train_no)):
            journey = d2[0].split('</Journey>')
            journey1 = journey[0].split('<Journey ')
            journey_data += str(journey1[1])      

        d3 = data.split('<Fares>')
        d4 = d3[1].split('</Fares>')
        fare = str(fare_val)
        fare_amount = "Amount="+fare
        # print fare_amount
        if d4[0].__contains__(fare):            
            fareIn = d4[0].split('</Fare>')
            fareIn_1 = fareIn[0].split('<Fare ')            
            fare_data = str(fareIn_1[1])     

    

    xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_data += '<ACP_RailBookRQ ResponseType="Native-Availability" xmlns="http://www.acprailinternational.com/API/R2"><POS><RequestorID>RTG-XML</RequestorID></POS>'
    xml_data += '<RailBookInfo><SelectedOptions><SelectedOption ID="1" IsCreditSale="true" TicketOption="Etk">'
    xml_data += '<ODFare '+str(fare_data)
    xml_data += '</ODFare>'
    xml_data += '<OriginDestinationOption>'
    xml_data += '<Journey '+str(journey_data)+'</Journey>'
    xml_data += '<PlacePrefs/>'
    xml_data += '</OriginDestinationOption>'
    xml_data += '<PassengerIndex><Passenger PassengerID="1" SliceID="1"/></PassengerIndex>'
    xml_data += '<PaymentIndex/>'
    xml_data += '</SelectedOption></SelectedOptions>'
    xml_data += '<Payments/>'
    xml_data += '<Passengers><Passenger ID="1" NamePrefix="Mr" GivenName="Test" Surname="Test" Age="-1" CountryResidence="TS" Nationality="Indian" PlaceOfBirthCity="PTC" PlaceOfBirthCountry="India" PassportNumber="R686910S" DayOfBirth="06" MonthOfBirth="July" YearOfBirth="1995" IsLeader="true"/></Passengers>'
    xml_data += '<Remarks/>'
    xml_data += '</RailBookInfo>'
    xml_data += '</ACP_RailBookRQ>'
    
    print "============================"

    print  xml_data

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailBookRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Book API  request"
    
    Result = requests.post(serURL, data=xml_data, headers=headers)
    print Result
    if Result.status_code == 200:
        response = Result.text
        print "api response"
        print response
    else:
        pass
    print "After Book API Response"

    return HttpResponse("Booking successfull")
  

def bookAPI_call1(request):
    ''' Booking API Request '''
    journey_data = fare_data = ""
    fare_val = request.session.get('fare_val')
    avail_response = request.session.get('Avail_Rail_response')
    if avail_response:
        data = str(avail_response)
        d1 = data.split('<Journeys>')
        d2 = d1[1].split('</Journeys>')        
        if d2[0].__contains__("9014"):
            # print "if condition"
            journey = d2[0].split('</Journey>')
            journey1 = journey[0].split('<Journey ')
            # print journey1
            journey_data = "<Journey "
            journey_data += str(journey1[1])
            print "&&&"
            print journey_data

            journey_data+="</Journey>"         

        d3 = data.split('<Fares>')
        d4 = d3[1].split('</Fares>')
        fare = str(fare_val)
        fare_amount = "Amount="+fare
        if d4[0].__contains__(fare):
            print "fare ifcondition  "
            print "&&&"
            fareIn = d4[0].split('</Fare>')
            fareIn_1 = fareIn[0].split('<Fare ')
            # print fareIn_1[1]
            print ">>>>>"
            fare_data = str(fareIn_1[1])
            fare_data+="</Fare>"

    

    xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
    root = ET.Element("ACP_RailBookRQ", xmlns="http://www.acprailinternational.com/API/R2",
                      ResponseType="Native-Availability")
    pos = ET.SubElement(root, "POS")
    requestor = ET.SubElement(pos, "RequestorID").text = "RTG-XML"
    rail_book_info = ET.SubElement(root, "RailBookInfo") 
    select_options = ET.SubElement(rail_book_info, 'SelectedOptions') 
    select_options_one = ET.SubElement(select_options, 'SelectedOption', TicketOption="Etk", IsCreditSale="true", ID="1")
    fare = ET.SubElement(select_options_one, fare_data)
    origin = ET.SubElement(select_options_one, 'OriginDestinationOption') 
    # journey = ET.SubElement(origin, 'Journey').text = journey_data
    journey = ET.SubElement(origin, str(journey_data))

    # journey_data = ET.SubElement(journey, journey_data)
    passIndex = ET.SubElement(select_options_one, 'PassengerIndex') 
    passengerInd = ET.SubElement(passIndex, 'Passenger', PassengerID="1" ,SliceID="1") 
    passengersData = ET.SubElement(rail_book_info, 'Passengers') 
    passengers = ET.SubElement(passengersData, 'Passenger', ID="1", NamePrefix="Mr", GivenName="Test", Surname="Test", Age="-1", CountryResidence="", Nationality="", PlaceOfBirthCity="", PlaceOfBirthCountry="", PassportNumber="", DayOfBirth="Day", MonthOfBirth="Month", YearOfBirth="Year", IsLeader="true")   
    mydata = ET.tostring(root)
    xml_data += mydata

    print  xml_data

    serURL = 'https://ws.test.acprailinternational.com/method=ACP_RailBookRQ'
    headers = {'content-type': 'application/xml; charset=utf-8'}
    print "Book API  request"
    
    Result = requests.post(serURL, data=xml_data, headers=headers)
    print Result
    if Result.status_code == 200:
        response = Result.text
    else:
        pass
    print "After Book API Response"

    return HttpResponse("Booking successfull")
  

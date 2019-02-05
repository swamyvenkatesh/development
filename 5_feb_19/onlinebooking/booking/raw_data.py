<QueryDict: {u'firstparent': [u''], u'firstchildname': [u'', u''], u'non_adults': [u'[0, 1]'], u'secondparent': [u''], u'secondchildname': [u'', u''], u'passengersData': [u'[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]'], u'csrfmiddlewaretoken': [u'o6nGQJomcSTgPAVTCHjUzfZCKbCblwbtj54RskgZoaF7IuMqC8EN0xM7vvuwcM4D'], u'adults': [u'[0]']}>


 # passengers_info = request.session['passengers_Data']
        # fare = str(request.session['fare'])
        # fare = float(fare)
        # fare_class = request.session['fare_class']

        # all_data = {}
        # all_data['passengers'] = passengers_info
        # all_data['fare'] = fare
        # checkingData = request.session['resultData']
        # all_data['passport'] = str( checkingData[0][0]['is_passport'])
        # all_data['nationality'] = str(checkingData[0][0]['is_nationality'])
        # all_data['dob'] = str(checkingData[0][0]['is_dob'])
        # all_data['countryResidence'] = str(checkingData[0][0]['is_cntryres'])
        # all_data['birthPlace'] = str(checkingData[0][0]['is_birthplace'])
        # all_data['no_of_adults'] = request.session['adult_count']
        # all_data['no_of_childs'] = request.session['child_count']
        # fare_ref = request.session['fare_ref']
        # passengers_num = request.session['adult_count']+request.session['child_count']

        # all_data['passengers_num'] = passengers_num
        # n = len(passengers_info)/passengers_num
        # my_list=passengers_info
        # print fare, fare_class, passengers_num
        # final_passengers_list = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]     

        # # print final_passengers_list
        # passengers_data = []
        # for i in final_passengers_list:
        #     del i[0]
        #     passengers_data.append(i)

        # print "=================="
        # print passengers_data

        # if len(passengers_data) == passengers_num:
        #     print "lengths and count is equal"



def checkinfodeatil1(request):
    '''
        Passengers information is storing into session 
    '''
    if request.method=="GET":

        passengers_info = json.loads(request.GET.get('passengers'))
        adult_count = request.GET.get('adult_num')
        child_count = request.GET.get('child_num')
        request.session['passengers_Data'] = passengers_info
        request.session['adult_count'] = len(eval(adult_count))
        request.session['child_count'] = len(eval(child_count))

        return HttpResponse(passengers_info)


        # return render(request,'booking/checkout.html',{})
    else:
        return render(request,'booking/checkout.html',{})






Standard 7 407.10 [[{}, {}, {}, {}], [{u'secondname': u'swain'}, {}, {u'first_name': u'anita'}, {u'secondname': u'swain'}], [{u'first_name': u'namita '}, {u'secondname': u'swain'}, {}, {u'first_name': u'ravi raj'}], [{}, {}, {}, {}]] 4
GEt Details
{u'arr_station_code': '8700015', u'arr_station': 'Paris Nord', u'arr_time': '15:47:00', u'dept_station_code': '7015400', u'train': '9024', u'dept_station': 'London St Pancras Int', u'dept_time': '12:24:00'}
@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@@@$%%$#@
[[{}, {}, {}, {}], [{u'secondname': u'swain'}, {}, {u'first_name': u'anita'}, {u'secondname': u'swain'}], [{u'first_name': u'namita '}, {u'secondname': u'swain'}, {}, {u'first_name': u'ravi raj'}], [{}, {}, {}, {}]]

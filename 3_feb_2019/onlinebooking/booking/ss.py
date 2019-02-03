# rph_list  = [
# [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9'], 

# [u'10', u'11', u'12', u'13', u'14', u'15', u'16', u'17', u'18'], 

# [u'19', u'20', u'21', u'22', u'23', u'24', u'25', u'26', u'27'], 

# u'28', 

# [u'29', u'30', u'31', u'32'], 

# [u'33', u'34', u'35', u'36', u'37', u'38', u'39', u'40', u'41'],

#  [u'42', u'43', u'44', u'45', u'46', u'47', u'48', u'49', u'50'], 

#  [u'51', u'52', u'53', u'54', u'55', u'56', u'57', u'58', u'59'], 

#  [u'60', u'61', u'62', u'63', u'64', u'65'], [u'66', u'67', u'68', u'69', u'70', u'71', u'72', u'73', u'74'], [u'75', u'76', u'77', u'78', u'79', u'80'], [u'81', u'82', u'83', u'84', u'85', u'86', u'87', u'88', u'89'], [u'90', u'91', u'92', u'93', u'94', u'95', u'96', u'97', u'98'], [u'99', u'100', u'101', u'102', u'103', u'104', u'105', u'106', u'107'], [u'108', u'109', u'110', u'111', u'112', u'113'], [u'114', u'115', u'116', u'117', u'118', u'119'], [u'120', u'121', u'122', u'123', u'124', u'125', u'126', u'127', u'128'], [u'129', u'130', u'131', u'132', u'133', u'134', u'135'], [u'136', u'137'], [u'138', u'139', u'140', u'141', u'142', u'143', u'144', u'145', u'146'], [u'147', u'148', u'149', u'150', u'151', u'152', u'153', u'154', u'155'], [u'156', u'157', u'158', u'159', u'160', u'161', u'162'], [u'163', u'164'], [u'165', u'166', u'167', u'168', u'169', u'170', u'171'], [u'172', u'173', u'174', u'175', u'176', u'177', u'178', u'179', u'180'], [u'181', u'182', u'183', u'184', u'185', u'186', u'187', u'188', u'189'], [u'190', u'191', u'192', u'193', u'194', u'195'], [u'196', u'197', u'198', u'199', u'200', u'201', u'202', u'203', u'204'], [u'205', u'206', u'207', u'208', u'209', u'210', u'211', u'212', u'213']]



# actual_output =  [[{u'Turista': u'308.10', u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'308.10', u'class': u'Turista', u'fareRefer': u'1'}, 
#         {u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'365.10', u'Turista Plus': u'365.10', u'class': u'Turista Plus', u'fareRefer': u'2'}, 
#         {u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'365.10', u'Turista Plus': u'365.10', u'class': u'Turista Plus', u'fareRefer': u'2'}],

# hi = []


# pro = []

# for i in actual_output:
#     # ll = []
#     r_s = {}
#     li1 = []
    
#     for j in i:
#         pro.append(str(j['product_name']))
#         for k in rph_list:
            
#             # ll = []
#             for m in k:
#                 if j['fareRefer'] == m:
#                     # if pro == 
#                     li1.append(j['total_price'])

#                     # hi.append(j)

#             # d = list(set(ll))
#         # hi.append(ll)
#     # print pro
#     pro = list(set(pro))
#     # print pro
#     r_s[pro[0]] = list(set(li1))
#     hi.append(r_s)
#     # print r_s, "^^^6"*20
#     # break

# # print hi



# data = [
#         [
#             {u'Turista': u'308.10', 
#                 u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', 
#                 u'total_price': u'308.10', 
#                 u'class': u'Turista', 
#                 u'fareRefer': u'1'
#             }, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'365.10', u'Turista Plus': u'365.10', u'class': u'Turista Plus', u'fareRefer': u'2'}, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'506.10', u'Preferente': u'506.10', u'class': u'Preferente', u'fareRefer': u'3'}, 

#             {u'Turista': u'218.10', u'product_name': u'RENFE TICKET on DEPARTURE & RESER  WEB', u'total_price': u'218.10', u'class': u'Turista', u'fareRefer': u'4'}, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESER  WEB', u'total_price': u'203.10', u'Turista Plus': u'203.10', u'class': u'Turista Plus', u'fareRefer': u'5'}, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESER  WEB', u'total_price': u'203.10', u'Preferente': u'203.10', u'class': u'Preferente', u'fareRefer': u'6'}, 
#             {u'Turista': u'233.10', u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'233.10', u'class': u'Turista', u'fareRefer': u'7'}, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'221.10', u'Turista Plus': u'221.10', u'class': u'Turista Plus', u'fareRefer': u'8'}, 
#             {u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'227.10', u'Preferente': u'227.10', u'class': u'Preferente', u'fareRefer': u'9'}
#         ],


#         ]
# classes = ['Preferente', 'Turista Plus', 'Turista']

# dd = {}
# for i in data:
#     for kk in i:
#         # print kk

#         # print kk['product_name']
#         if kk['product_name'] not in dd:
#             # print "sdsfsdf"
#             for index, class1 in enumerate(classes):
#                 if kk.get(class1) is not None:
#                     list1 = []
#                     # print kk[class1], class1, "====", kk['product_name']
#                     # list1[index]=kk[class1]
#                     list1.append(kk[class1])
#                     dd[kk['product_name']] = list1
#         else:                        

#             for index, class1 in enumerate(classes):
#                 if kk.get(class1) is not None: 
#                     name = dd.get(kk['product_name'])                   
#                     # print kk[class1], class1, "====", kk['product_name']
#                     # list1[index]=kk[class1]
#                     name.append(kk[class1])
#                     dd[kk['product_name']] = name

#                 # print type(class1)

#                 # pass
# # print "$$$$$$$$$$$$$$"
# # print dd         

# # "<div id=\"DisplayName\">TICKET on DEPARTURE & RESERVATION -ANYTIME</div>"
# hi = "<div id=\"DisplayName\">Renfe E-Ticket Promo Fare</div>"  
# h=hi.split(">")[1].replace("</div","")
# print h
# # []


# ss = "Semi flex (BW) - Standard"
# ss = "Standard Business"
# if ss.__contains__('-'):
#   ss = ss.split("-")[-1]





# print ss

# sd = [u'62.70', u'123.70']
# # sd = ['166.7']

# sd = sorted([float(i) for i in sd])
# print sd
# print min(sd)

# # d_list = []
# # for i in data:
# #     for kk in i:
# #         # print kk
# #         dic = {}
# #         li = []
# #         for key, value in kk.items():
# #             if key == "product_name":
# #                 print value                
# #                 if key in classes: 
# #                     li.append({key:kk[key]})
# #                 dic[value] = li
# #         d_list.append(dic)


# # print d_list


# # "%s"(name)



# hello = [

# [{u'is_cntryres': u'false', u'total_price': u'735.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'1', u'is_passport': u'false', u'ticket_option': u'ETK', u' Standard': u'735.50', u'class': u' Standard', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}, 


# {u'is_cntryres': u'false', u'total_price': u'981.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'2', u'is_passport': u'false', u'ticket_option': u'ETK', u'class': u' Std Premier', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u' Std Premier': u'981.50', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}]


# , [{u'is_cntryres': u'false', u'total_price': u'600.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'3', u'is_passport': u'false', u'ticket_option': u'ETK', u' Standard': u'600.50', u'class': u' Standard', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'},

#  {u'is_cntryres': u'false', u'total_price': u'981.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'4', u'is_passport': u'false', u'ticket_option': u'ETK', u'class': u' Std Premier', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u' Std Premier': u'981.50', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}], 

# [{u'is_cntryres': u'false', u'total_price': u'735.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'5', u'is_passport': u'false', u'ticket_option': u'ETK', u' Standard': u'735.50', u'class': u' Standard', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}, {u'is_cntryres': u'false', u'total_price': u'981.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'6', u'is_passport': u'false', u'ticket_option': u'ETK', u'class': u' Std Premier', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u' Std Premier': u'981.50', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}], [{u'is_cntryres': u'false', u'total_price': u'220.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'7', u'is_passport': u'false', u'ticket_option': u'ETK', u' Standard': u'220.50', u'class': u' Standard', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}, {u'is_cntryres': u'false', u'total_price': u'546.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'8', u'is_passport': u'false', u'ticket_option': u'ETK', u'class': u' Std Premier', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u' Std Premier': u'546.50', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}], [{u'is_cntryres': u'false', u'total_price': u'412.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'9', u'is_passport': u'false', u'ticket_option': u'ETK', u' Standard': u'412.50', u'class': u' Standard', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}, {u'is_cntryres': u'false', u'total_price': u'655.50', u'is_nationality': u'false', u'is_email': u'true', u'is_birthplace': u'false', u'fareRefer': u'10', u'is_passport': u'false', u'ticket_option': u'ETK', u'class': u' Std Premier', u'is_dob': u'false', u'is_paxname': u'true', u'sales_condition': u'Refundable up to 1 day before the departure date. A 40% cancellation fee applies. Non-refundable after departure. Refunds are limited to completely unused and unvalidated passes, tickets and exchange vouchers.', u' Std Premier': u'655.50', u'product_name': u'Eurostar E-Ticket and Reservation Semi Flexible'}]]


# print hello[0][0]

# print hello[0][0]['is_passport']

# for key, value in hello[0][0].items():
#   print key, value
# # print hello[0]['is_passport']

# main_lis = [  {},{},{},{},{},{},{},{},{},{},  ]

# one = [  [{},{},{},{},{}] , [{},{},{},{},{}], [{},{},{},{},{}]]
# for i in main_lis:
    # if len(i)
    # print new,"{{{{"


# n=5
# final = [main_lis[i * n:(i + 1) * n] for i in range((len(main_lis) + n - 1) // n )] 

# print final


# # d = [{}, {u'first_name': u'suni'}, {u'secondname': u'swain'}, {u'passport': u'R681790'}, {}, {u'first_name': u'arjun'}, {u'secondname': u'swain'}, {u'passport': u'No'}, {}, {u'first_name': u'ravi'}, {u'secondname': u'raj'}, {u'passport': u'R711190'}]

# # print type(d)
# # print len(d)
# # while {} in d:
# #   d.remove({})

# # print len(d)


# final = [passengers_info[i * passengers_num:(i + 1) * passengers_num] for i in range((len(passengers_info) + passengers_num - 1) // passengers_num )] 
    # print "$$$$$$"*30


# # [

# #   [{}, {u'first_name': u'suni'}, {u'secondname': u'swain'}, {u'passport': u'12'}, {}], 
# #   [{u'first_name': u'ani'}, {u'secondname': u'swain'}, {u'passport': u'13'}, {}, {}], 
# #   [{}, {}, {}, {}, {}], 
# #   [{}, {}, {}, {}, {}]

# # ]
# main_lis = [  {},{},{},{},{},{},{},{},{},{},  ]
# n=2
# ll=[]
# li = []
# print len(main_lis)
# for i , j  in enumerate(main_lis,start=1):
#     li = []
#     li.append(j)
#     if i % n == 0:
#         ll.append(li)
#         li = []
#     # if len(main_lis)%n == 0:

#     #     li.append(i)
#     #     ll.append(li)
#     # li = []

# print ll



# my_list=[1,5,7,8,9,3,3,3,3,3,3,9,0]
# n=5
# final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]  
# print (final)

import datetime
fare_ref = 3

datas = [

{u'arrival': u'12:47:00', u'index': 0, 

u'journey_details': [{u'dept_station': 'London St Pancras Int', u'dept_time': '09:22:00', u'train': '9014', u'arr_station': 'Paris Nord', u'arr_time': '12:47:00'}], u'departure': u'09:22:00', u'duration': datetime.timedelta(0, 12300),

 u'fareRPHS_List': [u'1', u'2', u'3'], u'changes': 0}, 


{u'arrival': u'13:47:00', u'index': 1, u'journey_details': [{u'dept_station': 'London St Pancras Int', u'dept_time': '10:24:00', u'train': '9018', u'arr_station': 'Paris Nord', u'arr_time': '13:47:00'}], u'departure': u'10:24:00', u'duration': datetime.timedelta(0, 12180), u'fareRPHS_List': [u'4', u'5', u'6'], u'changes': 0}, 


{u'arrival': u'15:47:00', u'index': 2, u'journey_details': [{u'dept_station': 'London St Pancras Int', u'dept_time': '12:24:00', u'train': '9024', u'arr_station': 'Paris Nord', u'arr_time': '15:47:00'}], u'departure': u'12:24:00', u'duration': datetime.timedelta(0, 12180), u'fareRPHS_List': [u'7', u'8', u'9'], u'changes': 0}, 

{u'arrival': u'16:47:00', u'index': 3, u'journey_details': [{u'dept_station': 'London St Pancras Int', u'dept_time': '13:31:00', u'train': '9028', u'arr_station': 'Paris Nord', u'arr_time': '16:47:00'}], u'departure': u'13:31:00', u'duration': datetime.timedelta(0, 11760), u'fareRPHS_List': [u'10', u'11', u'12'], u'changes': 0}, 


{u'arrival': u'17:47:00', u'index': 4, u'journey_details': [{u'dept_station': 'London St Pancras Int', u'dept_time': '14:22:00', u'train': '9032', u'arr_station': 'Paris Nord', u'arr_time': '17:47:00'}], u'departure': u'14:22:00', u'duration': datetime.timedelta(0, 12300), u'fareRPHS_List': [u'13', u'14', u'15'], u'changes': 0}

]
# print len(datas)
# dic = {}
# for i in datas:
#     # print (i)
#     for j1 , j2  in i.items():
#         # print (j1)
#         if j1 == 'fareRPHS_List':
#             # print j2
#             # print fare_ref
#             # fare_ref = [i.encode('utf-8') for i in fare_ref]
#             j2 = [int(x.encode('utf-8')) for x in j2]
#             # print j2
#             if fare_ref in j2:
#                 # print "44444"
#                 # print i['journey_details']
#                 dic[fare_ref] = i['journey_details']

#             else:
#                 print "**"

#     # break
# print "DDDDD"
# # print dic


# for i in  dic[fare_ref]:
#     print i
# data = {u'dept_station': 'London St Pancras Int', u'dept_time': '13:31:00', u'train': '9028', u'arr_station': 'Paris Nord', u'arr_time': '16:47:00'}


# print data


main_lis = [  [ {},{},{} ] , [{},{},{}] ,[{},{},{}]]

for i in main_lis:
    # print i
    del i[0]
    print i

# main_lis = [ del i[0] for i in main_lis]

import uuid

print uuid.uuid4()
# [
#       OrderedDict([(u'TrainSegment', OrderedDict([(u'@DepartureDateTime', u'2019-01-30T08:09:00'), (u'@ArrivalDateTime', u'2019-01-30T09:40:00'), (u'@TrainNumber', u'0809'), (u'@JourneyDuration', u'PT1H31M'), (u'@TrainServiceType', u'Train'), (u'@CrossBorder', u'false'), (u'@OperatorName', u'ATOC'), (u'DepartureStation', OrderedDict([(u'@LocationCode', u'7000372'), (u'@Name', u'Chichester'), (u'@Country', u'GB')])), (u'ArrivalStation', OrderedDict([(u'@LocationCode', u'7000246'), (u'@Name', u'London Victoria'), (u'@Country', u'GB')])), (u'RailAmenities', OrderedDict([(u'RailAmenity', OrderedDict([(u'@Name', u'SN')]))])), (u'ClassCodes', None)]))]),      
#       OrderedDict([(u'TrainSegment', OrderedDict([(u'@DepartureDateTime', u'2019-01-30T09:40:00'), (u'@ArrivalDateTime', u'2019-01-30T10:40:00'), (u'@TrainNumber', u'0940'), (u'@JourneyDuration', u'PT1H'), (u'@TrainServiceType', u'Tube'), (u'@CrossBorder', u'false'), (u'@OperatorName', u'ATOC'), (u'DepartureStation', OrderedDict([(u'@LocationCode', u'7000246'), (u'@Name', u'London Victoria'), (u'@Country', u'GB')])), (u'ArrivalStation', OrderedDict([(u'@LocationCode', u'7000021'), (u'@Name', u'London Euston'), (u'@Country', u'GB')])), (u'RailAmenities', OrderedDict([(u'RailAmenity', OrderedDict([(u'@Name', u'Tube segment')]))])), (u'ClassCodes', None)]))]), 
#       OrderedDict([(u'TrainSegment', OrderedDict([(u'@DepartureDateTime', u'2019-01-30T10:40:00'), (u'@ArrivalDateTime', u'2019-01-30T12:10:00'), (u'@TrainNumber', u'1040'), (u'@JourneyDuration', u'PT1H30M'), (u'@TrainServiceType', u'Train'), (u'@CrossBorder', u'false'), (u'@OperatorName', u'ATOC'), (u'DepartureStation', OrderedDict([(u'@LocationCode', u'7000021'), (u'@Name', u'London Euston'), (u'@Country', u'GB')])), (u'ArrivalStation', OrderedDict([(u'@LocationCode', u'7000096'), (u'@Name', u'Crewe'), (u'@Country', u'GB')])), (u'RailAmenities', OrderedDict([(u'RailAmenity', OrderedDict([(u'@Name', u'VT')]))])), (u'ClassCodes', None)]))]), 
#       OrderedDict([(u'TrainSegment', OrderedDict([(u'@DepartureDateTime', u'2019-01-30T12:23:00'), (u'@ArrivalDateTime', u'2019-01-30T12:46:00'), (u'@TrainNumber', u'1223'), (u'@JourneyDuration', u'PT23M'), (u'@TrainServiceType', u'Train'), (u'@CrossBorder', u'false'), (u'@OperatorName', u'ATOC'), (u'DepartureStation', OrderedDict([(u'@LocationCode', u'7000096'), (u'@Name', u'Crewe'), (u'@Country', u'GB')])), (u'ArrivalStation', OrderedDict([(u'@LocationCode', u'7000168'), (u'@Name', u'Chester'), (u'@Country', u'GB')])), (u'RailAmenities', OrderedDict([(u'RailAmenity', OrderedDict([(u'@Name', u'AW')]))])), (u'ClassCodes', None)]))]), 
#       OrderedDict([(u'TrainSegment', OrderedDict([(u'@DepartureDateTime', u'2019-01-30T13:02:00'), (u'@ArrivalDateTime', u'2019-01-30T13:18:00'), (u'@TrainNumber', u'1302'), (u'@JourneyDuration', u'PT16M'), (u'@TrainServiceType', u'Train'), (u'@CrossBorder', u'false'), (u'@OperatorName', u'ATOC'), (u'DepartureStation', OrderedDict([(u'@LocationCode', u'7000168'), (u'@Name', u'Chester'), (u'@Country', u'GB')])), (u'ArrivalStation', OrderedDict([(u'@LocationCode', u'7023060'), (u'@Name', u'Delamere'), (u'@Country', u'GB')])), (u'RailAmenities', OrderedDict([(u'RailAmenity', OrderedDict([(u'@Name', u'NT')]))])), (u'ClassCodes', None)]))])
# ]


dict1 = {}
dict1['price'] = [121, 156]
# print dict1
# print dict1['price'][0]

# print len(dict1['price'])

ll = ['first1', 'standard1', 'first2', 'standard2', 'first3', 'standard3', 'standard4']
li = []
main = []
list2 = []
count = 0
for index, i in enumerate(ll):
    # print i
    dd = {}
    count+=1

    # if count %2 == 0:   

    
    li.append(i)
    if len(li) == 2:
        # print li
        dd['price'] = li
        main.append(dd) 
        print dd
        del li[:]
        # main.append(dd)
    # print dd
        

def split_seq(seq, size):
    newseq = []
    splitsize = 1.0/size*len(seq)
    for i in range(size):
            newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
    return newseq

# print main


# print split_seq(ll, 3)

n=2
final = [ll[i * n:(i + 1) * n] for i in range((len(ll) + n - 1) // n )] 

# print final


list_Data = [
    [{u'total_price': u'948.00', u'First': u'948.00'}, {u'total_price': u'738.00', u'Standard': u'738.00'}], 
    [{u'total_price': u'981.00', u'First': u'981.00'}, {u'total_price': u'486.00', u'Standard': u'486.00'}], 
    [{u'total_price': u'624.00', u'First': u'624.00'}, {u'total_price': u'423.00', u'Standard': u'423.00'}], 
    [{u'total_price': u'141.00', u'Standard': u'141.00'}]

]

for i in list_Data:
    print i
    # print i[0]
    if len(i) == 2:

        print i[0].get('First')
        print i[1].get('Standard')
    # print i[1]['total_price']

    # for jj in i:
    #     print jj
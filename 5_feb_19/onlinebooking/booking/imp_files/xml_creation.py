
# from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree as ET

# div_root = ET.Element('div') # <div>
#     tab = ET.SubElement(div_root, 'table', clas='table',border='1') # <div><table>
#     thr_root = ET.SubElement(tab, 'tr') # <div><table><tr>
    
#     for i in head_list:
#         tad = ET.SubElement(thr_root,'th').text=str(i) # <div><table><tr><th></th><th></th><th></th><th></th><th></th></tr>
    
    
#     for index1,j in enumerate(first_list):  
#         tr_root = ET.SubElement(tab, 'tr')  # <div><table><tr><th>5times</th></tr><tr>    
#         for number,k in enumerate(j): 
#             print k,"::::::::"
            
#             # for no, value in enumerate(k):            
#             tad = ET.SubElement(tr_root,'td', id='').text=str(k)   # <div><table><tr><th>5times</th></tr><tr><td>length of k times</td></tr></table></div>                                     

#     data = ET.tostring(div_root).replace('clas','class')
#     return data

Adults = 2

child = 2
child_ages = []
originlocation="123456"
DestinationLocation="sec"
DepartureDepartureDate="29-01-2019"
ReturnReturnDate="31-08-1234"


xml_start = '<?xml version="1.0" encoding="UTF-8"?>'
root = ET.Element("ACP_RailAvailRQ",xmlns="http://www.acprailinternational.com/API/R2", ResponseType="Native-Availability")
pos = ET.SubElement(root, "POS")
requestor = ET.SubElement(pos, "RequestorID").text="RTG-XML"
rail_avail_info = ET.SubElement(root, "RailAvailInfo")
origins = ET.SubElement(rail_avail_info , 'OriginDestinationSpecifications')
origin1=ET.SubElement(origins,'OriginLocation', LocationCode="{0}".format(originlocation))
origin2=ET.SubElement(origins,'DestinationLocation', LocationCode="{0}".format(DestinationLocation))
origin3=ET.SubElement(origins,'Departure', DepartureDate="{0}".format(DepartureDepartureDate))
if ReturnReturnDate:
    origin4=ET.SubElement(origins,'Return', ReturnDate="{0}".format(ReturnReturnDate))

passengers = ET.SubElement(rail_avail_info , 'PassengerSpecifications')
# for adults 
passtype=ET.SubElement(passengers,'PassengerType',Age="-1", Quantity="{0}".format(Adults))
# for childs
if child_ages:
    for i in child_ages:
        passtype=ET.SubElement(passengers,'PassengerType',Age=str(i), Quantity="1")


fare_qual=ET.SubElement(rail_avail_info,'FareQualifier RateCategory="Regular"')
responsePt=ET.SubElement(rail_avail_info,'ResponsePtPTypes')
responsePt1=ET.SubElement(responsePt,'ResponsePtPType').text="TW"     


mydata = ET.tostring(root) 

mydata = xml_start+mydata


print mydata
print type(mydata)


xml = """
        <?xml version="1.0" encoding="UTF-8"?>
            <ACP_RailAvailRQ xmlns="http://www.acprailinternational.com/API/R2" ResponseType="Native-Availability">
                <POS>
                    <RequestorID>RTG-XML</RequestorID>
                </POS>
                <RailAvailInfo>
                    <OriginDestinationSpecifications>
                        <OriginLocation LocationCode="%s"/>
                        <DestinationLocation LocationCode="%s"/>
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
        """%('orgLocCode', 'destLocCode', 'date_string')

print type(xml)
# <PassengerType Age="-1" Quantity="3"/>
# <PassengerType>suni</PassengerType>


data = 'Semi flex (HZ) - Std Premier '

data = "Standard"

dd =  data.split('-')

print dd

# print dd[0]
# print dd[1]


print dd[-1]

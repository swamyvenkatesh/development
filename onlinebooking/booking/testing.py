error = {'ACP_RailAvailRS': 
			{'@xmlns': 'http://www.acprailinternational.com/API/R2', 
			'Errors': {'Error': {'@ShortText': 'User Error: message', '@Code': '81', 
			'#text': 'Rule Violation: Invalid UIC code: 0', '@Type': '3'}}, 
			'@Target': 'Production', '@TimeStamp': '2019-01-23T02:05:13', 
			'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', '@Version': '1.001', 
			'@xsi:schemaLocation': 'http://www.acprailinternational.com/API/R2 ACP_RailAvailRS.xsd'
			}
		}

# print error['ACP_RailAvailRS'].get('OriginDestinationOptions')


data = [
[
	{u'product_name': u'TICKET on DEPARTURE & RESERVATION -ANYTIME via:ANY PERMITTED - Travel is allowed via any permitted route.', u'total_price': u'948.00', u'class': u'First', u'fareRefer': u'1'}, 
	{u'product_name': u'TICKET on DEPARTURE & RESERVATION -ANYTIME via:ANY PERMITTED - Travel is allowed via any permitted route.', u'total_price': u'738.00', u'class': u'Standard', u'fareRefer': u'2'}
	],

 [
 	{u'product_name': u'TICKET on DEPARTURE & RESERVATION -ANYTIME via:VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury.', u'total_price': u'981.00', u'class': u'First', u'fareRefer': u'3'},

 	 {u'product_name': u'TICKET on DEPARTURE & RESERVATION -ANYTIME via:VIA BANBURY - Valid only for travel via (changing trains or passing through) Banbury.', u'total_price': u'486.00', u'class': u'Standard', u'fareRefer': u'4'}],

 	  [{u'product_name': u'TICKET on DEPARTURE & RESERVATION -OFFPEAK via:ANY PERMITTED - Travel is allowed via any permitted route.', u'total_price': u'624.00', u'class': u'First', u'fareRefer': u'5'}, 

 	  {u'product_name': u'TICKET on DEPARTURE & RESERVATION -OFFPEAK via:ANY PERMITTED - Travel is allowed via any permitted route.', u'total_price': u'423.00', u'class': u'Standard', u'fareRefer': u'6'}], 


 	  [{u'product_name': u'TICKET on DEPARTURE & RESERVATION -ADVANCE via:XC &CONNECTIONS - Only valid on booked CrossCountry services and required connecting services.', u'total_price': u'141.00', u'class': u'Standard', u'fareRefer': u'7'}]]



# for dat in data:
# 	for i in dat:
# 		print i['product_name']
# 		pass


ddd = [
	[{}, {}, {}], 
	[{}, {}, {}], 
	[{}, {}, {}], 
	[{}, {}, {}],
	[{}, {}, {}], 
	[{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], 
	[{}, {}, {}], [{}, {}, {}], 
	[
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'149.10', u'class': u'Turista', u'fareRefer': u'205'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'203.10', u'class': u'Turista Plus', u'fareRefer': u'206'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'242.10', u'class': u'Preferente', u'fareRefer': u'207'}
	], 
	[	{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'164.10', u'class': u'Turista', u'fareRefer': u'208'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'221.10', u'class': u'Turista Plus', u'fareRefer': u'209'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'266.10', u'class': u'Preferente', u'fareRefer': u'210'}
	], 
	[	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'308.10', u'class': u'Turista', u'fareRefer': u'211'}, 
	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'365.10', u'class': u'Turista Plus', u'fareRefer': u'212'}, 
	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'506.10', u'class': u'Preferente', u'fareRefer': u'213'}
	]] 

# for i in ddd:
# 	# print i
# 	if i is not None:
# 		print i



dddd = [
	[
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'149.10', u'class': u'Turista', u'fareRefer': u'205'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'203.10', u'class': u'Turista Plus', u'fareRefer': u'206'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER WEB', u'total_price': u'242.10', u'class': u'Preferente', u'fareRefer': u'207'}
	], 
	[	{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'164.10', u'class': u'Turista', u'fareRefer': u'208'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'221.10', u'class': u'Turista Plus', u'fareRefer': u'209'}, 
		{u'product_name': u'RENFE TICKET on DEPARTURE & RESER. PROMO+', u'total_price': u'266.10', u'class': u'Preferente', u'fareRefer': u'210'}
	], 
	[	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'308.10', u'class': u'Turista', u'fareRefer': u'211'}, 
	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'365.10', u'class': u'Turista Plus', u'fareRefer': u'212'}, 
	{u'product_name': u'RENFE TICKET on DEPARTURE & RESERVATION', u'total_price': u'506.10', u'class': u'Preferente', u'fareRefer': u'213'}
	]
	] 



<td class="text-center"><button type="submit" class="btn btn-default btn-style-soft tocart2" title="Add to cart" data-possibleplaceprefsref="2" data-optionreference="1" data-journeyreference="0" data-farereference="2" data-termsandconditionsurl="" data-itinerarytypename="One-Way" style="width:100%"> £{{price.total_price}}&nbsp;<span class="glyphicon glyphicon-shopping-cart" style="font-size:0.8em;"></span> </button></td>
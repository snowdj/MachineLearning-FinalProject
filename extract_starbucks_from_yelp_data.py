import os
import json
import csv
import us_census_data

def extractStarBucksData():

	starbucksData = []

	currentPath = os.getcwd()
	path = currentPath + '/yelp_academic_dataset_business.json'

	with open(path, 'r') as data_file:  
		addBusiness = True
		for line in data_file:
			businessData = json.loads(line)
			if businessData['name'] == 'Starbucks':

				# create starbucks info
				starbucksDict = {}
				#starbucksDict['starbucks_business_id'] = businessData['business_id']
				#print businessData['business_id']
				starbucksDict['avg_stars'] = businessData['stars']
				#starbucksDict['median_hours_open'] = businessData['business_id']

				address = businessData['full_address']
				zipcode = address[-5::]
				if " " in zipcode:
					addBusiness = False


				usCensusData = us_census_data.getDataFromUSCensusWithZipcode(zipcode)
				if usCensusData != {}:
					starbucksDict['total_population'] = usCensusData[zipcode]["total_population"]
					starbucksDict['percent_white_people'] = usCensusData[zipcode]["percent_white_people"]
					starbucksDict['people_per_household'] = usCensusData[zipcode]["people_per_household"]
					starbucksDict['yearly_household_income'] = usCensusData[zipcode]["yearly_household_income"]
				else:
					print("us census data not added")
					addBusiness = False
				

				# attributes
				attributes = businessData['attributes']
				if 'Wi-Fi' in attributes.keys():
					if attributes['Wi-Fi'] == "no":
						starbucksDict['has_wifi'] = 0
					else:
						starbucksDict['has_wifi'] = 1
				else:
					addBusiness = False

				if 'Price Range' in attributes.keys():
					starbucksDict['price_range'] = attributes['Price Range']
				else:
					addBusiness = False

				if 'Outdoor Seating' in attributes.keys():
					if attributes['Outdoor Seating'] == "false":
						starbucksDict['has_outdoor_seating'] = 0
					else:
						starbucksDict['has_outdoor_seating'] = 1
				else:
					addBusiness = False

				if 'Accepts Credit Cards' in attributes.keys():
					if attributes['Accepts Credit Cards'] == "false":
						starbucksDict['has_credit_card_pay'] = 0
					else:
						starbucksDict['has_credit_card_pay'] = 1
				else:
					addBusiness = False
				
				if 'Wheelchair Accessible' in attributes.keys():
					if attributes['Wheelchair Accessible'] == "false":
						starbucksDict['is_wheelchair_accessible'] = 0
					else:
						starbucksDict['is_wheelchair_accessible'] = 1
				else:
					starbucksDict['is_wheelchair_accessible'] = 0

				
				if 'Parking' in attributes.keys():
					parking = attributes['Parking']
					
					if 'lot' in parking.keys():
						if parking['lot'] == "false":
							starbucksDict['has_lot_parking'] = 0
						else:
							starbucksDict['has_lot_parking'] = 1
					else:
						starbucksDict['has_lot_parking'] = 0

					if 'street' in parking.keys():
						if parking['street'] == "false":
							starbucksDict['has_street_parking'] = 0
						else:
							starbucksDict['has_street_parking'] = 1
					else:
						starbucksDict['has_street_parking'] = 0

				else:
					addBusiness = False

				#starbucksDict['num_similar_restaurants'] = businessData['business_id']

				if addBusiness:
					starbucksData.append(starbucksDict)
				addBusiness = True
				

	convertStarbucksDataToCSV(starbucksData)


def convertStarbucksDataToCSV(starbucksData):
	print ("converting json to csv")
	# http://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file-python
	keys = starbucksData[0].keys()
	with open('starbucks.csv', 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(starbucksData)


extractStarBucksData()
# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "LCD047_MOJ_gov"
pages = [
  'https://www.gov.uk/government/publications/spend-over-25-000-archive',
  'https://www.gov.uk/government/publications/spend-over-25-000',
  'https://www.gov.uk/government/publications/ministry-of-justice-spend-over-25000-2013',
  'https://www.gov.uk/government/publications/ministry-of-justice-spend-over-25000-2014',
  'https://www.gov.uk/government/publications/ministry-of-justice-spend-over-25000-2015'
  ]


# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string


for page in pages:

	html = urllib2.urlopen(page)
	soup = BeautifulSoup(html)
	
	fileBlocks = soup.findAll('div',{'class':'attachment-details'})
	
	for fileBlock in fileBlocks:
		fileUrl = fileBlock.a['href']
		fileUrl = fileUrl.replace("/government","http://www.gov.uk/government")
		fileUrl = fileUrl.replace(".csv/preview",".csv")
		
		title = fileBlock.h2.contents[0]
		titleTest = title.find('Download CSV')
		
		if titleTest == None:
			print 'not a csv'
		else:
			# create the right strings for the new filename
			title = title.replace('spend data','')
			title = title.upper().strip()
			csvYr = title.split(' ')[-1]
			csvYr = csvYr.replace("200","20")
			
			csvMth = title.split(' ')[-2][:3]
			csvMth = convert_mth_strings(csvMth);
		
			filename = entity_id + "_" + csvYr + "_" + csvMth
		
			todays_date = str(datetime.now())
		
			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
			
			print filename

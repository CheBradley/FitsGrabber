#This code will ask the user if they would like to extract images from 
#the FIRST catalog or the Stripe 82 catalog. It will then open a browser
#and the text file containing the RA and Dec values. If an RA and Dec 
#value are not found in the region, then it will create a new file with
#the discarded values.

import sys
import math
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def main():
	script = sys.argv[0]
	catalog = input("FIRST or Stripe 82?: ")
	if catalog == "FIRST":
		url = 'https://third.ucllnl.org/cgi-bin/firstcutout'
	elif catalog == "Stripe 82":
		url = 'https://third.ucllnl.org/cgi-bin/stripe82cutout'
	else:
		main()
	filename = input("What is the filename?: ")
	print("Would you like to place the images in Downloads?")
	response = input("Type 'y' for yes or 'n' for no: ")
	if response == 'n':
		path = input("Specify full path to directory: ")
		fitsgrabber(filename, url, path)
	elif response == 'y':
		path = 'Downloads' 
		fitsgrabber(filename, url, path)
	else:
		main()

def formatter(filename):
	"""
	Formats the file to fit the search form parameters
	
	"""
	
	formattedFilename = filename.strip(".txt") + 'formatted.txt'
	filetype = input('Press 1 if the file is in coordinate form or 2 if the file is in decimal form: ')
	if filetype == '1':
		with open(filename) as locations: 
			for location in locations:
				if ':' in location:
					fields = location.split(' ')
					RaDec = fields[0] + ' ' + fields[1]
					RaDec = RaDec.replace(':',' ')
					with open(formattedFilename, "a+") as formattedFile:
						formattedFile.write(RaDec+'\n')
						formattedFile.close()
				elif 'J' in location:
					fields = location.split(' ')
					for fieldNumber in range(len(fields)):
						if 'J' in fields[fieldNumber]:
							coordinates = fields[fieldNumber]
							coordinates = coordinates.replace('J','')
							newcoords = [coordinates[i:i+2] for i in range(0, len(coordinates), 2)]
							Ra = newcoords[0] + ' ' + newcoords[1] + ' ' + newcoords[2] + newcoords[3] + newcoords[4][0]
							Dec = newcoords[4][1] + newcoords[5] + ' ' + newcoords[6] + ' ' + newcoords[7] + newcoords[8]
							RaDec = Ra + ' ' + Dec
							with open(formattedFilename, "a+") as formattedFile:
								formattedFile.write(RaDec+'\n')
								formattedFile.close()
				else:
					with open(formattedFilename, "a+") as formattedFile:
						formattedFile.write(line+'\n')
						formattedFile.close()
	if filetype == '2':
		i = 0
		with open(filename) as locations:	
			for location in locations:
				fields = location.split('	') #this is a tab, not 3 spacings

				#the decimals have to be converted to floats and then
				#back to strings
				hours = float(fields[0])/15
				minutes = hours%1 * 60
				seconds = minutes%1 * 60
				hh = str(math.floor(hours))
				if len(hh) == 1:
					hh = '0'+hh
				mm = str(math.floor(minutes))
				if len(mm) == 1:
					mm = '0'+mm
				ss = str(seconds)[0:5]
				if len(str(math.floor(seconds))) == 1:
					ss = '0'+ss
				Ra = hh + ' ' + mm + ' ' + ss

				degrees = float(fields[1]) 
				minutes = degrees%1 * 60
				seconds = minutes%1 * 60
				dd = str(math.floor(degrees))
				if len(dd) == 1:
					dd = '0'+dd
				mm = str(math.floor(minutes))
				if len(mm) == 1:
					mm = '0'+mm
				ss = str(seconds)[0:5]
				if len(str(math.floor(seconds))) == 1:
					ss = '0'+ss
				Dec = dd + ' ' + mm + ' ' + ss
				
				RaDec = Ra + ' ' + Dec
				with open(formattedFilename, "a+") as formattedFile:
					formattedFile.write(RaDec+'\n')
					formattedFile.close()
				
				
	return formattedFilename
	

def fitsgrabber(filename, url, path):
	
	newFilename = filename.strip(".txt")
	savedFilename = newFilename + "_saved.txt"
	discardedFilename = newFilename + "_discarded.txt"
	
	formattedFilename = formatter(filename)
	
	from selenium import webdriver 
	
	#these are all settings that set up a profile in the web browser so 
	#that it will automatically download any file into a particular folder 
	profile = webdriver.FirefoxProfile() 		
	profile.set_preference("browser.download.folderList",2); 
	profile.set_preference("browser.download.manager.showWhenStarting", False); 
	profile.set_preference("browser.download.useDownloadDir", True); 
	profile.set_preference("browser.download.dir", path); 
	profile.set_preference("browser.download.manager.alwaysAsk.force", False);
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download"); 
	
	driver = webdriver.Firefox(firefox_profile=profile) 
	
	driver.get(url);	
	
	with open(formattedFilename) as locations:
		i = 0
		for line in locations: 
			RA = line
			RAvalue = driver.find_element_by_name("RA"); 
			RAvalue.clear() 
			RAvalue.send_keys(RA) 

			Imagesize = driver.find_element_by_name("ImageSize"); #same process as above
			Imagesize.clear()
			Imagesize.send_keys('1')

			Imagetype = driver.find_element_by_xpath("//input[@name='ImageType'][@value='FITS File']").click() #selects the FITS file option

			Submit = driver.find_element_by_name(".submit").click()	#finds the download button and clicks it
			
			#checks to make sure the RA and Dec value option is still available
			#if they are not, then it adds the RA and Dec value to a new file that holds the discarded values and goes back to the previous window
			#if they are, then it adds it to a file that holds the good values and moves on 
			try:
				driver.find_element_by_name("RA"); 
			except NoSuchElementException as exception:
				with open(discardedFilename, "a+") as discardedImages:
					discardedImages.write(RA)
					discardedImages.close()
					i += 1
					driver.back()
			else:
				with open(savedFilename, "a+") as savedImages:
					savedImages.write(RA)
					savedImages.close()
		print(i, 'locations not found') 
		driver.close() 
		
main()
		


	


import string, argparse, codecs, os, json, re, sys
import glob
import requests
import jsbeautifier
import wget

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.firefox.options import Options
from urls import urls

'''
Processing input parameters
'''
if len(sys.argv) != 3:
	print("Required Parameters:\n(1) Total Number of Machines \n(2) Current Machine Number")
	sys.exit(0)
totalMachines = int(sys.argv[1])
currentMachineNumber = int(sys.argv[2])
if (totalMachines < 1) or (currentMachineNumber <= 0) or (currentMachineNumber > totalMachines):
	print("First Argumnet should be total number of machines.\nSecond Argument should be current machine number.")
	sys.exit(0)
totalURLs = len(urls)
chunkSize = int(totalURLs/totalMachines)
endingIndex = chunkSize*currentMachineNumber
startingIndex = endingIndex - chunkSize
if currentMachineNumber == totalMachines: #useful when urls not divisible by total machines
	endingIndex = len(urls)
chunkedURLs = urls[startingIndex:endingIndex]
print("Total URLs to process (by this machine): ", len(chunkedURLs))
print("Starting and ending indices: ", startingIndex, endingIndex)



options = Options()
options.headless = True

# create a new Firefox session
driver = webdriver.Firefox(executable_path= "./geckodriver" , options=options)
driver.implicitly_wait(30)
driver.maximize_window()


cnt = 0
sCnt = 0
logCount = 0
LIMIT = 200 #200 sites data will be kept in memory
limit = LIMIT
sourceToURLLog = {} #for tracking back a script to its url
logCount = len(glob.glob("./logs/*")) #Setting log count to current number of files in log/ folder
urlToFilePath = {} #for optimization purposes

'''
fetchData will make a get request
with a timeout and if the request
fails, it will retry (total tries = 5)
'''
def fetchData(src):
	try:
		if src in urlToFilePath:
			with open(urlToFilePath[src]) as f: data = f.read()
			return data
	except: pass

	for i in range(0, 5): #5 retries
		try:
			req = requests.get(src, timeout=120) 
			script_source = req.text
			return script_source
		except:
			print("retrying ", src, " ...") 
			pass
	return ""

for url in chunkedURLs:
	try:
		cnt += 1
		limit -= 1

		print ("{0} {1} ({2})".format(cnt, url, sCnt))
		driver.get("http://" + url)

		html_source = driver.page_source
		html = BeautifulSoup(html_source, 'html.parser')

		folderName = "./data/" + url.replace("https://","").replace("http://","")
		os.system("mkdir " + folderName)

		#Here is the part which extracts Scripts
		scripts = driver.find_elements_by_tag_name("script")
		i = 0

		for script in scripts:
			i += 1
			sCnt += 1

			print ("script{0}".format(i))

			try:				
				#Get External scripts (scripts with src attribute)
				src = script.get_attribute("src")
				if src != "": 
					script_source = fetchData(src)
					if script_source == "": raise Exception("Couldn't get script source")
				
				#Get Inline scripts
				else:
					script_source = script.get_attribute("outerHTML")


				#Writing the retrieved script into respective folder
				scriptName = folderName+"/script{0}.js".format(i)
				with open(scriptName, "w") as f: 
					urlToFilePath[src] = scriptName
					f.write(jsbeautifier.beautify(script_source))

				#Logging into sourceToURLLog
				sourceURL = url
				if src != "": sourceURL = src
				sourceToURLLog[scriptName] = sourceURL
			except:
				i -= 1
				sCnt -= 1

		#Writing sourceToURLLog to file after completion of each site (url)
		if limit <= 0:
			try:
				with open("logs/sourceToURLLog"+str(logCount)+".json", "w") as f: 
					f.write(json.dumps(sourceToURLLog, indent=4))
				logCount += 1
				limit = LIMIT
				sourceToURLLog = {} #clearing memory
			except Exception as e:
				print(e)

	except:
		continue

	
driver.quit()

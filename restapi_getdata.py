# orginal source : https://www.splunk.com/blog/2011/08/02/splunk-rest-api-is-easy-to-use.html
# modified by HyunHo Noh 20180422


#Step 1: Get a session key

import urllib
import lxml.html
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseurl = 'https://localhost:8089'
username = 'admin'
password = '1'

url = baseurl + '/services/auth/login'
data = urllib.parse.urlencode({'username': username, 'password': password})

with requests.post(url, data=data, verify=False) as req:
    sessionkey = lxml.html.fromstring(req.content)[0].text
print("sessionkey {}".format(sessionkey))

#Step 2: Create a search job
searchquery = 'index="_internal" | head 10'
if not searchquery.startswith('search'):
    searchquery = 'search ' + searchquery

searchjoburl = baseurl + '/services/search/jobs'
with requests.post(searchjoburl, verify=False, 
              data=urllib.parse.urlencode({'search': searchquery}),
              headers={'Authorization': 'Splunk {}'.format(sessionkey)}) as req:
    sid = lxml.html.fromstring(req.content)[0].text
print("sid {}".format(sid))

#Step 3: Get the search status

servicessearchstatusstr = '/services/search/jobs/%s/' % sid

isnotdone = True
while isnotdone:
    with requests.post(baseurl + servicessearchstatusstr, 
                             headers={'Authorization': 'Splunk {}'.format(sessionkey)}, verify=False) as searchstatus:
            
        isDone=lxml.html.fromstring(searchstatus.content)
        
        isdonestatus=isDone.cssselect('key[name=isDone]')[0].text
        if(isdonestatus == '1'):
            isnotdone = False
print ("search status : {}".format(isdonestatus))

#Step 4: Get the search results
services_search_results_str = "/services/search/jobs/{}/results?output_mode=json&count=0".format(sid)
print(services_search_results_str)

with requests.get(baseurl + services_search_results_str, 
                 headers={'Authorization': 'Splunk {}'.format(sessionkey)}, verify=False) as searchresults:
    print(searchresults.content)
            
print ("search result: {}".format(searchresults.content))

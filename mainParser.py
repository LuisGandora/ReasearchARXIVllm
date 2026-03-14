#dependencie: pip install urllib, pip install --upgrade certifi
import urllib, urllib.request
import certifi 
import ssl

#This is meant to be imported to utilize this function specifically

#Tool for parsing ARXIV 
#Refer to https://google.github.io/adk-docs/tools/ for more info
def parseARXIV(researchTopic : str ,max_results : int):

    #SSL context that uses certifi's trusted certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    url = f'http://export.arxiv.org/api/query?search_query=all:{researchTopic}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url, context=ssl_context) 
    print(data.read().decode('utf-8'))

#For testing
# parseARXIV("Toys", 5)

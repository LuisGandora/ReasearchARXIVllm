#dependencie: pip install urllib, pip install --upgrade certifi
import urllib, urllib.request
import certifi 
import ssl
import textwrap

#This is meant to be imported to utilize this function specifically

#Tool for parsing ARXIV 
#Refer to https://google.github.io/adk-docs/tools/ for more info
def parseARXIV(researchTopic : str ,max_results : int)->str: 
    print("Called Oh Yeah")
    """
        Retrieves max_result number of papers related to a research topic inputted.

        Accepts a research topic :str for the main query and a max_results : int for how many papers the tool needs to parse

        Returns: 'utf-8' decoded articles from urllib that the user can use to generate new research topics
    """
    #SSL context that uses certifi's trusted certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    url = f'http://export.arxiv.org/api/query?search_query=all:{researchTopic}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url, context=ssl_context) 
    return data.read().decode('utf-8')

#For testing
# print(parseARXIV("Toys", 2))

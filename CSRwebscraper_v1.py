# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:35:41 2016

@author: Harrison
"""

from bs4 import BeautifulSoup
import requests

BASE_URL = "http://www.chinacsrmap.org"
DIRECTORY_URL = "/Org_List_EN.asp?LstFlt_Page="



### Part 1: first find all relevant links on all 20 pages
allLinks = []

for page in range(1,21): #21 is last index
    r = requests.get(BASE_URL + DIRECTORY_URL + str(page)) #request page
    html_raw = r.text #get the text
    soup = BeautifulSoup(html_raw,"lxml") #create BS object
    links_HTML = soup.find("div","containerList") #find links
    
    #run for loop to get all links one by one and put into allLinks
    for teasers in links_HTML.findAll("div","teaserBox"): #get all links
        preLink = teasers.get('onclick').replace('location.href=\'','') #remove the weird pre-tags
        allLinks.append(preLink.replace('\';','')) #remove the weird post-tags and append
        print(preLink.replace('\';','')) #just so that we can see it's moving

#just to check
len(allLinks)





### Part 2: now search through pages to see if they have keywords we're looking for
allCSRNames = []
allCSRLinks = []

##KEYWORDS #CHANGE KEYWORDS HERE
FI_keywords = ['financial inclusion'] 
Finance_keywords = ['finance','financial']
Education_keywords = ['education','educate','school']
Rural_keywords = ['rural','development']
Women_keywords = ['women','empowerment','mother']
ML_keywords = ['migrant','labor']
Digital_keywords = ['digital']

FI_Relevance = [-999] * len(allLinks)
Finance_Relevance = [-999] * len(allLinks)
Education_Relevance = [-999] * len(allLinks)
Rural_Relevance = [-999] * len(allLinks)
Women_Relevance = [-999] * len(allLinks)
ML_Relevance = [-999] * len(allLinks)
Digital_Relevance = [-999] * len(allLinks)


for index,link in enumerate(allLinks):
    #print(BASE_URL + link)
    fullLink = BASE_URL + link
    linkrequest = requests.get(fullLink) #request page
    linksoup = BeautifulSoup(linkrequest.text,"lxml") #create BS object
    
    # get org name
    pretitle = linksoup.find("div","OrgInfoPageTitle") #look for org title
    title = pretitle.find(text=True) #extract text
    print(title) #just to see that it's running
    
    # populate CSR names and links
    title = title.replace('\r\n','').replace('        ','').replace('      ','') #clean title up of junk
    allCSRNames.append(title) #add to CSR name list
    allCSRLinks.append(fullLink) #add to CSR link list

    # get all section text and search for keywords
    text = linksoup.findAll("div","OrgInfoSectionContent") #find all content sections
    
    # set relevance value from -999 to 0
    FI_Relevance[index] = 0
    Finance_Relevance[index] = 0
    Education_Relevance[index] = 0
    Rural_Relevance[index] = 0
    Women_Relevance[index] = 0
    ML_Relevance[index] = 0
    Digital_Relevance[index] = 0
    
    for block in text: 
        #search for FI keywords
        if any(words in block.get_text() for words in FI_keywords): #if it contains ANY of the keywords
            if FI_Relevance[index] == 1:
                continue
            else:
                FI_Relevance[index] += 1

        #search for Finance keywords
        if any(words in block.get_text() for words in Finance_keywords): #if it contains ANY of the keywords
            if Finance_Relevance[index] == 1:
                continue
            else:
                Finance_Relevance[index] += 1
        
        #search for Education keywords
        if any(words in block.get_text() for words in Education_keywords): #if it contains ANY of the keywords
            if Education_Relevance[index] == 1:
                continue
            else:
                Education_Relevance[index] += 1

        #search for Rural keywords
        if any(words in block.get_text() for words in Rural_keywords): #if it contains ANY of the keywords
            if Rural_Relevance[index] == 1:
                continue
            else:
                Rural_Relevance[index] += 1

        #search for Women keywords
        if any(words in block.get_text() for words in Women_keywords): #if it contains ANY of the keywords
            if Women_Relevance[index] == 1:
                continue
            else:
                Women_Relevance[index] += 1

        #search for ML keywords
        if any(words in block.get_text() for words in ML_keywords): #if it contains ANY of the keywords
            if ML_Relevance[index] == 1:
                continue
            else:
                ML_Relevance[index] += 1
            
        #search for Digital keywords
        if any(words in block.get_text() for words in Digital_keywords): #if it contains ANY of the keywords
            if Digital_Relevance[index] == 1:
                continue
            else:
                Digital_Relevance[index] += 1
  



### Part 3: now put it in a csv
import pandas as pd

#dictionary = dict(zip(allCSRNames, allCSRLinks, FI_Relevance))
df = pd.DataFrame({'CSR_Name' : allCSRNames
                  , 'CSR_Link' : allCSRLinks
                  , 'FI_Relevance' : FI_Relevance
                  , 'Finance_Relevance' : Finance_Relevance
                  , 'Education_Relevance' : Education_Relevance
                  , 'Rural_Relevance' : Rural_Relevance
                  , 'Women_Relevance' : Women_Relevance
                  , 'ML_Relevance' : ML_Relevance
                  , 'Digital_Relevance' : Digital_Relevance})
df['Relevance_Score'] = df.sum(axis = 1)
df.to_csv("C:/Users/Harrison/Anaconda3/HARRISONSSCRIPTS/CSR_relevance.csv")


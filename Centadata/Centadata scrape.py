import urllib.request
import urllib.parse
import re
import sqlite3

def GetHTML(url):
#function to open a url and return the html as string
    headers ={}
    headers ['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url,headers=headers)
    resp = urllib.request.urlopen(req)
    text = resp.read().decode(resp.headers.get_content_charset())
    return (text)

def CreateTable():
	sql="CREATE TABLE `Transactions` (`NameEng` TEXT,`AddressEng` TEXT,"
	sql+="`NameChi` TEXT,`AddressChi` TEXT);"
	c.execute(sql)

def DB_Insert(add_matrix):
	c.executemany('INSERT INTO Transactions VALUES (?,?,?,?)',add_matrix)
	conn.commit()

#Connect to / create local SQLite DB
path='CentaTrans.db'
conn=sqlite3.connect(path)
c=conn.cursor()
#Calls the create table function. Only run first time
CreateTable()
	
#Obtain list of links from main page
home='http://www1.centadata.com/ephome.aspx'

links=re.findall(r'<a href="([^>]*)">',GetHTML(home))[13:50]
#linksChi=re.findall(r'href="([^>]*)">',GetHTML(homeChi))[17:50]


#Cycle through each link
for item in links:
    counter=0
    end=0
    while end==0:
    #loops through all pages until regex returns no values
        #create url and call function to get html

        baseEng='http://www1.centadata.com/'
        baseEng+=item
        baseEng=baseEng.replace("&page=0", "&page=")
        baseEng+=str(counter)
        srctextEng=GetHTML(baseEng)
        srctextEng=srctextEng.replace("\\'", "\'")

        baseChi='http://www1.centadata.com/'
        baseChi+=item
        baseChi=baseChi.replace("epaddresssearch1", "paddresssearch1")
        baseChi=baseChi.replace("&page=0", "&page=")
        baseChi+=str(counter)
        srctextChi=GetHTML(baseChi)
        srctextChi=srctextChi.replace("\\'", "\'")

        #use regex to pull names and addresses
        nameEng=re.findall(r'<span style="text-decoration:underline">([^<]*)</span>',srctextEng)
        addressEng=re.findall(r'<td class="tdscp1addr">([^&]*)&nbsp;',srctextEng)
        nameChi=re.findall(r'<span style="text-decoration:underline">([^<]*)</span>',srctextChi)
        addressChi=re.findall(r'<td class="tdscp1addr">([^&]*)&nbsp;',srctextChi)
        page=list(zip(nameEng,addressEng,nameChi,addressChi))
        
        if len(nameEng)==0:
            end=1
        else:
            counter+=1
            print(baseEng)
            DB_Insert(page)



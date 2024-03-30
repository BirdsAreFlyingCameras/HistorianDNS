import requests
from PyEnhance import WebTools
from bs4 import BeautifulSoup
from pprint import pprint as Pprint

class Main:

    def __init__(self, URL):
        self.SubDomains = []
        self.Records = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                        'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}

        self.WebTool = WebTools.WebTools()

        self.GetRecords(URL=URL)

    def GetRecords(self, URL):

        WebRequest = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=self.WebTool.RequestHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        IndexsForSoups = []
        ListForSoups = []

        AllTags = WebRequestSoup.descendants

        RecordsContainers = WebRequestSoup.find_all('h3')

        print(RecordsContainers)

        for RecordType in RecordsContainers:
            IndexsForSoups.append(WebRequest.text.index(str(RecordType)))
        print(IndexsForSoups)

        for Iter, Index in enumerate(IndexsForSoups):

            if Iter+1 == len(IndexsForSoups):
                print('!')
                break
            else:
                NextIndex = IndexsForSoups[Iter+1]
                ListForSoups.append(WebRequest.text[Index:NextIndex])

       # Pprint(ListForSoups)

        for PreSoup in ListForSoups:
            IterSoup = BeautifulSoup(PreSoup, 'html.parser')
            Items = IterSoup.find_all('p')
            print(Items)


Main(URL='bumble.com')
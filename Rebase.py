import requests
from PyEnhance import WebTools,TextSets
from bs4 import BeautifulSoup
from pprint import pprint as Pprint
import re
class Main:

    def __init__(self, URL):
        self.SubDomains = []
        self.Records = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                        'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}

        self.WebTool = WebTools.WebTools()

        self.Replace = []

        self.Tags = [
            "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi",
            "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code",
            "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "dialog",
            "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer",
            "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "html",
            "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link",
            "main", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object",
            "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress",
            "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "slot", "small", "source",
            "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea",
            "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video",
            "wbr"
        ]

        print(max([len(Tag) for Tag in self.Tags]))

        for Tag in self.Tags:
            self.Replace.append(f'<{Tag}>')
            self.Replace.append(f'</{Tag}>')
            self.Replace.append(f'<{Tag}/>')

        self.GetBasePageRecords(URL=URL)


        self.RecordTypes = ["SOA","NS","MX","A","AAAA","CNAME", "PTR", "TXT"]
        for RecordType in self.RecordTypes:
            self.GetHistory(URL=URL, Type=RecordType.lower())

        for RecordType in self.RecordTypes:
            print(self.Records[RecordType])

    def GetBasePageRecords(self, URL):

        WebRequest = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=self.WebTool.RequestHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        IndexsForSoups = []
        ListForSoups = []

        RecordsContainers = WebRequestSoup.find_all('h3')

        #print(RecordsContainers)

        for RecordType in RecordsContainers:
            IndexsForSoups.append(WebRequest.text.index(str(RecordType)))

        for Iter, Index in enumerate(IndexsForSoups):

            if Iter+1 == len(IndexsForSoups):
                break
            else:
                NextIndex = IndexsForSoups[Iter+1]
                ListForSoups.append(WebRequest.text[Index:NextIndex])

        DictGuide = {0:"SOA", 1:"NS", 2:"MX", 3:"A", 4:"AAAA", 5:"CNAME", 6:"PTR", 7:"TXT"}

        for Iter, PreSoup in enumerate(ListForSoups):
            IterSoup = BeautifulSoup(PreSoup, 'html.parser')
            Items = IterSoup.find_all('p')

            TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

            #print([TagPattern.sub('', str(Item).replace('\n', ' ')) for Item in Items])

            self.Records[DictGuide.get(Iter)].append([TagPattern.sub('', str(Item).replace('\n', ' ')) for Item in Items])


    def GetHistory(self, URL, Type):

        DateRegex = re.compile("\d{4}-\d{2}-\d{2}\s-&gt;\s\d{4}-\d{2}-\d{2}")

        WebRequest = requests.get(f'https://dnshistory.org/historical-dns-records/{Type}/{URL}', headers=self.WebTool.RequestHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        Content = WebRequestSoup.find_all("p")

        IndexsForRecords = re.findall(DateRegex, str(Content))

        print(IndexsForRecords)

        Content = str(Content)

        TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

        for Iter, DataForIndex in enumerate(IndexsForRecords):

            if Iter+1 == len(IndexsForRecords):
                Index1 = Content.index(DataForIndex)
                Index2 = Content[Index1:].index('</p>')
                Index2 = int(Index1)+int(Index2)
                Record = Content[Index1:Index2]

                #print(Content[Index1:Index2])
                #print((TagPattern.sub('', str(Record).replace('\n', ' '))))

                self.Records[Type.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))

                break

            Index1 = Content.index(DataForIndex)
            Index2 = Content.index(IndexsForRecords[Iter+1])
            #print(Content[Index1:Index2])
            Record = Content[Index1:Index2]


            #self.Records[Type.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))

            #print((TagPattern.sub('', str(Record).replace('\n', ' '))))

            self.Records[Type.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))



Main(URL='bumble.com')
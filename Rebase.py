import requests
from PyEnhance import WebTools,TextSets
from bs4 import BeautifulSoup
from pprint import pprint as Pprint
import re

from rich.console import Console
from rich.table import Table
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

        for Tag in self.Tags:
            self.Replace.append(f'<{Tag}>')
            self.Replace.append(f'</{Tag}>')
            self.Replace.append(f'<{Tag}/>')

        self.GetBasePageRecords(URL=URL)


        self.RecordTypes = ["SOA","NS","MX","A","AAAA","CNAME", "PTR", "TXT"]
        for RecordType in self.RecordTypes:
            self.GetHistory(URL=URL, Type=RecordType.lower())

        self.Filter()

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

            self.Records[DictGuide.get(Iter)].append(''.join([TagPattern.sub('', str(Item).replace('\n', ' ')) for Item in Items]).strip())


    def GetHistory(self, URL, Type):

        DateRegex = re.compile("\d{4}-\d{2}-\d{2}\s-&gt;\s\d{4}-\d{2}-\d{2}")

        WebRequest = requests.get(f'https://dnshistory.org/historical-dns-records/{Type}/{URL}', headers=self.WebTool.RequestHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        Content = WebRequestSoup.find_all("p")

        IndexsForRecords = re.findall(DateRegex, str(Content))

        Content = str(Content)

        TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

        for Iter, DataForIndex in enumerate(IndexsForRecords):

            if Iter+1 == len(IndexsForRecords):
                Index1 = Content.index(DataForIndex)
                Index2 = Content[Index1:].index('</p>')
                Index2 = int(Index1)+int(Index2)
                Record = Content[Index1:Index2]

                self.Records[Type.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))
                break

            Index1 = Content.index(DataForIndex)
            Index2 = Content.index(IndexsForRecords[Iter+1])
            Record = Content[Index1:Index2]

            self.Records[Type.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))

    def Filter(self):
        self.RecordsToBeFiltered = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                                    'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}

        self.RecordsFiltered = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                                'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}


        DateRegex = re.compile("(?=\d{4}-\d{2}-\d{2}\s-&gt;\s\d{4}-\d{2}-\d{2})")
        for RecordType in self.RecordTypes:
            self.RecordsToBeFiltered[RecordType] = re.split(DateRegex, ''.join(self.Records[RecordType]))


        for RecordType in self.RecordTypes:
            for iter, Record in enumerate(self.RecordsToBeFiltered[RecordType]):
                if not Record == "":
                    Record = str(Record).replace('-&gt;', '->')

                    if RecordType == "SOA":

                        Record = Record.replace('&lt;', "").replace('&gt;', '')

                        if iter == 0 or iter == 1:
                            NewLineList = ["MName:", "Serial:", "Refresh:", "Retry:", "Expire:"]
                        else:
                            NewLineList = ["MName:", "RName:", "Serial:", "Refresh:", "Retry:", "Expire:"]

                        for NewLine in NewLineList:
                            NewLineIndex = Record.index(NewLine)
                            Record = f"{Record[:NewLineIndex]}\n{Record[NewLineIndex:]}"


                    if RecordType == "NS" or RecordType == "A" or RecordType == "AAAA" or RecordType == "MX":
                        Index1 = Record.index('<')
                        Index2 = Record.rindex('>')
                        Record = f"{Record[:Index1]}{Record[Index2+1:]}"
                    self.RecordsFiltered[RecordType].append(str(Record))


        self.Output()
        #for RecordType in self.RecordTypes:
        #    print(self.RecordsFiltered[RecordType])

    def Output(self):

        #for RecordType in self.RecordTypes:

        #    print('\n')
        #    print(f"Record Type: {RecordType}")
        #    for Record in self.RecordsFiltered[RecordType]:
        #        print(Record)

        LongestList = max(self.RecordsFiltered['SOA'], self.RecordsFiltered['NS'], self.RecordsFiltered['MX'], self.RecordsFiltered['A'], self.RecordsFiltered['AAAA'], self.RecordsFiltered['CNAME'], self.RecordsFiltered['PTR'], self.RecordsFiltered['TXT'])

        for RecordType in self.RecordTypes:
            for i in range(len(LongestList) - len(self.RecordsFiltered[RecordType])):
                self.RecordsFiltered[RecordType] += [" "]


        RecordTupsForTables = ('SOA','NS'),("MX","A"),("AAAA","CNAME"),("PTR","TXT")

        for RecordType1, RecordType2 in RecordTupsForTables:
            table = Table()
            table.title_style = "bold"
            table.border_style = "rgb(255,255,255)"
            table.add_column(f"{RecordType1}", justify="right", style="rgb(255,255,255)", no_wrap=True)
            table.add_column(f"{RecordType2}", style="rgb(255,255,255)", no_wrap=True)

            for RecordType1, RecordType2 in zip(self.RecordsFiltered[RecordType1], self.RecordsFiltered[RecordType2]):
                table.add_row(RecordType1, RecordType2)

            console = Console()
            console.print(table)

Main(URL='bumble.com')
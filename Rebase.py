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
            self.RecordsToBeFiltered[RecordType] = list(dict.fromkeys(self.RecordsToBeFiltered[RecordType])) # Removes Dupes

        for RecordType in self.RecordTypes:
            for iter, Record in enumerate(self.RecordsToBeFiltered[RecordType]):
                if not Record == "":
                    Record = str(Record).replace('-&gt;', '⇒')

                    if RecordType == "SOA":

                        Record = Record.replace('&lt;', "").replace('&gt;', '')

                        if iter == 0 or iter == 1:
                            NewLineList = ["MName:", "Serial:", "Refresh:", "Retry:", "Expire:"]
                        else:
                            NewLineList = ["MName:", "RName:", "Serial:", "Refresh:", "Retry:", "Expire:"]

                        for NewLine in NewLineList:
                            NewLineIndex = Record.index(NewLine)

                            if NewLine == "MName:":
                                Record = f"\n{Record[:NewLineIndex]}\n{Record[NewLineIndex:]}"
                            else:
                                Record = f"{Record[:NewLineIndex]}\n{Record[NewLineIndex:]}"

                    if RecordType == "NS" or RecordType == "A" or RecordType == "AAAA" or RecordType == "MX":
                        Index1 = Record.index('<')
                        Index2 = Record.rindex('>')
                        Record = f"{Record[:Index1]}{Record[Index2+1:]}"
                    self.RecordsFiltered[RecordType].append(str(Record))
        self.Output()

    def Output(self):

        LongestList = max(self.RecordsFiltered['SOA'], self.RecordsFiltered['NS'], self.RecordsFiltered['MX'], self.RecordsFiltered['A'], self.RecordsFiltered['AAAA'], self.RecordsFiltered['CNAME'], self.RecordsFiltered['PTR'], self.RecordsFiltered['TXT'])

        RealLenDict = {
            "SOA":len(list(set(self.RecordsFiltered['SOA']))), "NS":len(list(set(self.RecordsFiltered['NS']))), "MX":len(list(set(self.RecordsFiltered['MX']))),
            "A":len(list(set(self.RecordsFiltered['A']))), "AAAA":len(list(set(self.RecordsFiltered['AAAA']))), "CNAME":len(list(set(self.RecordsFiltered['CNAME']))),
            "PTR":len(list(set(self.RecordsFiltered['PTR']))), "TXT":len(list(set(self.RecordsFiltered['TXT'])))
        }

        for RecordType in self.RecordTypes:
            for i in range(len(LongestList) - len(self.RecordsFiltered[RecordType])):
                self.RecordsFiltered[RecordType] += [" "]

        LongestStingsLeft = []
        LongestStingsRight = []

        for RecordType in ["SOA","A","MX","PTR"]:
            LongestStingInList = max(self.RecordsFiltered[RecordType], key=len)
            LongestStingsLeft.append(LongestStingInList)
        LongestStingLeft = len(max(LongestStingsLeft, key=len))

        for RecordType in ["NS","AAAA","CNAME","TXT"]:
            LongestStingInList = max(self.RecordsFiltered[RecordType], key=len)
            LongestStingsRight.append(LongestStingInList)
        LongestStingRight = len(max(LongestStingsRight, key=len))

        RecordTupsForTables = ('SOA','NS'),("A","AAAA"),("MX","CNAME"),("PTR","TXT")


        table = Table()
        table.show_header = False
        table.add_column(style="rgb(255,255,255)", no_wrap=True, min_width=LongestStingLeft+10)
        table.add_column(style="rgb(255,255,255)", no_wrap=True, min_width=LongestStingRight+10)
        table.border_style = "rgb(255,255,255)"


        for RecordType1, RecordType2 in RecordTupsForTables:

            table.title_style = "bold"

            Section1HeaderText = f'{RecordType1} Records'
            Section2HeaderText = f'{RecordType2} Records'

            Section1HeaderSides = f"{'═'*int(((LongestStingLeft+10)/2)-(len(Section1HeaderText)/2))}"
            Section2HeaderSides = f"{'═'*int(((LongestStingRight+10)/2)-(len(Section1HeaderText)/2))}"



            SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides}"
            SectionHeader2 = f"{Section2HeaderSides} {Section2HeaderText} {Section2HeaderSides}"

            table.add_row(SectionHeader1, SectionHeader2)
            table.add_section()

            LenRecordType1 = RealLenDict[RecordType1]
            LenRecordType2 = RealLenDict[RecordType2]

            if LenRecordType1 < 100 and LenRecordType2 < 100:
                DisplayRange = max(LenRecordType1, LenRecordType2)
            else:
                DisplayRange = 100

            if LenRecordType1 == 0:
                self.RecordsFiltered[RecordType1].insert(0, f"No {RecordType1} Records Found")
            if LenRecordType2 == 0:
                self.RecordsFiltered[RecordType2].insert(0, f"No {RecordType2} Records Found")

            table.add_row('', '')

            for RecordType1Item, RecordType2Item in zip(self.RecordsFiltered[RecordType1][:DisplayRange], self.RecordsFiltered[RecordType2][:DisplayRange]):
                table.add_row(RecordType1Item, RecordType2Item)

            table.add_row('', '')

            if RealLenDict[RecordType1] > 100:
                LeftRowText = f"There are {RealLenDict[RecordType1] - DisplayRange} More {RecordType1} records."
            else:
                LeftRowText = ''

            if RealLenDict[RecordType2] > 100:
                RightRowText = f"There are {RealLenDict[RecordType2] - DisplayRange} More {RecordType2} records."
            else:
                RightRowText = ''

            if not LeftRowText == '' and RightRowText == '':
                table.add_row(LeftRowText, RightRowText)

            table.add_section()


        console = Console()
        console.print(table)

Main(URL='bird.org')
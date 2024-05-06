import platform
import time
import requests
from PyEnhance import WebTools, TextSets, Stamps, Loading
from bs4 import BeautifulSoup
from pprint import pprint as Pprint
import re
from itertools import zip_longest
import os

from rich.align import Align
from rich.console import Console
from rich.table import Table
import math

Stamp = Stamps.Stamp

class Main:

    def __init__(self, URL):

        self.WebTool = WebTools.WebTools()
        self.Loading = Loading.Loading()

        self.Replace = []
        self.SubDomains = []

        self.Records = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                        'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}

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

        self.RecordTypes = ["SOA","NS","MX","A","AAAA","CNAME", "PTR", "TXT"]

        self.WebHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Cache-Control": "max-age=0",
            "Sec-CH-UA": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": "\"Windows\"",
            "Cookie": "sessionId=eyJpdiI6IklDVkZuQmFcL3NcLzN4Z1wvTmFcLzNnPT0iLCJ2YWx1ZSI6IlwvT1wvUnRQOHhcLzE2NGJcL1wvXC9cLzBcL1wvXC8wK3c9PSIsIm1hYyI6IjlkYzBmYWM1MjJlZjQ4MzI5YjFjNzg3MTQ0NjQ5ZDMwOTBiMjJhOWFjY2M2MzZiNTY5ZDgwN2E4YWE2NzE4YTEifQ%3D%3D; theme=light; csrftoken=ghPx4Dr56TjYVbnP5rSzG5hajkLQzN7b;"
        }

        self.URL = URL

        for Tag in self.Tags:
            self.Replace.append(f'<{Tag}>')
            self.Replace.append(f'</{Tag}>')
            self.Replace.append(f'<{Tag}/>')

        self.ClearScreenCommand = None
        if platform.system() == "Windows":
            self.UserOS = "Windows"
            self.ClearScreenCommand = "cls"
        elif platform.system() == "Linux":
            self.UserOS = "Linux"
            self.ClearScreenCommand = "clear"
        elif platform.system() == "Darwin":
            self.UserOS = "MacOS"
            self.ClearScreenCommand = "clear"
        else:
            self.UserOS = "Unknown"
            self.ClearScreenCommand = None


        self.Loading.Spin(Text="Checking If Request Will Be Blocked")
        
        
        #Function Calls
        
        self.GetBasePageRecords(URL=URL)

        for RecordType in self.RecordTypes:
            self.GetHistory(URL=URL, Type=RecordType.lower())

        self.Filter()


    def grouper(self,sequence, n, fillvalue=None): # Coded by ChatGPT
        args = [iter(sequence)] * n
        return [list(group) for group in zip_longest(*args, fillvalue=fillvalue)]


    def GetBasePageRecords(self, URL):

        WebRequest = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=self.WebHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')


        if WebRequest.status_code == 403: # If cloudflare captcha is returned
            self.Loading.Stop()
            os.system(self.ClearScreenCommand)
            print(f"{Stamp.Error} Request Blocked, Status code: {WebRequest.status_code}")
            exit()


        self.Loading.Stop()
        os.system(self.ClearScreenCommand)
        time.sleep(1)
        self.Loading.Spin(Text="Getting Records")


        IndexsForSoups = []
        ListForSoups = []

        RecordsContainers = WebRequestSoup.find_all('h3')

        for RecordType in RecordsContainers:
            IndexsForSoups.append(WebRequest.text.index(str(RecordType)))

        for Iter, Index in enumerate(IndexsForSoups):

            if Iter+1 == len(IndexsForSoups): # Checks if current loop iteration is the last
                break
            else:
                NextIndex = IndexsForSoups[Iter+1]
                ListForSoups.append(WebRequest.text[Index:NextIndex])


        DictGuide = {0:"SOA", 1:"NS", 2:"MX", 3:"A", 4:"AAAA", 5:"CNAME", 6:"PTR", 7:"TXT"}

        for Iter, PreSoup in enumerate(ListForSoups):
            IterSoup = BeautifulSoup(PreSoup, 'html.parser')
            Items = IterSoup.find_all('p')

            TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

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

            if Iter+1 == len(IndexsForRecords): # Checks if current loop iteration is the last
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
            #self.RecordsToBeFiltered[RecordType] = list(dict.fromkeys(self.RecordsToBeFiltered[RecordType])) # Removes Dupes

        for RecordType in self.RecordTypes:
            for iter, Record in enumerate(self.RecordsToBeFiltered[RecordType]):
                
                if Record != "":
                    Record = str(Record).replace('-&gt;', '⇒')

                    if RecordType == "SOA":

                        Record = Record.replace('&lt;', "").replace('&gt;', '')

                        if iter == 0 or iter == 1: # The first SOA record doesn't have the RName field
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

            print(f"Len Of {RecordType}: {len(self.RecordsFiltered[RecordType])}")
        print("_____________________________________")

        self.Output()

    def Output(self):

        self.Loading.Stop()
        #os.system(self.ClearScreenCommand) | Debug Uncomment

        LongestList = max(self.RecordsFiltered['SOA'], self.RecordsFiltered['NS'], self.RecordsFiltered['MX'], self.RecordsFiltered['A'], self.RecordsFiltered['AAAA'], self.RecordsFiltered['CNAME'], self.RecordsFiltered['PTR'], self.RecordsFiltered['TXT'])

        RealLenDict = {
            "SOA":len(self.RecordsFiltered['SOA']), "NS":len(self.RecordsFiltered['NS']), "MX":len(self.RecordsFiltered['MX']),
            "A":len(self.RecordsFiltered['A']), "AAAA":len(self.RecordsFiltered['AAAA']), "CNAME":len(self.RecordsFiltered['CNAME']),
            "PTR":len(self.RecordsFiltered['PTR']), "TXT":len(self.RecordsFiltered['TXT'])
        }

        self.NS_LessThen6 = False

        for RecordType in self.RecordTypes:
            print(f"Len Of {RecordType} Before Group Function: {RealLenDict[RecordType]}")
            if RecordType == "NS":
                
               if RealLenDict["NS"] < 6:

                    self.NS_LessThen6 = True
                    self.RecordsFiltered[RecordType].append('\n'.join(self.RecordsFiltered[RecordType]))
                    self.RecordsFiltered[RecordType] = self.RecordsFiltered[RecordType][-1:]

                    for _ in range(len(LongestList) - RealLenDict["NS"]):
                        self.RecordsFiltered[RecordType].append(" ")

               else:
                   GroupedList = list(self.grouper(self.RecordsFiltered[RecordType], 7, fillvalue=''))
                   self.RecordsFiltered[RecordType] = GroupedList

            else:
                for i in range(len(LongestList) - len(self.RecordsFiltered[RecordType])):
                    self.RecordsFiltered[RecordType] += [" "]

            print(f"Len Of {RecordType} After Group Function: {RealLenDict[RecordType]}")

        TermSize = os.get_terminal_size()
        TermWidth = TermSize.columns


        table = Table()
        table.show_header = False
        table.add_column(style="rgb(255,255,255)", no_wrap=True, width=math.floor(TermWidth/2))
        table.add_column(style="rgb(255,255,255)", no_wrap=True, width=math.floor(TermWidth/2))
        table.border_style = "rgb(255,255,255)"
        table.title_style = "bold"

        RecordTupsForTables = ('SOA','NS'),("A","AAAA"),("MX","CNAME"),("PTR","TXT")

        for RecordType1, RecordType2 in RecordTupsForTables:

            Section1HeaderText = f'{RecordType1} Records'
            Section2HeaderText = f'{RecordType2} Records'

            Section1HeaderTextLen = len(Section1HeaderText)
            Section2HeaderTextLen = len(Section2HeaderText)

            LeftColumnWidth = math.floor(TermWidth/2)
            RightColumnWidth = math.floor(TermWidth/2)

            SectionHeader1BufferInt = math.floor((LeftColumnWidth-Section2HeaderTextLen)/2)
            SectionHeader2BufferInt = math.floor((RightColumnWidth-Section1HeaderTextLen)/2)

            Section1HeaderSides = '═' * (SectionHeader1BufferInt-4) # Need to adjust
            Section2HeaderSides = '═' * (SectionHeader2BufferInt-4) # Need to adjust 

            SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides}"
            SectionHeader2 = f"{Section2HeaderSides} {Section2HeaderText} {Section2HeaderSides}"


            # ||| Start of code I will probably remove |||

            if len(SectionHeader1) > LeftColumnWidth:
                Diff = len(SectionHeader1) - (LeftColumnWidth)
                #print(f"Diff: {Diff}")
                if Diff == 1:
                    SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides[:-1]}"
                else:
                    Section1HeaderSides = Section1HeaderSides[:-int(Diff/2)]
                    SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides}"

            if len(SectionHeader2) > RightColumnWidth:
                Diff = len(SectionHeader2) - (RightColumnWidth)
                #print(f"Diff: {Diff}")
                if Diff == 1:
                    SectionHeader2 = f"{Section2HeaderSides} {Section2HeaderText} {Section2HeaderSides[:-1]}"
                else:
                    Section2HeaderSides = Section2HeaderSides[:-int(Diff/2)]
                    SectionHeader2 = f"{Section2HeaderSides} {Section2HeaderText} {Section2HeaderSides}"

            # ||| End of code I will probably remove |||


            table.add_row(Align(SectionHeader1, align="center"), Align(SectionHeader2, align="center"))
            table.add_section()


            LenRecordType1 = RealLenDict[RecordType1]
            LenRecordType2 = RealLenDict[RecordType2]

            print(LenRecordType1)
            print(LenRecordType2)

            if LenRecordType1 < 100 and LenRecordType2 < 100:
                DisplayRange = max(LenRecordType1, LenRecordType2)
            else:
                DisplayRange = 100

            if LenRecordType1 == 0:
                print("___________________________________") # Debug String
                print(f"No {RecordType1} Records Found") # Debug String
                self.RecordsFiltered[RecordType1].insert(0, f"No {RecordType1} Records Found")
                print(self.RecordsFiltered[RecordType1]) # Debug String
            if LenRecordType2 == 0:
                print("___________________________________") # Debug String
                print(f"No {RecordType2} Records Found") # Debug String
                self.RecordsFiltered[RecordType2].insert(0, f"No {RecordType2} Records Found")
                print(self.RecordsFiltered[RecordType2]) # Debug String



            table.add_row('', '') # Table Padding


            for RecordType1Item, RecordType2Item in zip(self.RecordsFiltered[RecordType1][:DisplayRange], self.RecordsFiltered[RecordType2][:DisplayRange]):

                print(RecordType1Item)# Debug String
                print(RecordType2Item)# Debug String

                if RecordType2 == "NS":
                    if self.NS_LessThen6 != True:
                        #print(f"Record Type 2 Item: {RecordType2Item}")
                        RecordType2Item = '\n'.join(RecordType2Item)
                        table.add_row(RecordType1Item, RecordType2Item)
                    else:
                        table.add_row(RecordType1Item, RecordType2Item)
                else:
                    table.add_row(RecordType1Item, RecordType2Item)

            table.add_row('', '')


            print("+++")
            print(f"Len Of {RecordType1}: {RealLenDict[RecordType1]}")
            print(f"Len Of {RecordType2}: {RealLenDict[RecordType2]}")


            if RealLenDict[RecordType1] > 100:
                LeftRowText = f"There are {RealLenDict[RecordType1] - DisplayRange} More {RecordType1} records."
            else:
                LeftRowText = ''

            if RealLenDict[RecordType2] > 100:
                RightRowText = f"There are {RealLenDict[RecordType2] - DisplayRange} More {RecordType2} records."
            else:
                RightRowText = ''


            if LeftRowText != '' or RightRowText != '':
                table.add_row(LeftRowText, RightRowText)
            if LeftRowText != '' and RightRowText != '':
                table.add_row(LeftRowText, RightRowText)

            table.add_section() # Table Padding

        console = Console()
        console.print(table)

        self.SaveResults()


    def SaveResults(self):

        print('\n')

        SaveResultsChoice = input(f"{Stamps.Stamp.Input} Save Results [y/n]: ")

        if SaveResultsChoice == "y" or SaveResultsChoice == "Y" or SaveResultsChoice == "yes" or SaveResultsChoice == "Yes":

            SaveFileName = f"HistorianDNS-{self.URL}.txt"

            if os.path.exists(SaveFileName):
                print("\n")
                PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                if PathAlreadyExistChoice == "1":
                    os.remove(SaveFileName)

                elif PathAlreadyExistChoice == "2":
                    print("\n")
                    SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                    if not SaveFileName.endswith(".txt"):
                        SaveFileName = f"{SaveFileName}.txt"

                elif PathAlreadyExistChoice == "3":
                    exit()

                else:
                    print('\n')
                    print(f"{Stamps.Stamp.Error} Invalid Choice")
                    print("\n")
                    PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                    if PathAlreadyExistChoice == "1":
                        os.remove(SaveFileName)

                    if PathAlreadyExistChoice == "2":
                        print("\n")
                        SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                        if not SaveFileName.endswith(".txt"):
                            SaveFileName = f"{SaveFileName}.txt"

                    if PathAlreadyExistChoice == "3":
                        exit()

            BannerNameForTXT = SaveFileName.replace(".txt", "")

            with open(SaveFileName, 'x', encoding='utf-8') as f:

                f.write(f"┣━━━━━━━━━━ HistorianDNS Results for {BannerNameForTXT} ━━━━━━━━━━┫")

                f.write('\n')
                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ SOA Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('SOA') == 0:
                    for SOA in self.RecordsFiltered.get('SOA'):
                        if not SOA == " ":
                            f.write(SOA)
                            f.write('\n')

                else:
                    f.write("No SOA Records Found")


                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ NS Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('NS') == 0:
                    for NS in self.RecordsFiltered.get('NS'):
                        if not NS == " ":
                            f.write(SOA)
                            f.write('\n')

                else:
                    f.write("No NS Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ A Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('A') == 0:
                    for A in self.RecordsFiltered.get('A'):
                        if not A == " ":
                            f.write(A)
                            f.write('\n')

                else:
                    f.write("No A Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ AAAA Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('AAAA') == 0:
                    for AAAA in self.RecordsFiltered.get('AAAA'):
                        if not AAAA == " ":
                            f.write(AAAA)
                            f.write('\n')

                else:
                    f.write("No AAAA Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ MX Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('MX') == 0:
                    for MX in self.RecordsFiltered.get('MX'):
                        if not MX == " ":
                            f.write(MX)
                            f.write('\n')

                else:
                    f.write("No MX Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ CNAME Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('CNAME') == 0:
                    for CNAME in self.RecordsFiltered.get('CNAME'):
                        if not CNAME == " ":
                            f.write(CNAME)
                            f.write('\n')

                else:
                    f.write("No CNAME Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ PTR Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('PTR') == 0:
                    for PTR in self.RecordsFiltered.get('PTR'):
                        if not PTR == " ":
                            f.write(PTR)
                            f.write('\n')

                else:
                    f.write("No PTR Records Found")

                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ TXT Records ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if not self.RecordsFiltered.get('TXT') == 0:
                    for TXT in self.RecordsFiltered.get('TXT'):
                        if not TXT == " ":
                            f.write(TXT)
                            f.write('\n')

                else:
                    f.write("No TXT Records Found")

                f.write('\n')

            if self.UserOS == "Linux" or self.UserOS == "MacOS" or self.UserOS == "Unknown":
                print('\n')
                print(f"{Stamps.Stamp.Output} Saved Results to {os.path.dirname(os.path.abspath(__file__))}/{SaveFileName}")
                print('\n')
                print(f"{Stamps.Stamp.Info} Exiting")
            else:
                print('\n')
                print(f"{Stamps.Stamp.Output} Saved Results to {os.path.dirname(os.path.abspath(__file__))}\\{SaveFileName}")
                print('\n')
                print(f"{Stamps.Stamp.Info} Exiting")
        else:
            print('\n')
            print(f"{Stamps.Stamp.Info} Exiting")
            exit()

class UI:
    def __init__(self):
        self.ClearScreenCommand = None
        if platform.system() == "Windows":
            self.UserOS = "Windows"
            self.ClearScreenCommand = "cls"
        elif platform.system() == "Linux":
            self.UserOS = "Linux"
            self.ClearScreenCommand = "clear"
        elif platform.system() == "Darwin":
            self.UserOS = "MacOS"
            self.ClearScreenCommand = "clear"
        else:
            self.UserOS = "Unknown"
            self.ClearScreenCommand = None

        os.system(self.ClearScreenCommand)
        print(f"{Stamp.Info} Checking for an internet connection")
        if self.InternetConnection() == False:
            RetryChoice = (f"{Stamp.Error} No internet connection try agian? [y/n]: ")
            if RetryChoice.lower() == "y" or RetryChoice.lower() == "yes":
                print('\n')
                if self.InternetConnection() == False:
                    print(f"{Stamp.Error} Retry failed exiting")
                    exit()
            else:
                print(f"{Stamp.Info} Exiting")
                exit()
        else:
            os.system(self.ClearScreenCommand)
            self.Input()


    def InternetConnection(self):
        try:
            requests.get('https://google.com')
            return True

        except:
            return False

    def Input(self):
        URL = input(f"{Stamp.Input} Please Enter URL: ")

        if URL.startswith('https://'):
            URL = URL.replace("https://", "")
        if URL.startswith("http://"):
            URL = URL.replace("http://", "")
        print('\n')
        print(f"{Stamp.Info} Starting search on url: {URL}")

        time.sleep(2)

        os.system(self.ClearScreenCommand)

        Main(URL=URL)

#Main(URL='google.com')
#Main(URL='facebook.com')

UI()
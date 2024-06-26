import platform
import time
import requests
from PyEnhance import WebTools, Stamps, Loading
from bs4 import BeautifulSoup
import re
from itertools import zip_longest
import os
import sys, locale
from rich.align import Align
from rich.console import Console
from rich.table import Table
import math

Stamp = Stamps.Stamp

class Main:
    """
    Class that handles DNS record retrieval for a given URL.

    Attributes:
        WebTool (WebTools.WebTools): Instance of WebTools class.
        CheckingIfWebsiteWillBlockRequestLoading (Loading.Loading): Instance of Loading class for indicating that the script is checking if dnshistory.com will block the request.
        GettingRecordsLoading (Loading.Loading): Instance of Loading class for indicating the status of record retrieval.

        Replace (list): List of strings to replace in HTML tags.
        SubDomains (list): List of subdomains.

        Records (dict): Dictionary to store DNS records. Keys represent record types and values represent record data.

        Tags (list): List of HTML tags.

        RecordTypes (list): List of record types.

        WebHeaders (dict): Dictionary of HTTP headers used for web requests.

        URL (str): The URL of the website used to fetch its DNS records.

        ClearScreenCommand (str): Command to clear the screen based on user OS.
        UserOS (str): Operating system of the user.

    Methods:
        grouper(sequence, n, fillvalue=None): Groups the sequence into tuples of size n.
        GetBasePageRecords(URL): Retrieves the base page records for the given URL.
        GetHistory(URL, Type): Retrieves historical DNS records for the given URL and record type.
        Filter(): Filters the DNS records based on certain conditions.
    """
    def __init__(self, URL):
        """
        Initializes the object with the given URL.

        :param URL: The URL of the website used to fetch its DNS records.
        """
        self.URL = URL

        self.WebTool = WebTools.WebTools()
        self.CheckingIfWebsiteWillBlockRequestLoading = Loading.Loading()
        self.GettingRecordsLoading = Loading.Loading()

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


        if self.UserOS == "Windows":
            WinTerm = self.ShellIsWinTerm()
            if WinTerm is False:
                self.UnicodeSupported = False
            else:
                self.UnicodeSupported = True
        else:
            self.UnicodeSupported = True


        
        #Function Calls

        self.CheckingIfWebsiteWillBlockRequestLoading.Spin(Text="Checking If Request Will Be Blocked") # Starts Loading indicator

        self.GetBasePageRecords(URL=URL)

        for RecordType in self.RecordTypes:
            self.GetHistory(URL=URL, RecordType=RecordType.lower())

        self.Filter()



    def ShellIsWinTerm(self) -> bool: # Checks if users shell is the Windows Terminal. Need to do this due to cmd being unable to display the unicode arrow used for the output table.

        is_windows_terminal = sys.platform == "win32" and os.environ.get("WT_SESSION") # Got this snippet from Stack Overflow (https://stackoverflow.com/questions/62878172/how-do-i-detect-if-my-python-script-is-running-in-the-windows-terminal)

        if is_windows_terminal is None: # Will return none if shell is not Windows Terminal
            return False
        else:
            return True

    def grouper(self,sequence, n, fillvalue=None) -> list: # Coded by ChatGPT
        """
        :param sequence: The input sequence to be grouped.
        :param n: The number of elements in each group.
        :param fillvalue: The value used to fill any missing elements in the last group if the input sequence is not divisible evenly by n.
        :return: A list of grouped elements, where each group contains n elements from the input sequence. If the input sequence is not divisible evenly by n, the last group will be filled with fillvalue.
        """
        args = [iter(sequence)] * n
        return [list(group) for group in zip_longest(*args, fillvalue=fillvalue)]


    def GetBasePageRecords(self, URL:str):
        """
        :param URL: The URL of the website used to fetch its DNS records.
        :return: None
        """
        WebRequest = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=self.WebHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        if WebRequest.status_code == 403: # Triggerd if a CloudFlare captcha is returned
            self.CheckingIfWebsiteWillBlockRequestLoading.Stop()
            os.system(self.ClearScreenCommand)
            print(f"{Stamp.Error} Request Blocked, Status code: {WebRequest.status_code}")
            exit()

        self.CheckingIfWebsiteWillBlockRequestLoading.Stop() # Stops loading indicator so a new one can be made
        os.system(self.ClearScreenCommand)
        self.GettingRecordsLoading.Spin(Text="Getting Records") # Makes a new loading indicator


        IndexesForSoups = []
        ListForSoups = []

        RecordsContainers = WebRequestSoup.find_all('h3')

        for RecordType in RecordsContainers:
            IndexesForSoups.append(WebRequest.text.index(str(RecordType)))

        for Iter, Index in enumerate(IndexesForSoups):
            if Iter+1 == len(IndexesForSoups):  # Checks if current loop iteration is the last and if it is brakes the loop
                break
            else:
                NextIndex = IndexesForSoups[Iter+1]
                ListForSoups.append(WebRequest.text[Index:NextIndex])


        DictGuide = {0:"SOA", 1:"NS", 2:"MX", 3:"A", 4:"AAAA", 5:"CNAME", 6:"PTR", 7:"TXT"} # Dict of DNS record types

        for Iter, PreSoup in enumerate(ListForSoups):
            IterSoup = BeautifulSoup(PreSoup, 'html.parser')
            Items = IterSoup.find_all('p')

            TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

            self.Records[DictGuide.get(Iter)].append(''.join([TagPattern.sub('', str(Item).replace('\n', ' ')) for Item in Items]).strip())


    def GetHistory(self, URL:str, RecordType:str):

        """
        Get historical DNS records for a given URL and record type.

        :param URL: The URL for which to retrieve the historical DNS records.
        :type URL: str
        :param RecordType: The type of DNS record to retrieve (e.g., A, CNAME, MX).
        :type RecordType: str
        :return: None
        """

        DateRegex = re.compile("\d{4}-\d{2}-\d{2}\s-&gt;\s\d{4}-\d{2}-\d{2}") # Regex for finding dates in html code

        WebRequest = requests.get(f'https://dnshistory.org/historical-dns-records/{RecordType}/{URL}', headers=self.WebTool.RequestHeaders)
        WebRequestSoup = BeautifulSoup(WebRequest.text, 'html.parser')

        Content = WebRequestSoup.find_all("p")

        IndexesForRecords = re.findall(DateRegex, str(Content)) # Returns a list of indexes where the DateRegex was matched.

        Content = str(Content)

        TagPattern = re.compile(r'</?\w*/?>')  # Matches any HTML tag

        for Iter, DataForIndex in enumerate(IndexesForRecords):

            if Iter+1 == len(IndexesForRecords): # Checks if current loop iteration is the last
                Index1 = Content.index(DataForIndex)
                Index2 = Content[Index1:].index('</p>')
                Index2 = int(Index1)+int(Index2)
                Record = Content[Index1:Index2]
                self.Records[RecordType.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))
                break

            Index1 = Content.index(DataForIndex) # Index where DateRegex was matched
            Index2 = Content.index(IndexesForRecords[Iter+1]) # Index of next DateRegex match
            Record = Content[Index1:Index2] # This gets the full record. This works because

            self.Records[RecordType.upper()].append(TagPattern.sub('', str(Record).replace('\n', ' ')))

    def Filter(self):

        self.RecordsToBeFiltered = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                                    'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}

        self.RecordsFiltered = {'SOA':[], 'NS':[], 'MX':[], 'A':[],
                                'AAAA':[], 'CNAME':[], 'PTR':[], 'TXT':[]}


        DateRegex = re.compile("(?=\d{4}-\d{2}-\d{2}\s-&gt;\s\d{4}-\d{2}-\d{2})")
        
        
        for RecordType in self.RecordTypes:
            self.RecordsToBeFiltered[RecordType] = re.split(DateRegex, ''.join(self.Records[RecordType]))

        for RecordType in self.RecordTypes:
            for IterCount, Record in enumerate(self.RecordsToBeFiltered[RecordType]):
                
                if Record != "":
                    if self.UnicodeSupported is True:
                        Record = str(Record).replace('-&gt;', '⇒')
                    else:
                        Record = str(Record).replace('-&gt;', '->')

                    if RecordType == "SOA":

                        Record = Record.replace('&lt;', "").replace('&gt;', '')

                        NewLineList = ["MName:", "Serial:", "Refresh:", "Retry:", "Expire:"]

                        for NewLine in NewLineList:
                            NewLineIndex = Record.index(NewLine)

                            if NewLine == "MName:":
                                if IterCount == 0 or IterCount == 1:
                                    Record = f"{Record[:NewLineIndex]}\n{Record[NewLineIndex:]}"
                                else:
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

        self.GettingRecordsLoading.Stop() # Stops loading indicator
        os.system(self.ClearScreenCommand)

        LongestList = max(self.RecordsFiltered['SOA'], self.RecordsFiltered['NS'], self.RecordsFiltered['MX'], self.RecordsFiltered['A'], self.RecordsFiltered['AAAA'], self.RecordsFiltered['CNAME'], self.RecordsFiltered['PTR'], self.RecordsFiltered['TXT'])

        RealLenDict = {  # Need this due to the code below that will even out the lists so that they are all of equal length this dictionary is used to compare list length post equalization
            "SOA":len(self.RecordsFiltered['SOA']), "NS":len(self.RecordsFiltered['NS']), "MX":len(self.RecordsFiltered['MX']),
            "A":len(self.RecordsFiltered['A']), "AAAA":len(self.RecordsFiltered['AAAA']), "CNAME":len(self.RecordsFiltered['CNAME']),
            "PTR":len(self.RecordsFiltered['PTR']), "TXT":len(self.RecordsFiltered['TXT'])
        }

        self.NS_LessThen6 = False

        for IterCount, RecordType in enumerate(self.RecordTypes):

            if RecordType == "NS":  # This code is used to group NS records so they take up the same amount of lines as the corresponding SOA record

                if RealLenDict["NS"] < 6:
                     self.NS_LessThen6 = True
                     self.RecordsFiltered[RecordType].append('\n'.join(self.RecordsFiltered[RecordType]))
                     self.RecordsFiltered[RecordType] = self.RecordsFiltered[RecordType][-1:]

                     for _ in range(len(LongestList) - RealLenDict["NS"]):
                         self.RecordsFiltered[RecordType].append(" ")
                else:
                     if IterCount == 0: # Need to check this because the first SOA record is only 6 lines
                        GroupedList = list(self.grouper(self.RecordsFiltered[RecordType], 6, fillvalue=''))
                        self.RecordsFiltered[RecordType] = GroupedList
                     else:
                         GroupedList = list(self.grouper(self.RecordsFiltered[RecordType], 7, fillvalue=''))
                         self.RecordsFiltered[RecordType] = GroupedList

            else:
                for _ in range(len(LongestList) - len(self.RecordsFiltered[RecordType])):
                    self.RecordsFiltered[RecordType] += [" "]

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
                Diff = len(SectionHeader1) - LeftColumnWidth
                if Diff == 1:
                    SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides[:-1]}"
                else:
                    Section1HeaderSides = Section1HeaderSides[:-int(Diff/2)]
                    SectionHeader1 = f"{Section1HeaderSides} {Section1HeaderText} {Section1HeaderSides}"

            if len(SectionHeader2) > RightColumnWidth:
                Diff = len(SectionHeader2) - RightColumnWidth
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

            if LenRecordType1 < 100 and LenRecordType2 < 100:
                DisplayRange = max(LenRecordType1, LenRecordType2)
            else:
                DisplayRange = 100

            if LenRecordType1 == 0:
                self.RecordsFiltered[RecordType1].insert(0, f"No {RecordType1} Records Found")
            if LenRecordType2 == 0:
                self.RecordsFiltered[RecordType2].insert(0, f"No {RecordType2} Records Found")


            table.add_row('', '') # Table Padding


            for RecordType1Item, RecordType2Item in zip(self.RecordsFiltered[RecordType1][:DisplayRange], self.RecordsFiltered[RecordType2][:DisplayRange]):

                if RecordType2 == "NS":
                    if self.NS_LessThen6 != True:
                        RecordType2Item = '\n'.join(RecordType2Item)
                        table.add_row(RecordType1Item, RecordType2Item)
                    else:
                        table.add_row(RecordType1Item, RecordType2Item)
                else:
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

            if LeftRowText != '' or RightRowText != '' or LeftRowText != '' and RightRowText != '':
                table.add_row(LeftRowText, RightRowText)

            table.add_section() # Table Padding

        console = Console()
        console.print(table)

        self.SaveResults()


    def SaveResults(self):

            def MakeTXT(SaveFileName:str):

                RecordTypeList = [
                    "SOA",
                    "NS",
                    "MX",
                    "A",
                    "AAAA",
                    "CNAME",
                    "PTR",
                    "TXT"
                ]

                BannerNameForTXT = self.URL

                TableForTXT = Table()

                TableForTXT.show_header = False

                TableForTXT.add_section()

                TableForTXT.add_row(Align(f"Historian DNS Results For {BannerNameForTXT}", align="center"))

                TableForTXT.add_section()

                for RecordType in RecordTypeList:

                    if RecordType != "SOA":
                        TableForTXT.add_section()

                    TableForTXT.add_row(Align(f'{RecordType} Records', align="center"))

                    TableForTXT.add_section()

                    if RecordType != "NS":
                        for Record in self.RecordsFiltered[RecordType]:
                            TableForTXT.add_row(f"{Record}")
                    else:
                        for RecordsList in self.RecordsFiltered[RecordType]:
                            for Record in RecordsList:
                                TableForTXT.add_row(f"{Record}")


                from rich import print as rprint
                with open(SaveFileName, 'x', encoding='utf-8') as f:
                    rprint(TableForTXT, file=f)


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


            def SaveFileNameHandling():
                SaveFileName = f"HistorianDNS-{str(self.URL)[:str(self.URL).rindex('.')]}.txt"

                if os.path.exists(SaveFileName):
                    print("\n")
                    PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                    if PathAlreadyExistChoice == "1":
                        os.remove(SaveFileName)
                        MakeTXT(SaveFileName=SaveFileName)

                    elif PathAlreadyExistChoice == "2":
                        print("\n")
                        SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                        if not SaveFileName.endswith(".txt"):
                            SaveFileName = f"{SaveFileName}.txt"

                        MakeTXT(SaveFileName=SaveFileName)

                    elif PathAlreadyExistChoice == "3":
                        print(f"{Stamp.Info} Exiting...")
                        exit()

                    else:
                        print('\n')
                        print(f"{Stamps.Stamp.Error} Invalid Choice")
                        print("\n")
                        PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                        if PathAlreadyExistChoice == "1":
                            os.remove(SaveFileName)
                            MakeTXT(SaveFileName=SaveFileName)

                        if PathAlreadyExistChoice == "2":
                            print("\n")
                            SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                            if not SaveFileName.endswith(".txt"):
                                SaveFileName = f"{SaveFileName}.txt"
                            MakeTXT(SaveFileName=SaveFileName)

                        if PathAlreadyExistChoice == "3":
                            print(f"{Stamp.Info} Exiting...")
                            exit()
                else:
                    MakeTXT(SaveFileName=SaveFileName)

            print('\n')
            SaveResultsChoice = input(f"{Stamps.Stamp.Input} Save Results [y/n]: ")
            if SaveResultsChoice == "y" or SaveResultsChoice == "Y" or SaveResultsChoice == "yes" or SaveResultsChoice == "Yes":
                SaveFileNameHandling()
            else:
                print('\n')
                print(f"{Stamps.Stamp.Info} Exiting...")
                exit()

class UI:
    """
    This class represents the user interface for a program.
    It provides methods to check for an internet connection,
    get user input and start the main program.

    Attributes:
        ClearScreenCommand (str): The command to clear the screen based on the user's operating system.
        UserOS (str): The user's operating system.
    """
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
            RetryChoice = (f"{Stamp.Error} No internet connection try again? [y/n]: ")
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


    def InternetConnection(self) -> bool:
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

UI()
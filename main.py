from bs4 import BeautifulSoup
import requests
import re
import os

from PyEnhance import Counter

Counter = Counter.Counter



def SetUp():
    global URL
    PositiveStatusCodes = [200, 301, 401, 403]

    def Input():
        global URL
        URL = input('Enter URL: ')

        def Checks():
            global URL

            if URL.startswith('http://'):
                URL = URL.replace('http://', '')
            elif URL.startswith('https://'):
                URL = URL.replace('https://', '')
            else:
                pass

            if URL.startswith('www.'):
                URL = URL.replace('www.', '')
            else:
                pass

            if URL.endswith('/'):
                URL = URL.replace('/', '')
            else:
                pass

            if requests.get(f'http://{URL}').status_code not in PositiveStatusCodes:
                print(f'{URL} did not return a positive status code')
            else:
                print(f'{URL} did return a positive status code')

        Checks()

    Input()

    print(f'Using {URL} as url')

    if os.path.exists(f'{URL}'):
        pass
    else:
        os.mkdir(f'{URL}')
    os.chdir(f'{URL}')
SetUp()



def main():

    def CheckForHistoricalRecords(URL):
        def GetData():

            global DateRegex, TagP, Replace, tags, Data, RecordsDict

            RecordsDict = {}

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagH3 = (soup.find_all('h3'))

            Data = str(TagH3)

            Replace = ['[', ']', "'"]

        GetData()

        def FilterData():

            DataList = Data.split(',')

            RecordsList = []

            HistoricalRecordsList = []

            for i in DataList:

                Counter.Add()

                #print(Counter.Count)

                #print(i)

                if Counter.Count == 10:
                    break
                else:
                    RecordsList.append(i)

            for i in RecordsList:

                if 'href' in i:

                    FirstIndex = i.index('>')
                    LastIndex = i.index('-')

                    NameForDict = i[FirstIndex + 1:LastIndex]


                    HistoricalRecordsList.append(i)

                    if ' ' in NameForDict:

                        #print(f'Name For Dict: {NameForDict}')
                        #print(f'First Index: {FirstIndex}')
                        #print(f'Last Index: {LastIndex}')
                        NameForDict = NameForDict.strip()

                        RecordsDict[NameForDict] = True

                    else:

                        NameForDict = NameForDict.strip()

                        RecordsDict[NameForDict] = True
                else:

                    FirstIndex = i.index('>')
                    LastIndex = i.rindex('<')

                    NameForDict = i[FirstIndex + 1:LastIndex]

                    #print(f'Name For Dict NO HREF: {NameForDict}')
                    #print(f'First Index HREF: {FirstIndex}')
                    #print(f'Last Index HREF: {LastIndex}')

                    NameForDict = NameForDict.strip()

                    RecordsDict[NameForDict] = False

            #for i in RecordsDict.keys():
                #print(i)

            #print(RecordsDict)

        FilterData()

        def GetCurrentRecords():

            def GetData():

                global DateRegex, TagP, TagH3, Replace, tags, Data, RecordsDict

                DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
                tags = [
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

                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                         ' Chrome/90.0.4430.212 Safari/537.36'}

                Request = requests.get(f'https://dnshistory.org/dns-records/{URL}', headers=headers)

                Response = Request.text

                soup = BeautifulSoup(Response, 'html.parser')

                TagH3 = (soup.find_all('h3'))

                Replace = ['[', ']', "'"]

            GetData()

            def GetBasePageRecords():

                global BasePageDict

                BasePageDict = {}

                SpecialCharters = [
                    '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                    '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|', ';',
                    ':', "'", '"', ',', '.', '<', '>', '/', '?', '~', '`',
                ]

                for H3Tag in TagH3:

                    NameForDict = H3Tag.text[0:8]
                    NameForDict = str(NameForDict)


                    Index = re.findall('\W', NameForDict)

                    try:
                        if not len(Index) == 0:

                            IndexForSlice = NameForDict.index(Index[1])
                            NameForDict = NameForDict[0:IndexForSlice]

                    except IndexError:
                        continue

                    NameForDict = NameForDict.strip()

                    NextPTag = H3Tag.find_next_sibling('p')

                    if NextPTag:
                        TagPText = NextPTag.text
                        TagPText = str(TagPText)
                        TagPText = TagPText.replace('\\n', '\n')

                        BasePageDict[NameForDict] = TagPText

                print(BasePageDict)

            GetBasePageRecords()

        GetCurrentRecords()

    CheckForHistoricalRecords(URL)

    def SOA(URL):

        if os.path.exists('SOA.txt'):
            os.remove('SOA.txt')

        if BasePageDict['SOA'] == False:

            for SOARecordStr in BasePageDict['SOA']:
                if os.path.exists('SOA.txt'):
                    with open('SOA.txt', 'a') as f:
                        f.write(f'{SOARecordStr}')
                else:
                    with open('SOA.txt', 'x') as f:
                        f.write(f'{SOARecordStr}')


        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/soa/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]
        def FilterData():

            global SOARecordList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')
            DateFind = re.findall(DateRegex, TagP)

            Indexs = []

            for i in list(DateFind):
                Indexs.append(TagP.index(i))
            SOARecordList = []

            for x in range(len(Indexs)-1):
                I1 = Indexs[0]
                I2 = Indexs[1]
                SOARecordList.append(TagP[I1:I2])
                Indexs.pop(0)
            try:
                LastIndex = Indexs[-1]
                End = TagP.rfind('\n')
                SOARecordList.append(TagP[LastIndex:End])
            except IndexError:
                global NoSOARecordsFound
                NoSOARecordsFound = True
                OutputData()
        def OutputData():

            global SOAOutputList
            SOAOutputList = []
            for i in range(len(SOARecordList)):
                SOARecordStr = str(SOARecordList[i])
                SOARecordStr = SOARecordStr.replace('-&gt;', '->')

                SOAOutputList.append(SOARecordStr)

            def ConsoleOutput():

                for SOARecordStr in SOAOutputList:

                    print(SOARecordStr)


            def TXTOutput():

                for SOARecordStr in SOAOutputList:
                    if os.path.exists('SOA.txt'):
                        with open('SOA.txt', 'a') as f:
                            f.write(f'{SOARecordStr}\n\n')
                    else:
                        with open('SOA.txt', 'x') as f:
                            f.write(f'{SOARecordStr}\n\n')

                for SOARecordStr in BasePageDict['SOA']:
                    if os.path.exists('SOA.txt'):
                        with open('SOA.txt', 'a') as f:
                            f.write(f'{SOARecordStr}')
                    else:
                        with open('SOA.txt', 'x') as f:
                            f.write(f'{SOARecordStr}')


            ConsoleOutput()
            TXTOutput()


        GetData()
        FilterData()
        OutputData()

    def NS(URL):

        if os.path.exists('NS.txt'):
            os.remove('NS.txt')

        if BasePageDict['NS'] == False:

            for NSRecordStr in BasePageDict['NS']:
                if os.path.exists('NS.txt'):
                    with open('NS.txt', 'a') as f:
                        f.write(f'{NSRecordStr}')
                else:
                    with open('NS.txt', 'x') as f:
                        f.write(f'{NSRecordStr}')


        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"

            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/ns/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]

        def FilterData():

            global Lines, NSList, NSRLinksList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')

            x = TagP.splitlines()

            Lines = []

            for i in range(len(x)):

                if re.findall(DateRegex, x[i]):
                    Lines.append(x[i])
                else:
                    pass

            NSList = []
            NSRLinksList = []

        def OutputData():

            global NSList, NSRLinksList

            def ConsoleOutput():

                for i in Lines:
                    Index1 = (i.find('href='))
                    Index2 = (i.find('>'))

                    RLink = i[Index1 + 6:Index2 - 2]

                    NSRLinksList.append(RLink)

                    Index1 = (i.find('<'))
                    Index2 = (i.find('>'))

                    LinkRemove = i[Index1:Index2 + 1]

                    i = i.replace(LinkRemove, '')

                    i = i.replace('-&gt;', '->')

                    NSList.append(str(i))

                for i in NSList:
                    print(i)

                #for i in NSRLinksList:
                #    print(i)


            def TXTOutput():

                if os.path.exists('NS.txt'):
                    with open('NS.txt', 'a') as f:
                        for i in NSList:
                            f.write(f'{i}\n\n')
                else:
                    with open('NS.txt', 'x') as f:
                        for i in NSList:
                            f.write(f'{i}\n\n')


                for NSRecordStr in BasePageDict['NS']:
                    if os.path.exists('NS.txt'):
                        with open('NS.txt', 'a') as f:
                            f.write(f'{NSRecordStr}')
                    else:
                        with open('NS.txt', 'x') as f:
                            f.write(f'{NSRecordStr}')



            ConsoleOutput()
            TXTOutput()

        GetData()
        FilterData()
        OutputData()

    def MX(URL):

        if os.path.exists('MX.txt'):
            os.remove('MX.txt')


        if BasePageDict['MX'] == False:

            for MXRecordStr in BasePageDict['MX']:
                if os.path.exists('MX.txt'):
                    with open('MX.txt', 'a') as f:
                        f.write(f'{MXRecordStr}')
                else:
                    with open('MX.txt', 'x') as f:
                        f.write(f'{MXRecordStr}')


        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/mx/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]

        def FilterData():

            global Lines, MXList, MXRLinksList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')

            x = TagP.splitlines()

            Lines = []

            for i in range(len(x)):

                if re.findall(DateRegex, x[i]):

                    Lines.append(x[i])

                else:
                    pass

                MXList = []
                MXRLinksList = []

        def OutputData():

            for i in Lines:
                Index1 = (i.find('href='))
                Index2 = (i.find('>'))

                RLink = i[Index1 + 6:Index2 - 2]

                MXRLinksList.append(RLink)

                Index1 = (i.find('<'))
                Index2 = (i.find('>'))

                LinkRemove = i[Index1:Index2 + 1]

                i = i.replace(LinkRemove, '')

                i = i.replace('-&gt;', '->')

                MXList.append(str(i))

            for i in MXList:
                print(i)
            #for i in MXRLinksList:
            #    print(i)

            if os.path.exists('MX.txt'):
                with open('MX.txt', 'a') as f:
                    for i in MXList:
                        f.write(f'{i}\n\n')
            else:
                with open('MX.txt', 'x') as f:
                    for i in MXList:
                        f.write(f'{i}\n\n')

            for MXRecordStr in BasePageDict['MX']:
                if os.path.exists('MX.txt'):
                    with open('MX.txt', 'a') as f:
                        f.write(f'{MXRecordStr}')
                else:
                    with open('MX.txt', 'x') as f:
                        f.write(f'{MXRecordStr}')

        GetData()
        FilterData()
        OutputData()

    def A(URL):

        if os.path.exists('A.txt'):
            os.remove('A.txt')

        if BasePageDict['A'] == False:

            for ARecordStr in BasePageDict['A']:
                if os.path.exists('A.txt'):
                    with open('A.txt', 'a') as f:
                        f.write(f'{ARecordStr}')
                else:
                    with open('A.txt', 'x') as f:
                        f.write(f'{ARecordStr}')

        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/a/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]

        def FilterData():

            global Lines, AList, ARLinksList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')


            x = TagP.splitlines()

            Lines = []

            for i in range(len(x)):

                if re.findall(DateRegex, x[i]):

                    Lines.append(x[i])

                else:
                    pass

                AList = []
                ARLinksList = []

        def OutputData():

            for i in Lines:
                Index1 = (i.find('href='))
                Index2 = (i.find('>'))

                RLink = i[Index1 + 6:Index2 - 2]

                ARLinksList.append(RLink)

                Index1 = (i.find('<'))
                Index2 = (i.find('>'))

                LinkRemove = i[Index1:Index2 + 1]

                i = i.replace(LinkRemove, '')

                i = i.replace('-&gt;', '->')


                AList.append(str(i))

            for i in AList:
                print(i)

            #for i in ARLinksList:
            #    print(i)

            if os.path.exists('A.txt'):
                with open('A.txt', 'a') as f:
                    for i in AList:
                        f.write(f'{i}\n\n')
            else:
                with open('A.txt', 'x') as f:
                    for i in AList:
                        f.write(f'{i}\n\n')

            for ARecordStr in BasePageDict['A']:
                if os.path.exists('A.txt'):
                    with open('A.txt', 'a') as f:
                        f.write(f'{ARecordStr}')
                else:
                    with open('A.txt', 'x') as f:
                        f.write(f'{ARecordStr}')

        GetData()
        FilterData()
        OutputData()

    def AAAA(URL):

        if os.path.exists('AAAA.txt'):
            os.remove('AAAA.txt')

        if BasePageDict['AAAA'] == False:

            for AAAARecordStr in BasePageDict['AAAA']:
                if os.path.exists('AAAA.txt'):
                    with open('AAAA.txt', 'a') as f:
                        f.write(f'{AAAARecordStr}')
                else:
                    with open('AAAA.txt', 'x') as f:
                        f.write(f'{AAAARecordStr}')
        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/aaaa/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]

        def FilterData():

            global Lines, AAAAList, AAAARLinksList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')

            x = TagP.splitlines()

            Lines = []

            for i in range(len(x)):

                if re.findall(DateRegex, x[i]):

                    Lines.append(x[i])

                else:
                    pass

                AAAAList = []
                AAAARLinksList = []

        def OutputData():

            for i in Lines:
                Index1 = (i.find('href='))
                Index2 = (i.find('>'))

                RLink = i[Index1 + 6:Index2 - 2]

                AAAARLinksList.append(RLink)

                Index1 = (i.find('<'))
                Index2 = (i.find('>'))

                LinkRemove = i[Index1:Index2 + 1]

                i = i.replace(LinkRemove, '')

                AAAAList.append(str(i))

            for i in AAAAList:
                print(i)

            #for i in AAAARLinksList:
            #    print(i)


            if os.path.exists('AAAA.txt'):
                with open('AAAA.txt', 'a') as f:
                    for i in AAAAList:
                        f.write(f'{i}\n\n')

            else:
                with open('AAAA.txt', 'x') as f:
                    for i in AAAAList:
                        f.write(f'{i}\n\n')

            for AAAARecordStr in BasePageDict['AAAA']:
                if os.path.exists('AAAA.txt'):
                    with open('AAAA.txt', 'a') as f:
                        f.write(f'{AAAARecordStr}')
                else:
                    with open('AAAA.txt', 'x') as f:
                        f.write(f'{AAAARecordStr}')

        GetData()
        FilterData()
        OutputData()

    def TXT(URL):

        if os.path.exists('TXT.txt'):
            os.remove('TXT.txt')

        if BasePageDict['AAAA'] == False:

            for AAAARecordStr in BasePageDict['AAAA']:
                if os.path.exists('AAAA.txt'):
                    with open('AAAA.txt', 'a') as f:
                        f.write(f'{AAAARecordStr}')
                else:
                    with open('AAAA.txt', 'x') as f:
                        f.write(f'{AAAARecordStr}')
        def GetData():

            global DateRegex, TagP, Replace, tags

            DateRegex = r"\d{4}-\d{2}-\d{2} -&gt; \d{4}-\d{2}-\d{2}"
            tags = [
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

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/90.0.4430.212 Safari/537.36'}

            Request = requests.get(f'https://dnshistory.org/historical-dns-records/txt/{URL}', headers=headers)

            Response = Request.text

            soup = BeautifulSoup(Response, 'html.parser')

            TagP = (soup.find_all('p'))

            Replace = ['[', ']', "'"]

        def FilterData():

            global TXTRecordList, TagP

            for i in tags:
                Replace.append(f'<{i}>')
                Replace.append(f'</{i}>')
                Replace.append(f'<{i}/>')

            for i in Replace:
                TagP = str(TagP).replace(i, '')
            DateFind = re.findall(DateRegex, TagP)

            Indexs = []

            for i in list(DateFind):
                Indexs.append(TagP.index(i))
            TXTRecordList = []

            for x in range(len(Indexs) - 1):
                I1 = Indexs[0]
                I2 = Indexs[1]
                TXTRecordList.append(TagP[I1:I2])
                Indexs.pop(0)
            try:
                LastIndex = Indexs[-1]
                End = TagP.rfind('\n')
                TXTRecordList.append(TagP[LastIndex:End])
            except:
                print('No TXT Records Found')
                OutputData()
        def OutputData():

            global TXTOutputList
            TXTOutputList = []
            for i in range(len(TXTRecordList)):
                TXTRecordStr = str(TXTRecordList[i])
                TXTRecordStr = TXTRecordStr.replace('-&gt;', '->')

                TXTOutputList.append(TXTRecordStr)

            def ConsoleOutput():

                for TXTRecordStr in TXTOutputList:

                    print(TXTRecordStr)


            def TXTOutput():

                for TXTRecordStr in TXTOutputList:
                    if os.path.exists('TXT.txt'):
                        with open('TXT.txt', 'a') as f:
                            f.write(f'{TXTRecordStr}\n\n')
                    else:
                        with open('TXT.txt', 'x') as f:
                            f.write(f'{TXTRecordStr}\n\n')

            for AAAARecordStr in BasePageDict['AAAA']:
                if os.path.exists('AAAA.txt'):
                    with open('AAAA.txt', 'a') as f:
                        f.write(f'{AAAARecordStr}')
                else:
                    with open('AAAA.txt', 'x') as f:
                        f.write(f'{AAAARecordStr}')

            ConsoleOutput()
            TXTOutput()

        GetData()
        FilterData()
        OutputData()

    SOA(URL)
    NS(URL)
    MX(URL)
    A(URL)
    AAAA(URL)
    TXT(URL)
    print('Done')
    exit()
if __name__ == "__main__":
    main()


# Beta 0.2.2
# HistorianDNS

# Not A Bird
# CEO of Bird Inc.

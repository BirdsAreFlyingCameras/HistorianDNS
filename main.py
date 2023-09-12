from bs4 import BeautifulSoup
import requests
import pprint as pp
import re


def SOA():
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

        Request = requests.get('https://dnshistory.org/historical-dns-records/soa/dnshistory.org', headers=headers)

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
        IndexForSplit = iter(Indexs)

        for Even, Odd in zip(IndexForSplit, IndexForSplit):
            SOARecordList.append(TagP[Even:Odd])

        LastIndex = Indexs[-1]
        End = TagP.rfind('\n')
        TXTRecordList.append(TagP[LastIndex:End])
    def OutputData():

        for i in range(len(SOARecordList)):
            SOARecordStr = str(SOARecordList[i])

            print(SOARecordStr)

    GetData()
    FilterData()
    OutputData()


def NS():
    def GetData():

        print('GetData')

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

        Request = requests.get('https://dnshistory.org/historical-dns-records/ns/dnshistory.org', headers=headers)

        Response = Request.text

        soup = BeautifulSoup(Response, 'html.parser')

        TagP = (soup.find_all('p'))

        Replace = ['[', ']', "'"]

    def FilterData():

        print('FilterData')

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

        print('OutputData')

        for i in Lines:
            Index1 = (i.find('href='))
            Index2 = (i.find('>'))

            RLink = i[Index1 + 6:Index2 - 2]

            NSRLinksList.append(RLink)

            Index1 = (i.find('<'))
            Index2 = (i.find('>'))

            LinkRemove = i[Index1:Index2 + 1]

            i = i.replace(LinkRemove, '')

            NSList.append(str(i))

        for i in NSList:
            print(i)

        for i in NSRLinksList:
            print(i)

    GetData()
    FilterData()
    OutputData()


def MX():
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

        Request = requests.get('https://dnshistory.org/historical-dns-records/mx/dnshistory.org', headers=headers)

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

            MXList.append(str(i))

        for i in MXList:
            print(i)
        for i in MXRLinksList:
            print(i)

    GetData()
    FilterData()
    OutputData()


def A():
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

        Request = requests.get('https://dnshistory.org/historical-dns-records/a/dnshistory.org', headers=headers)

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

            AList.append(str(i))

        for i in AList:
            print(i)

        for i in ARLinksList:
            print(i)

    GetData()
    FilterData()
    OutputData()


def AAAA():
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

        Request = requests.get('https://dnshistory.org/historical-dns-records/aaaa/dnshistory.org', headers=headers)

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

        for i in AAAARLinksList:
            print(i)

    GetData()
    FilterData()
    OutputData()


def TXT():
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

        Request = requests.get('https://dnshistory.org/historical-dns-records/txt/dnshistory.org', headers=headers)

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
        IndexForSplit = iter(Indexs)

        for Even, Odd in zip(IndexForSplit, IndexForSplit):
            TXTRecordList.append(TagP[Even:Odd])

        LastIndex = Indexs[-1]
        End = TagP.rfind('\n')
        TXTRecordList.append(TagP[LastIndex:End])

    def OutputData():

        for i in range(len(TXTRecordList)):
            TXTRecordStr = str(TXTRecordList[i])

            print(TXTRecordStr)

    GetData()
    FilterData()
    OutputData()


TXT()

# SOA()


# Dev State
# HistorianDNS

# Not A Bird
# CEO of Bird Inc.

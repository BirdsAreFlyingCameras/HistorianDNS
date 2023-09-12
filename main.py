from bs4 import BeautifulSoup
import requests
import pprint as pp
import re


def SOA():

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

    for i in range(len(SOARecordList)):

        SOARecordStr = str(SOARecordList[i])

        print(SOARecordStr)

SOA()


# Dev State
# HistorianDNS

# Not A Bird
# CEO of Bird Inc.
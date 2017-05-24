from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


with open("indeed.csv", "w", encoding="utf-8") as f:
    f.write('job_title' + ',' + 'summary' + "\n")

    query = ["software+engineer", "data+scientist"]
    for q in query:
        start = 0
        for i in range(41):
            start = start + 25
            start_url = "http://api.indeed.com/ads/apisearch?publisher=8305212411288598&q=" + q +"&limit=25&start=" + str(start) + "&fromage=10&st=jobsite&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&format=json"
            resp = requests.get(start_url).content.decode()
            work = json.loads(resp)
            results = work['results']
            # print(type(work['results']))
            #
            # print(len(work['results']))
            # print(results[4]['url'])

            for i in range(len(work['results'])):
                # print(results[i]['url'])
                url = results[i]['url']
                resp = requests.get(url)
                soup = BeautifulSoup(resp.content, "html.parser")
                # print(soup)
                jobtitle = soup.find(size="+1").get_text()
                print(jobtitle)
                summary = soup.find(id = 'job_summary').get_text()
                summary = summary.lower()
                summary = summary.replace(',', '')
                summary = summary.replace('\n', '')
                summary = summary.replace('\t', '')
                # print(summary)
                f.write(jobtitle.lower() + ',' + summary + "\n")

import requests
from bs4 import BeautifulSoup
import requests
from Wappalyzer import Wappalyzer, WebPage

def check(ip_address, port):
    try:
        res = requests.get(f"https://{ip_address}:{port}")
        if res.status_code == 200:
            return "https"
    except Exception:
        pass

    try:     
        res = requests.get(f"http://{ip_address}:{port}")
        if res.status_code == 200:
            return "http"
    except Exception:
        pass

    return ""


def get_technologies(ip_address, port, s):
    res = ""
    target = f"{s}://{ip_address}:{port}"
    page = requests.get(target)
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.title:
        title = soup.title.text
    else:
        title = ""


    title = f"TITLE: {title}"

    try:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(target)
        technologies = wappalyzer.analyze_with_versions_and_categories(webpage)

        res += "    | TECHNOLOGIES:\n"


        di = {}
        for tech in technologies:
            category = technologies[tech]['categories'][0]
            if technologies[tech]['versions']:
                version = technologies[tech]['versions'][0]
            else:
                version = ""

            if category in di.keys():
                di[category] += [{tech:version}]
            else:
                di[category] = [{tech:version}]
            
        for category in di:
            res += f"    |    {category}:\n"
            for i in di[category]:
                for j in i.keys():
                    res += f"    |       {j} {i[j]}\n"
        if "\n" in res:
            res = res[:-2]
        return [title, res]
    except Exception:
        return ["", ""]
    

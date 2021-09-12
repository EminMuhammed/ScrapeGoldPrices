import pandas as pd
import requests
from bs4 import BeautifulSoup

# istenilen yillar
start_year = 2015
finish_year = 2021
baseurl = "https://altin.in/arsiv"
url = f"https://altin.in/arsiv/2021"


def createyear_url(start_year, finish_year):
    url_year = [baseurl + "/" + str(year) for year in range(start_year, finish_year + 1)]
    return url_year


urlliste = createyear_url(start_year, finish_year)


def get_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def find_month_number(soup):
    month_column = soup.find("ul", attrs={"class": "ay"})
    month_number = len(month_column.find_all("li"))
    return month_number


def concat_year_mounth(urlliste):
    url_year_month_list = [value + "/" + str(i) for value in urlliste for i in
                           range(1, find_month_number(get_url(value)) + 1)]
    return url_year_month_list


url_year_month = concat_year_mounth(urlliste)


def find_day_number(soup):
    day_column = soup.find("ul", attrs={"class": "gun"})
    day_number = len(day_column.find_all("li"))
    return day_number


def concat_year_month_day(year_month_list):
    liste = [value + "/" + str(daynumber) for value in year_month_list for daynumber in
             range(1, find_day_number(get_url(value)) + 1)]
    return liste


year_month_day_list = concat_year_month_day(url_year_month)


def get_gold(urllist):
    # url listesinde gezer ve altın fiyatlarını alır.
    liste1 = []
    for ln in urllist:
        print(ln)
        soup = get_url(ln)
        alis = ""
        satis = ""
        try:
            alis = soup.find("li", attrs={"title": "Gram Altın - Alış"}).text
            satis = soup.find("li", attrs={"title": "Gram Altın - Satış"}).text
            liste1.append([ln, alis, satis])
        except:
            pass

    return liste1


data = get_gold(year_month_day_list)


def save_data(data, name):
    import pandas as pd
    df = pd.DataFrame(data, columns=["url", "alis", "satis"])
    df.to_excel(f"{name}.xlsx")


save_data(data, "altinfiyatlari")

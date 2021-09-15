import pandas as pd
import requests
from bs4 import BeautifulSoup

start_year = 2019
finish_year = 2021
baseurl = "https://altin.in/arsiv"
url = f"https://altin.in/arsiv/2021"


def createyear_url(start_year, finish_year):
    """
    It creates a link for each year by adding it to the end of the baseurl according to the given start and end years.

    Parameters
    ----------
    start_year: int
    start year
    finish_year: bitiş yılı
    end year

    Returns
    -------
    list
    """

    url_year = [baseurl + "/" + str(year) for year in range(start_year, finish_year + 1)]
    return url_year


urlliste = createyear_url(start_year, finish_year)


def get_url(url):
    """
    parts with beautifulsoup by sending a request to the given link

    Parameters
    ----------
    url: string
    url to request

    Returns
    -------
    bs4
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def find_month_number(soup):
    """
    Returns the month number of the included page resource.

    Parameters
    ----------
    soup: BeautifulSoup
    The page source of the site for which the number of months is to be obtained is given

    Returns
    -------
    int
    """

    month_column = soup.find("ul", attrs={"class": "ay"})
    month_number = len(month_column.find_all("li"))
    return month_number


def concat_year_month(urlliste):
    """
    By sending a request to the link with the year numbers, it takes the month numbers and adds them to the end of the link (url + year + month)

    Parameters
    ----------
    urlliste: liste
    list with only year at the end of the link address

    Returns
    -------
    list
    """

    url_year_month_list = [value + "/" + str(i) for value in urlliste for i in
                           range(1, find_month_number(get_url(value)) + 1)]
    return url_year_month_list


url_year_month = concat_year_month(urlliste)


def find_day_number(soup):
    """
    finds how many days are in the given page resource

    Parameters
    ----------
    soup: BeautifulSoup
    The page source of the site for which the number of days is to be obtained is given

    Returns
    -------
    int
    """

    day_column = soup.find("ul", attrs={"class": "gun"})
    day_number = len(day_column.find_all("li"))
    return day_number


def concat_year_month_day(year_month_list):
    """
    By sending a request to the links consisting of year and month, it finds the number of days and adds it to the
    end of the link. (url + year + month + day)

    Parameters
    ----------
    year_month_list: list
    link list with year and month


    Returns
    -------
    list
    """

    liste = [value + "/" + str(daynumber) for value in year_month_list for daynumber in
             range(1, find_day_number(get_url(value)) + 1)]
    return liste


year_month_day_list = concat_year_month_day(url_year_month)


def get_gold(urllist):
    """
    Gets gold information by requesting links
    Parameters
    ----------
    urllist: list
    url list

    Returns
    -------
    list
    """

    liste1 = []
    for ln in urllist:
        print(ln)
        soup = get_url(ln)
        try:
            alis = soup.find("li", attrs={"title": "Gram Altın - Alış"}).text
            satis = soup.find("li", attrs={"title": "Gram Altın - Satış"}).text
            liste1.append([ln, alis, satis])
        except:
            pass

    return liste1


data = get_gold(year_month_day_list)


def save_data(data, name):
    """
    convert list to excel
    Parameters
    ----------
    data: list
    list with gold information
    name: string
    excel file name

    Returns
    -------
    None
    """

    df = pd.DataFrame(data, columns=["url", "alis", "satis"])
    df.to_excel(f"{name}.xlsx")


save_data(data, "altinfiyatlari_yeni")
